import requests


class VkApiError(Exception):
    def __init__(self, error):
        self.error = error
        super().__init__(self.error)


class Vk(object):
    __slots__ = ('access_token', 'v')

    def __init__(self, access_token: str, v: str = '5.131'):
        self.access_token, self.v = access_token, v

    def invoke(self, method, values={}):
        url = 'https://api.vk.com/method/' + method
        values |= {'access_token': self.access_token, 'v': self.v}
        resp = requests.get(url, params=values, timeout=5).json()
        if 'error' in resp:
            raise VkApiError(resp)
        return resp['response']

    def get_api(self):
        return VkApiInvoke(self)


class VkApiInvoke(object):
    __slots__ = ('_vk', '_method')

    def __init__(self, vk, method=None):
        self._vk, self._method = vk, method

    def __getattr__(self, method):
        return VkApiInvoke(self._vk,
                           (self._method + '.' if self._method else '') + method)

    def __call__(self, **kwargs):
        return self._vk.invoke(self._method, kwargs)


class Longpoll():
    __slots__ = ('vk', 'group_id', 'key', 'server', 'ts', 'url', 'session')

    def __init__(self, vk: Vk, group_id: str = None):
        self.vk = vk
        self.group_id = group_id if group_id else None
        self.session = requests.Session()
        self.update()

    def update(self) -> None:
        values = {'group_id': self.group_id} if self.group_id else {}
        response = self.vk.invoke('groups.getLongPollServer' if self.group_id else
                                  'messages.getLongPollServer', values)

        self.key = response['key']
        self.server = response['server']
        self.ts = response['ts']
        self.url = self.server if self.group_id else 'https://' + self.server

    def check(self) -> list:
        params = {'act': 'a_check', 'key': self.key, 'ts': self.ts, 'wait': 90}
        if not self.group_id:
            params['mode'], params['version'] = 2, 2
        response = self.session.get(self.url, params=params).json()

        if 'failed' not in response:
            self.ts = response['ts']
            return response['updates']
        elif response['failed'] == 1:
            self.ts = response['ts']
        else:
            self.update()
        return []

    def listen(self):
        while True:
            for event in self.check():
                yield event
