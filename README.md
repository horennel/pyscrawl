## A simple crawler implementation

- install
```angular2html
python3 setup.py install
```

- use
```python
from pyscrawl import Spider
from pyscrawl import Request, Item


class MyItem(Item):

    @classmethod
    def file_path(cls):
        return ''


class MySpider(Spider):
    start_urls = []

    def parse(self, response):
        pass

    def parse_detail(self, response):
        pass


if __name__ == '__main__':
    MySpider().crawl()

```