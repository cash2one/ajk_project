# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from ajk.dbconnect import connection,connectionServer
from bs4 import BeautifulSoup
import re


cur,conn = None,None

class AjkPipeline(object):

	def __init__(self):
		self.setupDBCon()
		self.createTable()

	def process_item(self, item, spider):
		for key, value in item.items():
			# handle list and useless html tag
			if (isinstance(value,list)):
				if value:
					templist =[]
					for obj in value:
						temp =self.stripHTML(obj) # rid of useless tag
						templist.append(temp)
						templist = [i.strip() for i in templist if i]
					item[key] = templist
				else:
					item[key]=""
			else:
				item[key]= self.stripHTML(value)


		self.storeInDb(item)   #comment here to see result
		return item

	def setupDBCon(self):
		self.cur, self.conn = connection()
		# self.conn.set_charset('utf8')
		# self.cur.execute('SET NAMES utf8;')
		# self.cur.execute('SET CHARACTER SET utf8;')
		# self.cur.execute('SET character_set_connection=utf8;')		

	def createTable(self):
		self.cur.execute("""DROP TABLE IF EXISTS `Ajk_Loupan3`""")
		self.cur.execute("""CREATE TABLE IF NOT EXISTS `Ajk_Loupan3`(id INT NOT NULL AUTO_INCREMENT,\
			house_name VARCHAR(255) default NULL COMMENT '楼盘名',\
			url1 VARCHAR(255) default NULL COMMENT '网址',\
			address VARCHAR(255) default NULL COMMENT '地址区域',\
			address_detail VARCHAR(255) default NULL COMMENT '地址详情',\
			subway VARCHAR(255) default NULL COMMENT '地铁',\
			property_fee VARCHAR(255) default NULL COMMENT '物业费',\
			house_info TEXT default NULL COMMENT '楼盘概述',\
			building_type VARCHAR(255) default NULL COMMENT '物业类型',\
			total_floors VARCHAR(255) default NULL COMMENT '总楼层',\
			finished_month VARCHAR(255) default NULL COMMENT '竣工时间',\
			hall_height VARCHAR(255) default NULL COMMENT '大堂层高',\
			air_condition_type VARCHAR(255) default NULL COMMENT '空调类型',\
			ground_parking VARCHAR(255) default NULL COMMENT '地上车位',\
			under_parking VARCHAR(255) default NULL COMMENT '地下车位',\
			parking_fee VARCHAR(255) default NULL COMMENT '车位月租金',\
			property_company VARCHAR(255) default NULL COMMENT	'物业管理公司',\
			floor_height VARCHAR(255) default NULL COMMENT	'标准层高',\
			floor_area VARCHAR(255) default NULL COMMENT	'标准层面积',\
			passenger_ladder VARCHAR(255) default NULL COMMENT	'客梯数',\
			cargo_ladder VARCHAR(255) default NULL COMMENT	'货梯数',\
			foreign_related VARCHAR(255) default NULL COMMENT '是否涉外',\
			open_area VARCHAR(255) default NULL COMMENT	'开间面积',\
			bus VARCHAR(255) default NULL COMMENT	'公交',\
			shopping VARCHAR(255) default NULL COMMENT	'商场',\
			bank VARCHAR(255) default NULL COMMENT	'银行',\
			food VARCHAR(255) default NULL COMMENT	'餐饮',\
			hotel VARCHAR(255) default NULL COMMENT	'酒店',\
			market VARCHAR(255) default NULL COMMENT '超市',\
			elevator_type VARCHAR(255) default NULL COMMENT		'电梯品牌',\
			elevator_is_partition VARCHAR(255) default NULL COMMENT	'电梯有无分区设置',\
			air_condition_hours VARCHAR(255) default NULL COMMENT	'空调开放时间',\
			net VARCHAR(255) default NULL COMMENT	'网络通信',\
			companys TEXT default NULL COMMENT	'已入驻企业',\
			in_house_peitao VARCHAR(255) default NULL COMMENT '楼内配套',\
			protection VARCHAR(255) default NULL COMMENT '安防系统',\
			property_building VARCHAR(255) default NULL COMMENT	'开发商',\
			total_building_area VARCHAR(255) default NULL COMMENT '总建筑面积',\
			net_height VARCHAR(255) default NULL COMMENT	'净高',\
			wall VARCHAR(255) default NULL COMMENT	'外墙',\
			structure VARCHAR(255) default NULL COMMENT	'结构',\
			could_regist VARCHAR(255) default NULL COMMENT	'是否可注册',\
			PRIMARY KEY (id)\
			)""")

	def storeInDb(self,item):
		# try:
		# print(item.get('ground_parking'))
		self.cur.execute("""INSERT INTO `Ajk_Loupan3`(
		`house_name`,\
		`url1`,\
		`address`,\
		`address_detail`,\
		`subway`,\
		`property_fee`,\
		`house_info`,\
		`building_type`,\
		`total_floors`,\
		`finished_month`,\
		`hall_height`,\
		`air_condition_type`,\
		`ground_parking`,\
		`under_parking`,\
		`parking_fee`,\
		`property_company`,\
		`floor_height`,\
		`floor_area`,\
		`passenger_ladder`,\
		`cargo_ladder`,\
		`foreign_related`,\
		`open_area`,\
		`bus`,\
		`shopping`,\
		`bank`,\
		`food` ,\
		`hotel`,\
		`market`,\
		`elevator_type`,\
		`elevator_is_partition`,\
		`air_condition_hours`,\
		`net`,\
		`companys`,\
		`in_house_peitao`,\
		`protection`,\
		`property_building`,\
		`total_building_area` ,\
		`net_height`,\
		`wall`,\
		`structure`,\
		`could_regist`)	
		VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
				%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
				%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
				%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
				%s)""",
		(
		item.get('house_name'),
		item.get('url1'),
		item.get('address'),
		item.get('address_detail'),
		item.get('subway'),
		item.get('property_fee'),
		item.get('house_info')[0],
		item.get('building_type'),
		item.get('total_floors'),
		item.get('finished_month'),
		item.get('hall_height'),
		item.get('air_condition_type'),
		item.get('ground_parking'),
		item.get('under_parking'),
		item.get('parking_fee'),
		item.get('property_company'),
		item.get('floor_height'),
		item.get('floor_area'),
		item.get('passenger_ladder'),
		item.get('cargo_ladder'),
		item.get('foreign_related'),
		item.get('open_area'),
		item.get('bus'),
		item.get('shopping'),
		item.get('bank'),
		item.get('food'),
		item.get('hotel'),
		item.get('market'),
		item.get('elevator_type'),
		item.get('elevator_is_partition'),
		item.get('air_condition_hours'),
		item.get('net'),
		item.get('companys'),
		item.get('in_house_peitao'),
		item.get('protection'),
		item.get('property_building'),
		item.get('total_building_area'),
		item.get('net_height'),
		item.get('wall'),
		item.get('structure'),
		item.get('could_regist')
		))

		self.conn.commit()
		# except Exception as e:
		# 	print(e)
		# 	print(self.cur._last_executed)

	# def cleanPrice(self,string):
	# 	"""extract only number from price string"""
	# 	if string not in ["Null","\r","-",'']:
	# 		return re.search(r'[0-9]+',string).group()
	# 	else:
	# 		return string

	# def cleanEmpty(self,string,default=None):
	# 	return string if string else default

	def stripHTML(self,string):
		soup = BeautifulSoup(string,"lxml")
		return soup.get_text()
		# string_without_escape = string.strip('\n\t ')
		# tagStripper = MLStripper()
		# tagStripper.feed(string_without_escape)
		# return tagStripper.get_data()

	def __del__(self):
		self.closeDB()

	def closeDB(self):
		self.conn.close()

# from html.parser import HTMLParser#
# class MLStripper(HTMLParser):
# 	"""receive a string which has useless html tag and return another string without tag
# 	"""
# 	def __init__(self):
# 		super().__init__()
# 		self.reset()
# 		self.fed=[]
# 	def handle_data(self,d):
# 		self.fed.append(d)
# 	def get_data(self):
# 		return ''.join(self.fed)