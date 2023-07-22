import os
import sys
from AdminRealEstate.wsgi import application
from whitenoise import WhiteNoise


sys.path.insert(0, os.path.dirname(__file__))

environ = os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "AdminRealEstate.settings")

application = WhiteNoise(
    application, root="/home/tdbsoftc/public_html/fernbrook/static/")

application.add_files(
    "/home/tdbsoftc/public_html/fernbrook/static/", prefix="more-files/")
