import requests


class Vk(object):
    __slots__ = ('access_token', 'v')

    def __init__(self, access_token: str, v: str = '5.131'):
        self.access_token, self.v = access_token, v

    def invoke(self, method, values={}):
        url = 'https://api.vk.com/method/' + method
        values['access_token'], values['v'] = self.access_token, self.v
        return requests.get(url, params=values, timeout=5).json()

    def get_api(self):
        return VkApiInvoke(self)


class VkApiInvoke(object):
    __slots__ = ('_vk', '_method')

    def __init__(self, vk, method=None):
        self._vk, self._method = vk, method

    def __getattr__(self, method):
        return VkApiInvoke(
            self._vk,
            (self._method + '.' if self._method else '') + method
        )

    def __call__(self, **kwargs):
        return self._vk.invoke(self._method, kwargs)


class Longpoll():
    @staticmethod
    def listen(vk):
        data = vk.messages.getLongPollServer()['response']
        key, ts = data['key'], data['ts']
        while True:
            params = {'act': 'a_check', 'key': key, 'ts': ts,
                      'wait': 90, 'mode': 2, 'version': 2}
            response = requests.get(
                f'https://{data["server"]}', params=params).json()
            try:
                updates = response['updates']
            except KeyError:
                data = vk.messages.getLongPollServer()['response']
                continue
            ts = response['ts']
            if updates:
                for elem in updates:
                    yield elem
