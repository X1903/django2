import random
from IP_GET.IP_GET_v_0_3.address_collect import IP_http


# ===================
# 请求头
headers = {
	"User-Agent":
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
}

# =====================================================================================
# address save 地址保存位置
address_save_kdl = './data/kdl/IP_page{}.txt'  # 快代理
address_save_xici = './data/xirui.json'

# 代理地址
proxie = {
	'http': 'http://182.112.203.64:8118',
	'https': 'http://113.89.15.176:8123'
}

IP_max = len(IP_http)

def get_proxie():
	# 如果 max 为零 终止执行
	# 每隔多少秒生成一个 随机数
	random_one = random.randint(0, IP_max)
	http_port = IP_http[random_one][0]
	print(http_port)
	if max == 0:
		proxie = {
			'http': 'http://{}'.format(http_port),
			'https': 'https://{}'.format(http_port),
		}
		print('获取代理IP 失败')
		return proxie
	proxie = {
		'http': 'http://{}'.format(http_port),
		'https': 'https://{}'.format(http_port),
	}
	print('获取代理IP 成功')
	return proxie


url = 'http://www.xicidaili.com/'

# 国内高匿
url_xc_gn = "http://www.xicidaili.com/nn/"
