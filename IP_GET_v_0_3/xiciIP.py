from IP_GET.IP_GET_v_0_1.static_code import RE_IP, RE_PORT
from IP_GET.IP_GET_v_0_1.setting import headers, url, address_save_xici
import re
import json
import requests

data = requests.get(url, headers=headers).content.decode()

reStr = r"""<td>({}\.{}\.{}\.{})</td>\n\s*<td>({})</td>\n\s*<td>.*</td>\n\s*<td class="country">(.*)</td>\n\s*<td>(.*)</td>\n""".format(
	RE_IP, RE_PORT, RE_IP, RE_IP, RE_PORT)
tablelist = re.findall(reStr, data)
with open(address_save_xici, 'w', encoding='utf-8') as f:
	rdata = json.dumps(tablelist, ensure_ascii=False, indent=2)
	f.write(rdata)
