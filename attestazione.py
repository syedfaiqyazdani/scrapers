import scrapy
from scrapy.crawler import CrawlerProcess
import csv

csv_col = ['Denominazione', 'Codice Fiscale', 'P. IVA', 'Indirizzo', 'Cap', 'Citta', 'Provincia', 'Regione', 'Categorie', 'Legale Rappresentante', 'Direttore Tecnico', 'Data Scad 3', 'DataScad5', 'Soa']
csvfile = open('attestazione.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile,fieldnames=csv_col)
writer.writeheader()
csvfile.flush()

class attestazione(scrapy.Spider):
    name = "attestazione"

    def start_requests(self):
        yield scrapy.Request(url="https://attestazione.net/SoaEngine?Categoria=&Classifica=&Regione=")

    def parse(self, response, **kwargs):
        for link in response.css("table.table.table-striped.table-hover tbody > tr a.text-info::attr(href)").getall():
            url = 'https://attestazione.net' + link
            yield scrapy.Request(url=url,callback=self.data)

    def data(self,response):
        item = dict()
        for col in response.css("dl.dl-horizontal dt"):
            value = col.xpath("following-sibling::dd")[0].css("::text").get().strip()
            col_name = col.css("::text").get().strip()
            item[col_name] = value
        writer.writerow(item)
        csvfile.flush()


process = CrawlerProcess({})
process.crawl(attestazione)
process.start()
