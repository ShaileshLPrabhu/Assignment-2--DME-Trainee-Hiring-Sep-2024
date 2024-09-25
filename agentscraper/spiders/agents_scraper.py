import scrapy
import csv
import json


class BhSpider(scrapy.Spider):
    name = 'agentscraper'
    start_urls = ['https://www.bhhsamb.com/roster/Agents']
    
    def parse(self, response):
        # Extracting profile links of each agent
        profile_links = response.xpath('/html/body/div[1]/section/div[6]/article[1]/a/@href').getall()
        for url in profile_links:
            yield response.follow(url,self.parse_agent)

    def parse_agent(self, response):
        # Extracting Agent details using xpath
        addressline1 =response.xpath('/html/body/div[1]/section/article[1]/ul[3]/li/strong/text()').get(default=' ').strip()
        addressline2 =response.xpath('/html/body/div[1]/section/article[1]/ul[3]/li/text()').get(default=' ').strip()
        address = (addressline1 +','+addressline2).strip()
        data = {
            'name': response.xpath('/html/body/div[1]/section/article[1]/p').get(default=' ').strip(),
            'job_title': response.xpath('/html/body/div[1]/section/article[1]/p/span/text()').get(default=' ').strip(),
            'image_url': response.xpath('/html/body/div[1]/section/article[1]/img/@src').get(default=' ').strip(),
            'address': address,
            'phone':response.xpath('/html/body/div[1]/section/article[1]/ul[1]/li[1]/a/text()').get(default=' ').strip(),
            'description':response.xpath('/html/body/div[1]/section/article[2]/div[1]/p/text()').get(default='Empty Description').strip(),
            'website':response.xpath('/html/body/div[1]/section/article[1]/ul[2]/li[1]/a/@href').get(default='Link not available').strip()
        }

        self.save_data(data)
    
    #saving data to json & csv
    def save_data(self, data):
        with open('agents.json', 'a') as json_file:
            json.dump(data, json_file)
            json_file.write('\n')  

        with open('agents.csv', 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data.keys())
            writer.writerow(data)