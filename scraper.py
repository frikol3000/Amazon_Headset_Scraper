from flask import jsonify
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings


class Scraper:
    def __init__(self, spider, page_lim=1):
        self.output_data = []
        self.is_closed = False
        self.page_lim = page_lim
        self.process = CrawlerRunner(get_project_settings())
        self.spider = spider

    def run_spider(self):
        dispatcher.connect(self._crawler_result, signal=signals.item_scraped)
        self.process.crawl(self.spider, parent=self, page_lim=self.page_lim)

    def _crawler_result(self, item, response, spider):
        self.output_data.append(dict(item))

    def get_output_data(self):
        self.output_data = [dict(t) for t in {tuple(d.items()) for d in self.output_data}]
        return jsonify(self.output_data)

