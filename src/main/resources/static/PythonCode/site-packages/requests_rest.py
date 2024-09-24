from functools import partial

import requests

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'


def url_append(base_url, *args):
    url = base_url.rstrip('/')
    for a in args:
        a = str(a).strip('/')
        if a:
            url += '/' + a
    return url


def prefixed_request(prefix, f, method, url, *args, **kwargs):
    return f(method, url_append(prefix, url), *args, **kwargs)


class Config(object):
    def __init__(self, base_url, session=None, use_tail_slash=False):
        pass


class Client(object):
    def __init__(self, base_url, session=None, use_tail_slash=False, debug=False):
        self.base_url = base_url
        self.session = session
        self.use_tail_slash = use_tail_slash
        self.debug = debug

        if session is None:
            session = requests.Session()

        # self.prefix = url_append(base_url, resource_path)

        session.request = partial(prefixed_request, base_url, session.request)
        self.session = session

    def __call__(self, resource_path):
        return Resource(resource_path, client=self)


class RequestParameter(object):
    def __init__(self, method, url,
                 params=None, data=None, headers=None, cookies=None, files=None,
                 auth=None, timeout=None, allow_redirects=True, proxies=None,
                 hooks=None, stream=None, verify=None, cert=None, json=None):
        self.method = method
        self.url = url
        self.params = params
        self.data = data
        self.headers = headers
        self.cookies = cookies
        self.files = files
        self.auth = auth
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.proxies = proxies
        self.hooks = hooks
        self.stream = stream
        self.verify = verify
        self.cert = cert
        self.json = json

    @property
    def query_string(self):
        query_string = ''
        if self.params:
            query_string = '&'.join([f'{k}={self.params.get(k)}' for k in self.params])
        return query_string


class Resource(object):
    def __init__(self, resource_path, client: Client, parent_resource=None, actions=None):
        self.actions = actions
        self.resource_path = resource_path
        self.client = client
        self.parent_resource = parent_resource

        if self.actions is None:
            self.actions = []

        self.request_parameter: RequestParameter = RequestParameter(GET, '/')

    @property
    def base_url_path(self):
        return self.resource_path.rstrip('/')

    def _copy(self):
        return Resource(self.resource_path, self.client, self.parent_resource)

    def _prepare(self, method, url,
                 params=None, data=None, headers=None, cookies=None, files=None,
                 auth=None, timeout=None, allow_redirects=True, proxies=None,
                 hooks=None, stream=None, verify=None, cert=None, json=None):
        self.request_parameter = RequestParameter(method, url, params=params, data=data, headers=headers,
                                                  cookies=cookies, files=files, auth=auth, timeout=timeout,
                                                  allow_redirects=allow_redirects, proxies=proxies,
                                                  hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
        return self

    def _extract_response(self, response):
        pass

    def make_plural_action(self, action_name, method=POST):
        method = method  # The method is 'POST' usually
        url = f'{self.base_url_path}/{action_name}'
        if self.client.use_tail_slash:
            url += '/'

        def action(data=None, **kwargs):
            return self._copy()._prepare(method, url, data=data, **kwargs)

        action.__name__ = action_name

        return action

    def make_single_action(self, action_name, method=POST):
        method = method  # The method is 'POST' usually

        def action(id, data=None, **kwargs):
            url = f'{self.base_url_path}/{id}/{action_name}'
            if self.client.use_tail_slash:
                url += '/'

            return self._copy()._prepare(method, url, data=data, **kwargs)

        action.__name__ = action_name

        return action

    def list(self, **kwargs):
        '''GET /xxx/'''
        method = GET
        url = self.base_url_path
        if self.client.use_tail_slash:
            url += '/'
        return self._copy()._prepare(method, url, params=kwargs)

    def create(self, data=None, **kwargs):
        '''POST /xxx/'''
        method = POST
        url = self.base_url_path
        if self.client.use_tail_slash:
            url += '/'
        return self._copy()._prepare(method, url, data=data, **kwargs)

    def detail(self, id, **kwargs):
        '''GET /xxx/:id'''
        method = GET
        url = f'{self.base_url_path}/{id}'
        return self._copy()._prepare(method, url, **kwargs)

    def update(self, id, data=None, **kwargs):
        '''PUT /xxx/:id'''
        method = PUT
        url = f'{self.base_url_path}/{id}'
        return self._copy()._prepare(method, url, data=data, **kwargs)

    def partial_update(self, id, data=None, **kwargs):
        '''PATCH /xxx/:id'''
        method = PATCH
        url = f'{self.base_url_path}/{id}'
        return self._copy()._prepare(method, url, data=data, **kwargs)

    def delete(self, id, **kwargs):
        '''DELETE /xxx/:id'''
        method = DELETE
        url = f'{self.base_url_path}/{id}'
        return self._copy()._prepare(method, url, **kwargs)

    @property
    def response(self):
        p = self.request_parameter
        if self.client.debug:
            full_url = f'{self.client.base_url.rstrip("/")}/{p.url}'.rstrip('/')
            s = f'{p.method} {full_url}'
            if p.query_string:
                s += f'?{p.query_string}'
            if p.data:
                s += f'\n{p.data}'
            print(s)

        return self.client.session.request(
            p.method, p.url,
            params=p.params, data=p.data, headers=p.headers, cookies=p.cookies, files=p.files,
            auth=p.auth, timeout=p.timeout, allow_redirects=p.allow_redirects, proxies=p.proxies,
            hooks=p.hooks, stream=p.stream, verify=p.verify, cert=p.cert, json=p.json
        )

    def __call__(self, subresource: 'Resource'):
        resource_path = '/'.join([
            self.request_parameter.url,
            subresource.resource_path
        ])
        return Resource(resource_path, client=self.client, parent_resource=self)


if __name__ == '__main__':
    # base_url = 'http://localhost:8001/'
    base_url = 'https://httpbin.org/'

    new_name = 'aponder'
    new_email = 'i@aponder.top'
    new_user = {
        'name': new_name,
        'email': new_email,
    }
    update_user = new_user.copy()
    update_user.update({'name': f'new {new_name}'})

    # print(resource_user.list().json())
    # print(resource_user.create(new_user).json())
    # print(resource_user.update(1, new_user).json())
    # print(resource_user.patch(1, new_name).json())
    # print(resource_user.patch(1, new_email).json())
    # print(resource_user.delete(1).json())

    resource_client = Client(base_url, debug=True)
    Users = resource_client('users')

    users_creating = Users.create(new_user)
    print(users_creating.response)

    users_listing = Users.list(page=1, page_size=10)
    print(users_listing.response)

    users_detailing = Users.detail(1)
    print(users_detailing.response)

    users_updating = Users.update(2, update_user)
    print(users_updating.response)

    users_partial_updating = Users.partial_update(3, update_user)
    print(users_partial_updating.response)

    users_deleting = Users.delete(4)
    print(users_deleting.response)

    # extra actions
    Users.login = Users.make_plural_action('login')
    credentials = {'username': 'root', 'password': 'root'}
    print(Users.login(credentials).response)

    Users.disable = Users.make_single_action('disable')
    print(Users.disable(2).response)

    Users.copy = Users.make_single_action('copy')
    print(Users.copy(2).response)
    Users.prepare = Users.make_single_action('prepare')
    print(Users.prepare(2).response)

    # resource combination
    Blogs = resource_client('blogs')
    UsersBlogs = users_detailing(Blogs)

    new_blog = {'title': 'hello'}
    print(UsersBlogs.create(new_blog).response)
    print(UsersBlogs.list(page=2, page_size=20).response)
    print(UsersBlogs.delete(10).response)
    print(UsersBlogs.update(10, new_blog).response)
    print(UsersBlogs.partial_update(10, new_blog).response)
    print(UsersBlogs.delete(10).response)
