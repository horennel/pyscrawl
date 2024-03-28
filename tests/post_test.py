from pyscrawl import Spider
from pyscrawl import Request, Item


class MyItem(Item):
    title = str
    info = str

    @classmethod
    def file_path(cls):
        return './movie.txt'


class MySpider(Spider):

    def start_requests(self):
        urls = ['https://spa1.scrape.center/api/movie?limit=10&offset=0']
        for url in urls:
            yield Request(url=url, method='post', callback=self.parse_index)

    def parse_index(self, response):
        if response.status_code == 200:
            for infos in response.json['results']:
                url = 'https://spa1.scrape.center/api/movie/%s' % infos['id']
                yield Request(url=url, method='post', callback=self.parse_detail)

            now_offset = int(response.url.split('=')[-1])
            next_offset = now_offset + 10
            if next_offset < 110:
                url = 'https://spa1.scrape.center/api/movie?limit=10&offset=%d' % next_offset
                yield Request(url=url, method='post', callback=self.parse_index)

    def parse_detail(self, response):
        if response.status_code == 200:
            title = response.json['name']
            info = response.json['drama']
            detail = {
                'title': title,
                'info': info,
            }
            yield MyItem(**detail)


if __name__ == '__main__':
    MySpider().crawl()
