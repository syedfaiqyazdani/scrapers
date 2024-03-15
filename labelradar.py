import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import json

csv_col = ['label',"contact","styles","country"]
csvfile = open('labelradar.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_col)
writer.writeheader()
csvfile.flush()

class labelradar(scrapy.Spider):
    name = "labelradar"

    def start_requests(self):
        for i in range(13):
            yield scrapy.Request(url=f'https://api.labelradar.com/v1/labels?page={str(i)}&query=&pageSize=50&includeGenreParents=true&sortBy=most_fans&genres=75,34,61,35,49')


    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        for listing in data['content']:
            item = {}
            item['label'] = listing['fullname']
            item['contact'] =listing['website']
            item['styles'] =",".join([v['name'] for v in listing['acceptingGenres']])
            item['country'] =listing['location']
            writer.writerow(item)
            csvfile.flush()

process = CrawlerProcess({})
process.crawl(labelradar)
process.start()
s