import google.auth
import google.auth.transport.requests
from google.oauth2 import reauth
from google.oauth2 import _client

import logging
import json
from http.client import HTTPConnection # py3

def debug_requests_on():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

cred, _ = google.auth.default()
req = google.auth.transport.requests.Request()

#===================
# Get the access token for reauth api
#====================

access_token, _, _, _ = _client.refresh_grant(
    request=req,
    client_id=cred._client_id,
    client_secret=cred._client_secret,
    refresh_token=cred._refresh_token,
    token_uri=cred._token_uri,
    scopes=[reauth._REAUTH_SCOPE],
)
print(access_token)

#===================
# call reauth start endpoint
#====================
debug_requests_on()

scopes = ['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/accounts.reauth']
headers = {"Content-Type": _client._JSON_CONTENT_TYPE, "Authorization": f"Bearer {access_token}", "x-goog-api-client":"gl-python/100 grpc/200, gax/200 gapic/200 gccl/200"}
body = {"supportedChallengeTypes": ["SECURITY_KEY", "SAML", "PASSWORD"]}
body["oauthScopesForDomainPolicyLookup"] = scopes
body = json.dumps(body).encode("utf-8")
response = req(
    method="POST", url=reauth._REAUTH_API + ":start", headers=headers, body=body
)
print(response._response)