from six.moves import urllib
import json
import ssl


class GraphQLClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.token = None

    def execute(self, query, variables=None, verify_ssl=True):
        return self._send(query, variables, verify_ssl)

    def inject_token(self, token):
        self.token = token

    def _send(self, query, variables, verify_ssl):
        data = {'query': query,
                'variables': variables}
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        if self.token is not None:
            headers['Authorization'] = 'Bearer {}'.format(self.token)

        req = urllib.request.Request(
            self.endpoint, json.dumps(data).encode('utf-8'), headers)

        try:
            context = ssl.create_default_context()
            if not verify_ssl:
                context = ssl._create_unverified_context()
            response = urllib.request.urlopen(req, context=context)
            return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            print((e.read()))
            print('')
            raise e
