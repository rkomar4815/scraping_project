# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import json
from pandas.io.json import json_normalize
from flatten_json import flatten
from scrapy.crawler import CrawlerProcess
from scrapy import selector
from scrapy import signals


class NDSearchSpider(scrapy.Spider):

    def __init__(self, companies=None, company_info=[]):
        self.companies = companies
        self.company_info = company_info

    '''
    from_crawler checks if Spider is finished scraping and runs spider_closed
    to export scraped info to csv
    '''

    @classmethod
    def from_crawler(cls, crawler):
        spider = super(NDSearchSpider, cls).from_crawler(crawler)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def start_requests(self):
        url = 'https://firststop.sos.nd.gov/api/Records/businesssearch'
        body = "{'SEARCH_VALUE': 'x', 'STARTS_WITH_YN': 'true', 'ACTIVE_ONLY_YN': 'true'}"

        return [scrapy.Request(url=url, method='POST',
                               body=body,
                               headers={'Content-Type': 'application/json'},
                               callback=self.companies_parse)]

    def companies_parse(self, response):

        companies = json.loads(response.body.decode()).pop('rows')
        companies = list(companies.values())
        companies = (flatten(company) for company in companies)
        companies = pd.DataFrame(companies).rename(
            columns={'TITLE_0': 'TITLE', 'TITLE_1': 'FILING_TYPE'})

        companies['URLS'] = 'https://firststop.sos.nd.gov/api/FilingDetail/business/' + \
            companies['ID'].map(str) + '/false'
        self.companies = companies

        for url in companies['URLS']:
            yield scrapy.Request(
                url, headers={'Content-Type': 'application/json'},
                callback=self.company_info_parse, meta={'URLS': url})

    def company_info_parse(self, response):

        result = {'URLS': response.meta.get('URLS')}

        response.selector.remove_namespaces()

        response = dict(zip(response.xpath('//LABEL/text()').getall(),
                            response.xpath('//VALUE/text()').getall()))

        result.update(response)

        self.company_info.append(result)

    def spider_closed(self, spider):
        company_info = pd.DataFrame(self.company_info)
        final = company_info.merge(self.companies, on='URLS', how='outer')
        final.to_csv('result.csv')


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(NDSearchSpider)
    process.start()


    
