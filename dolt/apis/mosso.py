from dolt import Dolt
import httplib2

MOSSO_AUTH_URL = "https://auth.api.rackspacecloud.com"

class MossoHttp(object):
    def __init__(self, username=None, api_key=None, version="1.0", http=None, *args, **kwargs):
        self.http = http or httplib2.Http()
        self.username = username
        self.api_key = api_key
        self.version = "1.0"
        self.auth_token = None

    def request(self, uri, method='GET', body=None, headers=None, redirections=5, connection_type=None):
        if not self.auth_token:
            self.initialize_auth_token()
        if not headers:
            headers = {}
        headers['X-Auth-Token'] = self.auth_token
        return self.http.request(uri, method, body, headers, redirections, connection_type)

    def initialize_auth_token(self):
        if self.auth_token:
            return
        url = "%s/v%s" % (MOSSO_AUTH_URL, self.version)
        response, _body = self.http.request(url, headers = {
            'X-Auth-User': self.username,
            'X-Auth-Key': self.api_key,
        })
        # TODO: handle non-204 requests
        self.server_url = response['x-server-management-url']
        self.auth_token = response['x-auth-token']


class MossoServers(Dolt):
    def __init__(self, username, api_key, **kwargs):
        http = MossoHttp(username=username, api_key=api_key)
        super(MossoServers, self).__init__(http=http)

    def get_url(self):
        self._http.initialize_auth_token()
        self._api_url = self._http.server_url
        return super(MossoServers, self).get_url()
