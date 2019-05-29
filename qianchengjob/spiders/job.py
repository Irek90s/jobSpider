# -*- coding: utf-8 -*-
import scrapy


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['51job.com']
    # start_urls = ['https://search.51job.com/list/020000,000000,0000,00,9,99,%2520,2,1.html']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,%2520,2,1.html']

    def parse(self, response):
        # 获取列表
        job_list = response.xpath("//div[@id='resultList']/div[@class='el']")
        # print(job_list)
        # print(len(job_list))
        # print(job_list)
        for job in job_list:
            item = {}
            item["detail_url"] = job.xpath("./p/span/a/@href").extract_first()
            item["job_name"] = job.xpath("./p/span/a/@title").extract_first()
            item["company"] = job.xpath("./span[@class='t2']/a/@title").extract_first()
            item["work_place"] = job.xpath("./span[@class='t3']/text()").extract_first()
            item["salary"] = job.xpath("./span[@class='t4']/text()").extract_first()
            item["publish_date"] = job.xpath("./span[@class='t5']/text()").extract_first()
            # print(item)
            if item["detail_url"] is not None:
                yield scrapy.Request(
                    item["detail_url"],
                    callback=self.parse_detail,
                    meta={"item":item}
                )
        next_url = response.xpath(".//a[text()='下一页']/@href").extract_first()
        # 翻页
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["fuli"] = response.xpath(".//div[@class='jtag']/div/span/text()").extract()
        # print(item)
        yield item
