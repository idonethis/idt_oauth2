import logging
import requests

from django.conf import settings

OAUTH2_AUTHORIZE_URL = '%s/oauth/authorize' % settings.SLACK_DOMAIN
OAUTH2_TOKEN_EXCHANGE_URL = '%s/api/oauth.access' % settings.SLACK_DOMAIN

def get_authorize_config():
    service_url = OAUTH2_AUTHORIZE_URL
    query_params = {
        'client_id': settings.SLACK_OAUTH2_CLIENT_ID,
        'scope': 'read,post,identify',
    }

    return (service_url, query_params)


def token_exchange(code, redirect_uri):
    # See: https://api.slack.com/docs/oauth and https://api.slack.com/methods/oauth.access
    post_data = {
        'client_id': settings.SLACK_OAUTH2_CLIENT_ID,
        'client_secret': settings.SLACK_OAUTH2_CLIENT_SECRET,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    logging.info(
            'slack oauth2 token exchange post: %s',
            post_data)
    response = requests.post(
        OAUTH2_TOKEN_EXCHANGE_URL, data=post_data)
    logging.info(
            'slack oauth2 token exchange response status code: %s, content: %s',
            response.status_code, response.json())
    return response.json()
