Simple OAuth2 integration app

* add the app to the INSTALLED_APPS settings
* add urls to the urls configuration `url(r'^', include('oauth2.urls'))`
* define a OAUTH2_APP_POST_AUTHORIZE_VIEW string setting and point to a view in your app
  `OAUTH2_APP_POST_AUTHORIZE_VIEW='core.views.oauth2_token'`
* implement the view defined in the previous step with this signature:
`def oauth2_token(request, service_name, token_data=None, error=None):`
* define clients under oauth2/clients/SERVICENAME.py and define:
  `get_authorize_config` and `token_exchange` methods (see existing clients).
* define a OAUTH2_APP_ENABLED_CLIENTS setting, it should be an array of strings
  indicating the oauth2 clients you want to be enabled
  `OAUTH2_APP_ENABLED_CLIENTS=['idonethis', 'slack ']`
* while registering an OAuth app on a service provider use /oauth2/callback as
  the redirect URI: `https://example.com/oauth2/callback/`


To start the OAuth2 dance, simply point your client to
reverse('oauth2_authorize', kwargs={'service_name': 'SERVICE_NAME'})

After a successful OAuth2 flow, the view you previously configured will be
called.
