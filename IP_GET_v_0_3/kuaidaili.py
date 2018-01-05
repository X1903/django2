import requests
import json
from retrying import retry
from lxml import etree
from IP_GET.IP_GET_v_0_3.setting import headers, address_save_kdl, proxie
from threading import Thread
from queue import Queue


# http://landinghub.visualstudio.com/visual-cpp-build-tools

class KDL_GetAddress:
	def __init__(self):
		# 获取启动url
		self.url = Queue()
		self.html_str = Queue()
		self.data = Queue()
	
	def get_url_list(self, url, startPage, endPage):
		for page in range(startPage, endPage):
			self.url.put(url.format(page))
	
	@retry(stop_max_attempt_number=3)
	def _parse_url(self, url):
		# 重复请求
		response = requests.get(url, headers=headers, proxies=proxie, timeout=5)
		return response.content.decode()
	
	def parse_url(self):
		while True:
			url = self.url.get()
			print(url)
			# 获取数据
			try:
				html_str = self._parse_url(url)
			except:
				html_str = None
			self.html_str.put(html_str)
			self.url.task_done()
	
	def get_response(self):
		while True:
			html_str = self.html_str.get()
			html = etree.HTML(html_str)
			html_str = html.xpath('//tbody//tr')
			if len(html_str) != 0:
				ever_page = []
				for html in html_str:
					data_list = []
					IP = html.xpath('.//td[@data-title="IP"]/text()')[0] if len(
						html.xpath('.//td[@data-title="IP"]/text()')) > 0 else None
					data_list.append(IP)
					Port = html.xpath('.//td[@data-title="PORT"]/text()')[0] if len(
						html.xpath('.//td[@data-title="PORT"]/text()')) > 0 else None
					data_list.append(Port)
					msg = html.xpath('.//td[@data-title="匿名度"]/text()')[0] if len(
						html.xpath('.//td[@data-title="匿名度"]/text()')) > 0 else None
					data_list.append(msg)
					type = html.xpath('.//td[@data-title="类型"]/text()')[0] if len(
						html.xpath('.//td[@data-title="类型"]/text()')) > 0 else None
					data_list.append(type)
					ever_page.append(data_list)
				self.data.put(ever_page)
			else:
				self.data.put(None)
			self.html_str.task_done()
	
	def save(self):
		while True:
			# if len(address_list) - alist_length >30:
			data = self.data.get()
			print(data)
			with open(address_save_kdl.format(0), 'a', encoding='utf-8') as f:
				list = json.dumps(data, ensure_ascii=False)  ## str   ## utf-8
				f.write(list)
				f.write('\n')
			self.data.task_done()
	
	def start(self, startPage, endPage):  # 主逻辑 (url 的循环放在start 中)
		print('启动IP 获取计划')
		thread_list = []
		url = "http://www.kuaidaili.com/free/inha/{}/"
		# 获取url 列表
		Thread_url = Thread(target=self.get_url_list, args=(url, startPage, endPage))
		thread_list.append(Thread_url)
		# 网页数据
		
		Thread_response = Thread(target=self.parse_url)
		thread_list.append(Thread_response)
		
		# 获取返回值
		Thread_data = Thread(target=self.get_response)
		thread_list.append(Thread_data)
		# 保存
		Thread_save = Thread(target=self.save)
		thread_list.append(Thread_save)
		
		for mythread in thread_list:
			# 每隔线程在主线程结束后就结束
			mythread.setDaemon(True)
			mythread.start()
		
		for que in [self.url, self.html_str, self.data]:
			# 队列在主线程结束前结束
			que.join()


if __name__ == '__main__':
	get = KDL_GetAddress()
	get.start(1, 401)
	print('————结束————')
