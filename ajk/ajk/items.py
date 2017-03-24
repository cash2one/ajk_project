# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item
from scrapy.item import Field 


class AjkItem(Item):
	# define the fields for your item here like:
	#name = scrapy.Field()
	house_name = Field()			# 楼盘名
	# url2 = Field()					# 二级网址
	url1 = Field()					# 一级网址
	address = Field()				# 楼盘地址
	address_detail = Field()		# 地址详情
	open_area = Field()				# 开间面积
	building_type = Field()			# 物业类型
	property_fee = Field()			# 物业费
	finished_month = Field()		# 竣工时间
	total_floors = Field()			# 总楼层
	house_info = Field()			# 楼盘概述

	subway = Field()				# 地铁
	bus = Field()					# 公交
	shopping = Field()				# 商场
	bank = Field()					# 银行
	food = Field()					# 餐饮
	hotel = Field()					# 酒店
	market = Field()				# 超市

	property_company = Field()		# 物业管理公司
	air_condition_type = Field()	# 空调类型
	air_condition_hours = Field()	# 空调开放时间
	parking_fee = Field()			# 车位月租金
	net = Field()					# 网络通信
	companys = Field()				# 已入驻企业
	in_house_peitao = Field()		# 楼内配套
	protection = Field()			# 安防系统

	passenger_ladder = Field()		# 客梯数
	elevator_type = Field()			# 电梯品牌
	elevator_is_partition = Field()	# 电梯有无分区设置
	cargo_ladder = Field()			# 货梯数
	ground_parking = Field()		# 地上车位数
	under_parking = Field()			# 地下车位数

	property_building = Field()		# 开发商
	floor_height = Field()			# 标准层高
	total_building_area = Field()	# 总建筑面积
	net_height = Field()			# 净高
	floor_area = Field()			# 标准层面积
	hall_height = Field()			# 大堂层高
	wall = Field()					# 外墙
	structure = Field()				# 结构
	foreign_related = Field()		# 是否涉外
	could_regist = Field()			# 是否可注册






	# house_name = Field()			# 楼盘名
	# url2 = Field()					# 二级网址
	# url1 = Field()					# 一级网址
	# daily_rent = Field()			# 日租金
	# monthly_rent = Field()			# 月租金
	# rate_of_house = Field()			# 得房率
	# address = Field()				# 地址
	# subway = Field()				# 地铁
	# pict = Field()					# 图片

	# building_area = Field()			# 建筑面积
	# floors = Field()				# 楼层
	# desk_num = Field()				# 工位数
	# property_fee = Field()			# 物业费
	# estimate_monthly_fee = Field()	# 预估月支出

	# house_info = Field()			# 房源描述

	# building_type = Field()			# 类型
	# total_floors = Field()			# 总楼层
	# finished_month = Field()		# 竣工时间
	# hall_height = Field()			# 大堂层高
	# air_condition_type = Field()	# 空调类型
	# parking = Field()				# 车位

	# area_per_floor = Field()		# 单层面积
	# property_company = Field()		# 物业公司
	# floor_height = Field()			# 标准层高
	# elevator = Field()				# 电梯
	# foreign_related = Field()		# 是否涉外

	# train_distance = Field()		# 火车站距离
	# plane_distance = Field()		# 飞机场距离

	
	# open_area = Field()				# 开间面积

	# info = Field()					# 楼盘概述

	# bus = Field()					# 公交

	# shopping = Field()				# 商场
	# bank = Field()					# 银行
	# food = Field()					# 餐饮
	# hotel = Field()					# 酒店
	# market = Field()				# 超市

	# elevator_type = Field()			# 电梯品牌
	# elevator_is_partition = Field()	# 电梯有无分区设置
	# air_condition_hours = Field()	# 空调开放时间
	# parking_fee = Field()			# 车位月租金
	# net = Field()					# 网络通信
	# companys = Field()				# 已入驻企业
	# in_house_peitao = Field()		# 楼内配套
	# protection = Field()			# 安防系统

	# property_building = Field()		# 开发商
	# total_building_area = Field()	# 总建筑面积
	# net_height = Field()			# 净高
	# wall = Field()					# 外墙
	# structure = Field()				# 结构
	# could_regist = Field()			# 是否可注册
