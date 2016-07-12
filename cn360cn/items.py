# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Cn360cnItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    company = Field()
    description = Field()
    contact_person = Field()
    name = Field()
    sex = Field()
    position = Field()
    phone = Field()
    fax = Field()
    email = Field()
    address = Field()
    zip_code = Field()
    website = Field()
    business = Field()
    QQ = Field()


