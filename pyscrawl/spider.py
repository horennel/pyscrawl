import requests
from pyscrawl.parser import Response, Item, Request


class Spider(object):

    def __init__(self):
        self._requests = []
        self._session = requests.session()

    def _start(self):
        reqs = getattr(self, 'start_requests')
        for r in reqs():
            self._append_request(r)

    def start_requests(self):
        try:
            start_urls = getattr(self, 'start_urls')
        except:
            start_urls = []
        for url in start_urls:
            try:
                parse = getattr(self, 'parse')
                yield Request(url=url, method='get', callback=parse)
            except:
                pass

    def _append_request(self, req):
        self._requests.append(req)

    def crawl(self):
        self._start()
        for request in self._requests:
            try:
                func = getattr(self._session, request.method)
            except AttributeError:
                raise ValueError('Method %s is not implemented' % request.method)
            resp = func(url=request.url, headers=request.headers, data=request.data)
            response = Response(
                url=resp.url,
                method=request.method,
                status_code=resp.status_code,
                headers=resp.headers,
                content=resp.content,
                text=resp.text,
                meta=request.meta
            )
            print('[%s]:%s' % (response.status_code, response.url))
            result = request.callback(response)
            if result is not None:
                for i in request.callback(response):
                    if isinstance(i, Item):
                        pass
                    elif isinstance(i, Request):
                        self._append_request(i)
