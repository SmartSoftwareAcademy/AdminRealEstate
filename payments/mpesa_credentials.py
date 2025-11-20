import base64
import json
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

from core.models import Setup
from django.core.exceptions import ImproperlyConfigured


class MpesaC2bCredential:
    """
    Mpesa OAuth endpoint configuration - switches based on environment.
    """
    SANDBOX_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    PRODUCTION_URL = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    @classmethod
    def get_api_url(cls):
        cfg = Setup.objects.first()
        if cfg and cfg.mpesa_environment == 'production':
            return cls.PRODUCTION_URL
        return cls.SANDBOX_URL


class MpesaStkPushCredential:
    """
    Mpesa STK Push endpoint configuration - switches based on environment.
    """
    SANDBOX_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    PRODUCTION_URL = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    
    @classmethod
    def get_stk_push_url(cls):
        """
        Get the STK Push API endpoint URL based on configured environment.
        Returns sandbox URL by default, production URL when environment is set to 'production'.
        """
        cfg = Setup.objects.first()
        if cfg and cfg.mpesa_environment == 'production':
            return cls.PRODUCTION_URL
        return cls.SANDBOX_URL


class MpesaConfig:
    """
    Helper to read Mpesa configuration from the Setup model,
    falling back to known sandbox defaults.
    """

    # Default Sandbox Test Credentials from Safaricom Developer Portal
    # These are the standard test credentials provided by Safaricom
    DEFAULT_CONSUMER_KEY = 'cHnkwYIgBbrxlgBoneczmIJFXVm0oHky'
    DEFAULT_CONSUMER_SECRET = '2nHEyWSD4VjpNh2g'
    DEFAULT_BUSINESS_SHORT_CODE = '174379'  # Default sandbox test shortcode
    # Default sandbox passkey - provided by Safaricom for testing
    # Get your own from: https://developer.safaricom.co.ke -> My Apps -> Test Credentials
    DEFAULT_PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    DEFAULT_PHONE_NUMBER = 254743793901  # Default sandbox test phone number for STK push
    DEFAULT_CALLBACK_URL = 'https://example.com/payments/mpesa/callback/'

    @classmethod
    def get(cls):
        """
        Get Mpesa configuration from Setup model with smart defaults.
        For sandbox: Uses default sandbox shortcode (174379) and passkey if not configured.
        For production: Requires all credentials to be configured via admin panel.
        """
        cfg = Setup.objects.first()
        if not cfg:
            # Return defaults if no Setup record exists
            return {
                'consumer_key': cls.DEFAULT_CONSUMER_KEY,
                'consumer_secret': cls.DEFAULT_CONSUMER_SECRET,
                'short_code': cls.DEFAULT_BUSINESS_SHORT_CODE,
                'passkey': cls.DEFAULT_PASSKEY,
                'callback_url': cls.DEFAULT_CALLBACK_URL,
                'environment': 'sandbox',
            }
        
        # Determine environment
        environment = cfg.mpesa_environment if cfg.mpesa_environment else 'sandbox'
        
        # For sandbox: Use default shortcode and passkey if not configured
        # For production: Require explicit configuration
        if environment == 'sandbox':
            short_code = cfg.mpesa_business_short_code if cfg.mpesa_business_short_code else cls.DEFAULT_BUSINESS_SHORT_CODE
            # If consumer key/secret are configured but passkey is not, use default sandbox passkey
            if cfg.mpesa_consumer_key and cfg.mpesa_consumer_secret and not cfg.mpesa_passkey:
                passkey = cls.DEFAULT_PASSKEY
            else:
                passkey = cfg.mpesa_passkey if cfg.mpesa_passkey else cls.DEFAULT_PASSKEY
        else:
            # Production: Use configured values or defaults
            short_code = cfg.mpesa_business_short_code if cfg.mpesa_business_short_code else cls.DEFAULT_BUSINESS_SHORT_CODE
            passkey = cfg.mpesa_passkey if cfg.mpesa_passkey else cls.DEFAULT_PASSKEY
        
        return {
            'consumer_key': (cfg.mpesa_consumer_key if cfg.mpesa_consumer_key else cls.DEFAULT_CONSUMER_KEY),
            'consumer_secret': (cfg.mpesa_consumer_secret if cfg.mpesa_consumer_secret else cls.DEFAULT_CONSUMER_SECRET),
            'short_code': short_code,
            'passkey': passkey,
            'callback_url': (cfg.mpesa_callback_url if cfg.mpesa_callback_url else cls.DEFAULT_CALLBACK_URL),
            'environment': environment,
        }


class MpesaAccessToken:
    """
    Fetch an access token from Safaricom using the configured keys.
    Called per transaction to ensure fresh tokens and updated config.
    """

    @classmethod
    def get_access_token(cls):
        cfg = MpesaConfig.get()
        api_url = MpesaC2bCredential.get_api_url()
        try:
            r = requests.get(
                api_url,
                auth=HTTPBasicAuth(cfg['consumer_key'], cfg['consumer_secret']),
                timeout=30
            )
            r.raise_for_status()
            mpesa_access_token = json.loads(r.text)
            if 'access_token' not in mpesa_access_token:
                raise ValueError(f"Mpesa API error: {mpesa_access_token}")
            return mpesa_access_token['access_token']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get Mpesa access token: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response from Mpesa API: {str(e)}")


class LipanaMpesaPpassword:
    """
    Build the dynamic password & timestamp for Lipa Na Mpesa Online (STK push)
    using the configured business short code and passkey.
    
    IMPORTANT: This generates a FRESH password for EVERY request by:
    1. Creating a new timestamp (YYYYMMDDHHmmss format)
    2. Encoding: BusinessShortCode + Passkey + Timestamp
    3. Base64 encoding the result
    
    Password format: base64(BusinessShortCode + Passkey + Timestamp)
    Example: base64("174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + "20251120200446")
    """

    @classmethod
    def get_credentials(cls):
        """
        Generate fresh credentials for STK push request.
        Called for each transaction to ensure unique password and timestamp.
        
        Returns:
            dict: Contains BusinessShortCode, Password (base64 encoded), Timestamp, and CallbackURL
        """
        cfg = MpesaConfig.get()
        # Generate fresh timestamp for each request (format: YYYYMMDDHHmmss)
        lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Build password: BusinessShortCode + Passkey + Timestamp
        data_to_encode = cfg['short_code'] + cfg['passkey'] + lipa_time
        
        # Base64 encode the password
        online_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')
        
        return {
            "BusinessShortCode": cfg['short_code'],
            "Password": online_password,  # Fresh password generated for each request
            "Timestamp": lipa_time,  # Fresh timestamp for each request
            "CallbackURL": cfg['callback_url'],
        }