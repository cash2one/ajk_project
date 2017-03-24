# !/usr/bin/python3
# -*- coding: utf-8 -*-


from scrapy import Spider
from ajk.items import AjkItem
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.exceptions import IgnoreRequest

class AjkSpider(Spider):
	# name = "ajk"
	# start_urls = ('http://bj.xzl.anjuke.com/zu/p'+str(i+1)+'/' for i in range(90))

# 	def parse(self,response):
# 		"""parse first level house info"""
# 		for index,sel in enumerate(response.xpath("//div[@class='list-item']/@link")):
# 			#if index <= 5:   # locking for test
# 			item = AjkItem()
# 			item['url1'] = sel.extract()
# #				item = AjkItem()
# #				item['url1']='http://bj.xzl.anjuke.com/zu/27117959/?pt=2'  # this one has empty value info
# 			yield Request(url=item['url1'],meta={'item':item},callback=self.parse_house)
	name = "ajk"
	allowed_domains = ["bj.xzl.anjuke.com"]
	start_urls = ["http://bj.xzl.anjuke.com/loupan/"]
	def parse(self,response):
		"""parse first level house info"""
		# max_page = response.xpath("//div[@class='bdlis_mid_bana']/ul/li[4]/p/span[2]/text()").split('/')[1]
		page = response.xpath("//div[@class='bdlis_mid_bana']/ul/li[4]/p/span[2]/text()").extract()
		max_page = int(page[0].split('/')[1])
		# max_page = int(max_page)
		for i in range(max_page):
			url = 'http://bj.xzl.anjuke.com/loupan/p' + str(i+1) + '/'
			yield Request(url=url,callback=self.parse_index)

	def parse_index(self,response):
		for index,sel in enumerate(response.xpath("//div[@class='bd_lis_millde']/ul/li/div/h4/a/@href")):
			#if index <= 5:   # locking for test
			item = AjkItem()
			item['url1'] = sel.extract()
			# meta = {
			# 	dont_redirect: True,  # 禁止网页重定向
			# 	handle_httpstatus_list: [301, 302]  # 对哪些异常返回进行处理
			# }

#				item = AjkItem()
#				item['url1']='http://bj.xzl.anjuke.com/zu/27117959/?pt=2'  # this one has empty value info
			yield Request(url=item['url1'],meta={'item':item},callback=self.parse_house)

	def parse_house(self,response):
		""" parse second level house infomation"""
		item = response.meta['item']
		
		# item['house_name'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='fy_info']/ul[1]/li[4]/span[2]/a/text()").extract())
		item['house_name'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='content']/div/h1/text()").extract())
		#item['url1']
		# item['address'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='fy_info']/ul[1]/li[5]/span[2]/text()").extract())
		
		address = self.ifNotEmptyGetIndex(response.xpath("//div[@class='l-top-right']/ul/li[1]/div/span/text()").extract())
		address = ''.join(address)
		if len(address) > 0:
			add = address.split(']')[0]
			item['address'] = add.split('[')[1]
			item['address_detail'] = address.split(']')[1]
			# item['subway'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='fy_info']/ul[1]/li[6]/span[2]/text()").extract())
		else:
			item['address'] = '暂无信息'
			item['address_detail'] = '信息不明'

		item['property_fee'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='l-top-right']/ul/li[3]/div[2]/span/text()").extract())
		# item['building_area'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='fy_info']/ul[2]/li[1]/span[2]/text()").extract())
		# item['floors'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='fy_info']/ul[2]/li[2]/span[2]/text()").extract())
		# item['desk_num'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='fy_info']/ul[2]/li[3]/span[2]/text()").extract())
		# item['property_fee'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='fy_info']/ul[2]/li[4]/span[2]/text()").extract())
		# item['estimate_monthly_fee'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='fy_info']/ul[2]/li[5]/div/p/em/text()").extract())

		house_info = ''.join(response.xpath("//div[@class='l-cblock clearboth situation']/div/div/text()").extract())
		house_info = house_info.split()
		if house_info:
			item['house_info'] = house_info
		else:
			item['house_info'] = 'nothing here'
		# item['building_type'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'item-mod')]/div[contains(@class,'itemCon')]/ul[1]/li[1]/span[2]/text()").extract())
		item['building_type'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='l-top-right']/ul/li[3]/div[1]/span/text()").extract())
		# item['total_floors'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'item-mod')]/div[contains(@class,'itemCon')]/ul[1]/li[2]/span[2]/text()").extract())
		item['total_floors'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='l-top-right']/ul/li[4]/div[2]/span/text()").extract())
		item['finished_month'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='l-top-right']/ul/li[4]/div[1]/span/text()").extract())
		# item['hall_height'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'item-mod')]/div[contains(@class,'itemCon')]/ul[1]/li[4]/span[2]/text()").extract())
		# item['air_condition_type'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'item-mod')]/div[contains(@class,'itemCon')]/ul[1]/li[5]/span[2]/text()").extract())
		# item['parking'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'item-mod')]/div[contains(@class,'itemCon')]/ul[1]/li[6]/span[2]/text()").extract())
		item['open_area'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='l-top-right']/ul/li[2]/div/span/text()").extract())
		# item['area_per_floor'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'item-mod')]/div[contains(@class,'itemCon')]/ul[2]/li[1]/span[2]/text()").extract())	
		# item['property_company'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'item-mod')]/div[contains(@class,'itemCon')]/ul[2]/li[3]/span[2]/text()").extract())
		# item['floor_height'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'item-mod')]/div[contains(@class,'itemCon')]/ul[2]/li[4]/span[2]/text()").extract())
		# item['elevator'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'item-mod')]/div[contains(@class,'itemCon')]/ul[2]/li[5]/span[2]/text()").extract())		
		# item['foreign_related'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'item-mod')]/div[contains(@class,'itemCon')]/ul[2]/li[6]/span[2]/text()").extract())

		#traffic
		# item['train_distance'] = response.xpath("//dl[contains(@class,'train_box')]/dd/div/span/text()").extract()
		# item['plane_distance'] = response.xpath("//dl[contains(@class,'plane_box')]/dd/div/span/text()").extract()

		# item['url2'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'item-mod')]/div[contains(@class,'itemCon')]/preceding-sibling::h3/a/@href").extract()) or \
		# 				self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'p_crumbs')]/a/@href").extract(),index=-1)
		#print("Following url is :".format(item['url2']))   
		if item['url1']:
			return Request(url=item['url1'].replace('loupan','loupan/jiaotong'),
						meta={'item':item},
						callback=self.get_jiaotong_info,
						dont_filter=True
						)
		else:
			return item
		
	# def get_detailed_info(self,response):
	# 	item = response.meta['item']
		
	# 	# item['open_area'] = self.ifNotEmptyGetIndex(response.xpath("//*[contains(@class,'l-info-item')][1]/span/text()").extract())		
	# 	item['info'] = self.ifNotEmptyGetIndex(response.xpath("//*[@class='l-overview-cont']/text()").extract())

	# 	return Request(url=item['url2'].replace('loupan','loupan/jiaotong'),
	# 					dont_filter=True,
	# 					meta={'item':item},
	# 					callback=self.get_jiaotong_info
	# 					)

	def get_jiaotong_info(self,response):
		""" 交通信息"""
		item = response.meta['item']
		item['subway'] = self.ifNotEmptyGetIndex(list(filter(lambda x:x.startswith('地\xa0铁'),response.xpath("//div[@id='content']/div/div[4]/ul/li[3]/text()").extract())))
		item['bus'] = self.ifNotEmptyGetIndex(list(filter(lambda x:x.startswith('公\xa0交'),response.xpath("//div[contains(@class,'jt_mp_zbxx')][1]/ul/li/text()").extract())))
		item['shopping'] = self.ifNotEmptyGetIndex(list(filter(lambda x:x.startswith('商场'),response.xpath("//div[contains(@class,'jt_mp_zbxx')][2]/ul/li/text()").extract())))
		item['bank'] = self.ifNotEmptyGetIndex(list(filter(lambda x:x.startswith('银行'),response.xpath("//div[contains(@class,'jt_mp_zbxx')][2]/ul/li/text()").extract())))
		item['food'] = self.ifNotEmptyGetIndex(list(filter(lambda x:x.startswith('餐饮'),response.xpath("//div[contains(@class,'jt_mp_zbxx')][2]/ul/li/text()").extract())))
		item['hotel'] = self.ifNotEmptyGetIndex(list(filter(lambda x:x.startswith('酒店'),response.xpath("//div[contains(@class,'jt_mp_zbxx')][2]/ul/li/text()").extract())))
		item['market'] = self.ifNotEmptyGetIndex(list(filter(lambda x:x.startswith('超市'),response.xpath("//div[contains(@class,'jt_mp_zbxx')][2]/ul/li/text()").extract())))			

		return Request(url=item['url1'].replace('loupan','loupan/canshu'),
						dont_filter=True,
						meta={'item':item},
						callback=self.get_canshu_info
						)

	def get_canshu_info(self,response):
		""" 参数信息"""
		item = response.meta['item']
		# item['property_fee'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='fy_info']/ul[2]/li[4]/span[2]/text()").extract())
		item['property_company'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[1]/span[1]/text()").extract())
		# item['passenger_ladder'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[1]/span[2]/text()"))
		item['passenger_ladder'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[1]/span[2]/text()").extract())
		item['elevator_type'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[2]/span[2]/text()").extract())
		item['elevator_is_partition'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[3]/span[2]/text()").extract())
		item['air_condition_type'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[3]/span[1]/text()").extract())
		item['air_condition_hours'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[4]/span[1]/text()").extract())
		item['cargo_ladder'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[4]/span[2]/text()").extract())
		item['parking_fee'] = self.ifNotEmptyGetIndex(response.xpath("//div[contains(@class,'det_pag_cent')]/div[contains(@class,'pag_cent_l')]/div[2]/p[5]/span[1]/text()").extract())
		item['net'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[6]/span[1]/text()").extract())
		item['ground_parking'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[5]/span[2]/text()").extract())
		item['under_parking'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[6]/span[2]/text()").extract())
		item['companys'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/div//td[2]/text()").extract())
		item['in_house_peitao'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/p[7]/text()").extract())
		item['protection'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[2]/table//td[2]/text()").extract())

		hall_height = ''.join(response.xpath("//div[@class='pag_cent_l']/div[3]/p[4]/span[2]/text()").extract())
		# print(type(hall_height))
		if hall_height:
			item['hall_height'] = self.ifNotEmptyGetIndex(hall_height)
		else:
			item['hall_height'] = 'Nullll'
		item['property_building'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[3]/p[1]/span[1]/text()").extract())
		item['floor_height'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[3]/p[2]/span[2]/text()").extract())
		item['total_building_area'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[3]/p[3]/span[1]/text()").extract())
		item['net_height'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[3]/p[3]/span[2]/text()").extract())
		item['floor_area'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[3]/p[4]/span[1]/text()").extract())
		item['wall'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[3]/p[5]/span[2]/text()").extract())
		item['structure'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[3]/p[6]/span[1]/text()").extract())
		item['foreign_related'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[3]/p[6]/span[2]/text()").extract())
		item['could_regist'] = self.ifNotEmptyGetIndex(response.xpath("//div[@class='pag_cent_l']/div[3]/p[7]/span/text()").extract())
		return item

	def ifNotEmptyGetIndex(self,item,index=0):
		if item:
			return item[index]
		else:
			return item