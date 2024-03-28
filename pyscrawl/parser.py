import json
from lxml import etree


class Response(object):
    def __init__(self, url, method, text, status_code, content, headers, meta):
        self.url = url
        self.status_code = status_code
        self.content = content
        self.headers = headers
        self.method = method
        self.text = text
        if self.method == "post":
            self.json = self._to_json()
        else:
            self.json = None
        self.html = etree.HTML(content)
        self.meta = meta

    def _to_json(self):
        try:
            return json.loads(self.text)
        except Exception as e:
            return None

    def xpath(self, x_str):
        return self.html.xpath(x_str)


class Request(object):
    def __init__(self, method, url, headers=None, callback=None, data=None, meta=None):
        self.headers = headers
        self.method = method
        self.url = url
        self.data = data
        self.callback = callback
        self.meta = meta


class Item(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            print('open file：%s' % cls.file_path())
            cls._file = open(cls.file_path(), 'a')
        return cls._instance

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            pass
        self._file.write(json.dumps(kwargs, ensure_ascii=False) + '\n')

    def __del__(self):
        print("close file：%s" % self.file_path())
        self._file.close()
