# # Restriction to a domain. 
# RESTRICT_DOMAIN = True
# REQUIRED_DOMAIN = 'youralloweddomain.com'

# # The secret key is used by Flask to encrypt session cookies.
# SECRET_KEY = 'put a long secret key here'

# # OAuth2 configuration.
# # This can be generated from the Google Developers Console at
# # https://console.developers.google.com/project/_/apiui/credential.
# # Note that you will need to add all URLs that your application uses as
# # authorized redirect URIs. For example, typically you would add the following:
# #
# #  * http://localhost:8080/oauth2callback
# #  * https://<your-app-id>.appspot.com/oauth2callback. (if using google app engine)
# #
# # If you receive a invalid redirect URI error review you settings to ensure
# # that the current URI is allowed.
# GOOGLE_OAUTH2_CLIENT_ID     = 'enter your client id here'
# GOOGLE_OAUTH2_CLIENT_SECRET = 'enter your client secret here'

# config.py
class Config:
    SECRET_KEY = 'YOUR_SECRET_KEY'
    GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'
    GOOGLE_CLIENT_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'
    REDIRECT_URI = 'YOUR_REDIRECT_URI'  # e.g., 'http://localhost:8080/authorize'
    RESTRICT_DOMAIN = True
    REQUIRED_DOMAIN = 'example.com'
