from os import getenv
from dotenv import load_dotenv


load_dotenv()

secret_key = getenv('SECRET_KEY')
email_host_user = getenv('EMAIL_HOST_USER')
email_host_password = getenv('EMAIL_HOST_PASSWORD')
default_from_email = getenv('DEFAULT_FROM_EMAIL')
email_host = getenv('EMAIL_HOST')
email_port = int(getenv('EMAIL_PORT'))
