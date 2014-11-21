from base64 import b64encode
import logging
import requests

from django.conf import settings

OAUTH2_AUTHORIZE_URL = '%s/api/oauth2/authorize/' % settings.IDT_DOMAIN
OAUTH2_TOKEN_EXCHANGE_URL = '%s/api/oauth2/token/' % settings.IDT_DOMAIN

def get_authorize_config():
    service_url = OAUTH2_AUTHORIZE_URL
    query_params = {
        'client_id': settings.IDT_OAUTH2_CLIENT_ID,
        'approval_prompt': 'auto',
    }

    return (service_url, query_params)


def token_exchange(code, redirect_uri):
    headers = get_idt_oauth2_client_id_headers()
    post_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
    }
    logging.info(
            'idt oauth2 token exchange post: %s, headers: %s',
            post_data, headers)
    response = requests.post(
        OAUTH2_TOKEN_EXCHANGE_URL, headers=headers, data=post_data)
    logging.info(
            'idt oauth2 token exchange response status code: %s, content: %s',
            response.status_code, response.json())
    return response.json()


def token_refresh(refresh_token):
    headers = get_idt_oauth2_client_id_headers()
    post_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    logging.info(
            'idt oauth2 token refresh post: %s, headers: %s',
            post_data, headers)
    response = requests.post(
        OAUTH2_TOKEN_EXCHANGE_URL, headers=headers, data=post_data)
    logging.info(
            'idt oauth2 token refresh response status code: %s, content: %s',
            response.status_code, response.json())
    return response.json()


def get_idt_oauth2_client_id_headers():
    id_str = '%s:%s' % (settings.IDT_OAUTH2_CLIENT_ID, settings.IDT_OAUTH2_CLIENT_SECRET)
    return {'Authorization': 'Basic %s' % b64encode(id_str)}

