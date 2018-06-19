import os
try:
    import local_config
except:
    pass

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    VERIFICATION_TOKEN = os.environ.get(
        "SO_VERIFICATION_TOKEN") or local_config.veri
    BOT_TOKEN = os.environ.get("GB_TOKEN") or local_config.bot_token
    USER_TOKEN = os.environ.get("GB_USER_TOKEN") or local_config.user_token
    OAUTH_SCOPE = os.environ.get("SCOPES") or local_config.scopes
    CLIENT_ID = os.environ.get("CLIENT_ID") or local_config.client_id
    CLIENT_SECRET = os.environ.get(
        "CLIENT_SECRET") or local_config.client_secret
    CELERY_BROKER_URL = os.environ.get(
        "CELERY_BROKER_URL") or local_config.celery_broker_url
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND") or local_config.celery_url_results
