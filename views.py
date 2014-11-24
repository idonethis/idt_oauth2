from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse

import string
import random
import urllib
import importlib


def oauth2_authorize(request, service_name):
    redirect_uri = request.build_absolute_uri(reverse('oauth2_callback'))

    client = get_oauth2_client(service_name)
    service_url, query_params = client.get_authorize_config(redirect_uri)

    random_state_string = generate_random_state_string()

    request.session['oauth2_state'] = random_state_string
    request.session['oauth2_service_name'] = service_name

    query_params['state'] = random_state_string
    query_params['response_type'] = 'code'

    url = '%s?%s' % (service_url, urllib.urlencode(query_params))

    return redirect(url)


def generate_random_state_string():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])


def oauth2_callback(request):
    post_oauth2_callback = load_view(settings.OAUTH2_APP_POST_AUTHORIZE_VIEW)

    try:
        service_name = None
        if 'error' in request.GET or 'error_reason' in request.GET:
            raise OAuth2FlowError
        if request.session['oauth2_state'] != request.GET['state']:
            raise OAuth2StateMismatchError
        service_name = request.session['oauth2_service_name']
    except (KeyError, OAuth2StateMismatchError, OAuth2FlowError), e:
        return post_oauth2_callback(request, service_name, error=True)
    finally:
        # Clean up all session vars without failing.
        try:
            del request.session['oauth2_service_name']
            del request.session['oauth2_state']
        except KeyError:
            pass

    client = get_oauth2_client(service_name)

    redirect_uri = request.build_absolute_uri(reverse('oauth2_callback'))

    token_data = client.token_exchange(request.GET['code'], redirect_uri)

    return post_oauth2_callback(request, service_name, token_data=token_data)


def get_oauth2_client(service_name):
    try:
        if service_name not in settings.OAUTH2_APP_ENABLED_CLIENTS:
            raise OAuth2ClientNotEnabled()

        client_name = "idt_oauth2.clients.%s" % service_name
        return importlib.import_module(client_name)
    except ImportError, e:
        raise raise_404_or_devfriendly_exception(e)


def load_view(name):
    package, method = name.rsplit('.', 1)

    module = importlib.import_module(package)
    return getattr(module, method)


def raise_404_or_devfriendly_exception(e):
    if settings.DEBUG:
        raise e
    else:
        raise Http404


class OAuth2StateMismatchError(Exception):
    pass


class OAuth2FlowError(Exception):
    pass


class OAuth2ClientNotEnabled(Exception):
    pass


def fake_oauth2_authorize(request, service_name):
    service_url = reverse('oauth2_callback')
    query_params = {
        'state': request.GET['state'],
        'code': ('fake-%s-code' % service_name),
    }
    url = '%s?%s' % (service_url, urllib.urlencode(query_params))
    return redirect(url)
