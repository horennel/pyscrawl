from pyscrawl import Spider
from pyscrawl import Request, Item


class MyItem(Item):
    title = str
    info = str
    score = float

    @classmethod
    def file_path(cls):
        return './movie.txt'


class MySpider(Spider):
    start_urls = ['https://ssr1.scrape.center/']

    def parse(self, response):
        if response.status_code == 200:
            detail_urls = response.xpath('//a[@class="name"]/@href')
            for detail_url in detail_urls:
                url = 'https://ssr1.scrape.center%s' % detail_url
                yield Request(url=url, method='get', callback=self.parse_detail)

            next_page = response.xpath('//a[@class="next"]/@href')[0]
            url = 'https://ssr1.scrape.center%s' % next_page
            yield Request(url=url, method='get', callback=self.parse)

    def parse_detail(self, response):
        if response.status_code == 200:
            title = response.xpath('//h2[@class="m-b-sm"]/text()')[0]
            info = response.xpath('//div[@class="drama"]/p/text()')[0].strip()
            score = float(response.xpath('//p[@class="score m-t-md m-b-n-sm"]/text()')[0].strip())
            detail = {
                'title': title,
                'info': info,
                'score': score,
            }
            yield MyItem(**detail)


if __name__ == '__main__':
    MySpider().crawl()
