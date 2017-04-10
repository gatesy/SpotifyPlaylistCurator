# This contains the OAuth related stuff we need to use the Spotify API

import requests
import json
from datetime import datetime, timedelta
from base64 import b64encode

class ClientCredentials:
    """Instances of this class maintain the client credentials access token"""
    
    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self.token = None
        self.expires = datetime.min # expiry time, stored in UTC

    def get_token(self):
        """Get the current access token, or if there isn't one (or it's expired) request a new one"""
        if self.token is None or self.has_token_expired():
            # Get the auth value and encode it in base 64.
            client_id_secret = b64encode(bytes('{}:{}'.format(self._client_id, self._client_secret), 'utf-8')).decode('utf-8')

            auth_request = requests.post(
                'https://accounts.spotify.com/api/token',
                headers={
                    'Authorization': 'Basic {}'.format(client_id_secret),
                    'Content-Type': 'application/x-www-form-urlencoded'},
                data='grant_type=client_credentials')
            auth = json.loads(auth_request.content)

            self.token = auth['access_token']
            self.expires = datetime.utcnow() + timedelta(seconds=auth['expires_in'])
            print('Successfully acquired application bearer token. Expires at {}'.format(self.expires))
            
        return self.token

    def has_token_expired(self):
        """Check to see if the existing token has expired"""
        return self.expires - datetime.utcnow() <= timedelta()
    