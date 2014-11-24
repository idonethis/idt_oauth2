from django import test

import responses
import json

from core import models
from oauth2.clients import idonethis


class ClientIdonethisTest(test.TestCase):
    @responses.activate
    def test_token_refresh(self):
        api_response_body = json.dumps({
            'access_token': 'foo-access-token',
            'token_type': 'foo-token-type',
            'refresh_token': 'foo-refresh-token',
            'scope': 'foo-scope',
            'expires_in': 3600,
        })

        responses.add(responses.POST, 'http://localhost/fake/idonethis/api/oauth2/token/',
                        body=api_response_body, status=200,
                        content_type='application/json')
        idonethis.token_refresh('foo-token')
        self.assertEquals(1, len(responses.calls))
        self.assertEquals('http://localhost/fake/idonethis/api/oauth2/token/', 
                responses.calls[0].request.url)
