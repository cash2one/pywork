# -*- coding: utf-8 -*- 
import urllib2,json,re,threading,Queue,csv,random
from urlparse import urlparse
import socket
import time
import datetime


uaList = [
        'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI 4LTE Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 XiaoMi/MiuiBrowser/2.1.1',
        'Mozilla/5.0 (iPhone 5CGLOBAL; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/6.0 MQQBrowser/5.8 Mobile/12F70 Safari/8536.25',
        'Mozilla/5.0 (Linux; Android 4.0.3; M031 Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a UCBrowser/9.3.1.339 Mobile',
        'Mozilla/5.0 (Linux; U; Android 4.1.1; zh-CN; M040 Build/JRO03H) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.4.1.362 U3/0.8.0 Mobile Safari/533.1',
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
		"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
		"Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)",
		"Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62",
		"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64",
		"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1",
		"IE 7 ? Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR",
		"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1",
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
		"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; 360SE)",
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon/3.0)",
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; TencentTraveler 4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) )",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
		"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
		"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
		"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; 360SE)"
    ]

class Checking(threading.Thread):
	def __init__(self, queue, avail):
		super(Checking, self).__init__()
		self.queue = queue
		self.avail = avail
		self.yellowword = []
		fo = open('yellow.txt','r+')
		for line in fo:
			self.yellowword.append(line.strip('\n'))


	def run(self):
		while True:
			domain = self.queue.get()
			archiveurls = self.geturls(domain)
			print len(archiveurls)
			rs1 = domain + ' count:'+str(len(archiveurls))+' '
			for aurl in archiveurls:
				print aurl
				sr = self.check_arc(aurl)
				yeword = unicode('yellow', "utf-8")
				rs = rs1 + sr
				if yeword in sr:
					self.avail.writerow([rs])
					break
			else:
				self.avail.writerow([rs])
			self.queue.task_done()


			
	def geturls(self,domain):
		times = ['20080601000000','20090601000000','20100601000000','20110601000000','20120601000000','20130601000000','20140601000000','20150601000000','20160601000000']
		archiveurls = []
		for tm in times:
			myUrl = "https://web.archive.org/web/"+tm+"*/http://{}".format(domain)
			print myUrl
			#print myUrl
			try:
				req = urllib2.Request(myUrl)
				myResponse = urllib2.urlopen(req)
				myPage = myResponse.read()
				unicodePage = myPage.decode("utf-8")
				arc_link = re.search('<div class="month".*?>(.*?)<div id="wbCalNote">',unicodePage,re.S)
				arc_link = arc_link.group(0)
				urls = re.findall(u'<a.*?href="(.*?)".*?>(.*?)</a>',arc_link,re.S)
				for url in urls:
					aurl ='https://web.archive.org'+url[0]
					archiveurls.append(aurl)
			except:
				print '123'
				break
		archiveurls = list(set(archiveurls))
		return archiveurls




	# 查询域名是否可注册
	def check_arc(self, aurl):
		#query = "http://m.tq1.uodoo.com/s?q={}&from=smor&safe=1&by=submit&snum=6".format(hotword)
		ua = random.choice(uaList)
		headers = {
			'Host': 'archive.org',
			'Referer': 'https://archive.org',
			'User-Agent': ua,
		}
		try:
			result = 'OK'
			if aurl:
				print aurl
				#reqcheck = urllib2.Request(checkurl,'',headers)
				resultchk = urllib2.urlopen(aurl).read()
				dr = re.compile(r'<[^>]+>',re.S)
				resultchk = dr.sub('',resultchk)
				resultchk = unicode(resultchk, "utf-8")
				words = self.yellowword
				for word in words:
					word = unicode(word, "utf-8")
					if word in resultchk:
						result = 'yellowurl '+aurl
						print result
						break

		except Exception as e:
			#print "error",e
			available = 'error'
		else:
			available = result
			#available = rs
		return available


	# 查询域名的sogou rank
	def check_sr(self, domain):
		url = 'https://www.sogou.com/sogourank?ur=http%3A%2F%2Fwww.{0}%2F'.format(domain)
		try:
			r = urllib2.urlopen(url).read().strip()[-1]
		except Exception:
			r = "error"
		return r


def main():
	today = datetime.date.today()
	today = today.strftime("%Y-%m-%d")
	domain_file = open('domain.txt')
	#domain.txt 为域名文件，每行一个域名，不要有www或者是http这些，只留域名的主体和后缀，如：baidu.com
	avail = open('domain_chk.txt','ab+') # avail.csv为导出的结果文件，生成在当前脚本文件所在目录
	#fields = ["相关搜索"]
	fields = [today]
	w = csv.writer(avail)

	queue = Queue.Queue()
	for domain in domain_file:
		domain = domain.strip()
		queue.put(domain)

	print queue.qsize()


	
	for i in range(20): # 10为线程数量
		t = Checking(queue, w)
		t.setDaemon(True)
		t.start()
	queue.join()
	avail.close()
	
if __name__ == '__main__':
	main()
