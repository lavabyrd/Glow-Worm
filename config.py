import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    VERIFICATION_TOKEN = os.environ.get(
        "SO_VERIFICATION_TOKEN")
    BOT_TOKEN = os.environ.get("GLOW_BOT_TOKEN")
    USER_TOKEN = os.environ.get("GLOW_USER_TOKEN")
    OAUTH_SCOPE = os.environ.get("SCOPES")
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get(
        "CLIENT_SECRET")
    CELERY_BROKER_URL = os.environ.get(
        "REDIS_URL")
    CELERY_RESULT_BACKEND = os.environ.get(
        "REDIS_URL")
