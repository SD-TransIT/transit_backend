import logging
import sys

from django.contrib.auth import get_user_model
from os import getenv

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

login = getenv('SUPERUSER_LOGIN', None)
passwd = getenv('SUPERUSER_PASSWORD', None)
mail = getenv('SUPERUSER_EMAIL', None)

if not (login and passwd):
    logging.info("SUPERUSER_LOGIN or SUPERUSER_PASSWORD not provided, superuser will not be automatically created")
    sys.exit()

User = get_user_model()
exists = User.objects.filter(username=login).exists()

if exists:
    logging.info(F"Superuser with login {login} already exists. New user will not be created")
    sys.exit()

User.objects.create_superuser(login, mail, passwd)
logging.info(F"Superuser with login {login} created from .env specification")

