from django.test import TestCase, override_settings
from django.core import mail
from unittest import mock
from django.contrib import messages
from .models import Setup
from .utils import MailSender  # Import your MailSender class

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class MailSenderTestCase(TestCase):
    def setUp(self):
        self.subject = "Test Subject"
        self.body = "Test Body"
        self.to = ['titusowuor30@gmail.com']
        self.attachments = []

    @mock.patch.object(messages, 'success')
    def test_send_email_success(self, mock_success):
        # Mock Setup.objects.first()
        setup_mock = mock.MagicMock(spec=Setup)
        setup_mock.email_host = 'mail.fernbrookapartments.com'
        setup_mock.email_port = 465
        setup_mock.support_reply_email = 'info@fernbrookapartments.com'
        setup_mock.email_password = 'Fernbrook@2023'
        setup_mock.use_tls = True
        setup_mock.fail_silently = False
        with mock.patch('core.models.Setup.objects.first', return_value=setup_mock):
            mail_sender = MailSender(self.subject, self.body, self.to, self.attachments)
            mail_sender.request = None  # Mock the request attribute

            mail_sender.send_email()

        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, self.subject)
        self.assertEqual(sent_email.body, self.body)
        self.assertEqual(sent_email.from_email, 'info@fernbrookapartments.com')
        self.assertEqual(sent_email.to, self.to)

        mock_success.assert_called_once_with(None, 'Email sent successfully!')

    @mock.patch.object(messages, 'info')
    def test_send_email_failure(self, mock_info):
        # Mock Setup.objects.first() to raise an exception
        with mock.patch('core.models.Setup.objects.first', side_effect=Exception('Test Exception')):
            mail_sender = MailSender(self.subject, self.body, self.to, self.attachments)
            mail_sender.request = None  # Mock the request attribute

            mail_sender.send_email()

        mock_info.assert_called_once_with(None, 'Email send error:Test Exception')

