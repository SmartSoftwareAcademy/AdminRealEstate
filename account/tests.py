from django.test import TestCase

# Create your tests here.
import socket

host_name = "tdbsoft.co.ke"
ip_address = socket.gethostbyname(host_name)
print("IP Address:", ip_address)
