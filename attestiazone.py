import scrapy
from scrapy.crawler import CrawlerProcess
import csv

csv_col = ['label',"contact","styles","country","website"]
csvfile = open('labelbase.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_col)
writer.writeheader()
csvfile.flush()


class labelbase(scrapy.Spider):
    name = "labelbase"

    def start_requests(self):
        for i in range(1,100):
            yield scrapy.Request(url=f'https://labelsbase.net/?latest_release_date_min=2023-01-01&followers_sc_min=100&page={str(i)}')

    def parse(self, response, **kwargs):
        for listing in response.css("div.label-card"):
            yield scrapy.Request(url=listing.css("div.label-card-head-flex a::attr(href)").get(),callback=self.data,meta={'country':listing.css("small span::text").get()})

    def data(self,response):
        item = {}
        item['label'] = response.css("h1.label-name::text").get()
        item['website'] = "".join([f.css("::attr(href)").get() for f in response.css("a") if f.css("::attr(onmousedown)").get() is not None if 'Link Webpage' in f.css("::attr(onmousedown)").get()])
        item['styles'] = "".join([",".join([a.css("::text").get() for a in v.xpath("following-sibling::a") if "/?g=" in a.css("::attr(href)").get()  ])  for v in response.css("div.line-title-block") if v.css("span.line-title-text::text").get() is not None if "Genres" in v.css("span.line-title-text::text").get()])
        for v in response.css("div.line-title-block"):
            if v.css("span.line-title-text::text").get() is not None:
                if "Contacts" in v.css("span.line-title-text::text").get():
                    for index,a in enumerate(v.xpath("following-sibling::a")):
                        try:
                            if "Demo Email" in a.css("a::attr(onmousedown)").get():
                                item['contact'] =a.css("::text").get()
                                break
                        except:
                            pass
                        try:
                            if "Contact Email" in a.css("a::attr(onmousedown)").get():
                                item['contact'] = a.css("::text").get()
                        except:
                            pass
                        try:
                            if "Submission" in a.css("a::attr(onmousedown)").get():
                                if "mailto" in a.css("::attr(href)").get():
                                    item['contact'] = a.css("::text").get()
                                    break
                        except:
                            pass
        item['country'] = response.meta['country']
        writer.writerow(item)
        csvfile.flush()

process = CrawlerProcess({})
process.crawl(labelbase)
process.start()
