import requests

class Auth:
    def __init__(self, host, username, password):
        self._host = host
        self._auth_request = {'username':username, 'password':password}

    def login(self):
        target = 'http://{}/jams/api/authentication/login'.format(self._host)
        r = requests.post(target, data = self._auth_request)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        self._auth_response = r.json()


    def host(self):
        return self._host

    def access_token(self):
        return self._auth_response['access_token']

    def header(self):
        return {'Authorization': 'bearer {}'.format(self.access_token())}

