import logging
import requests

from django.conf import settings

OAUTH2_AUTHORIZE_URL = '%s/o/oauth2/auth' % settings.GOOGLE_DOMAIN
OAUTH2_TOKEN_EXCHANGE_URL = '%s/o/oauth2/token' % settings.GOOGLE_DOMAIN

def get_authorize_config(redirect_uri):
    service_url = OAUTH2_AUTHORIZE_URL
    query_params = {
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'scope': 'openid email',
        'redirect_uri': redirect_uri,
    }

    return (service_url, query_params)


def token_exchange(code, redirect_uri):
    post_data = {
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    logging.info(
            'google oauth2 token exchange post: %s',
            post_data)
    response = requests.post(
        OAUTH2_TOKEN_EXCHANGE_URL, data=post_data)
    logging.info(
            'google oauth2 token exchange response status code: %s, content: %s',
            response.status_code, response.json())
    return response.json()
