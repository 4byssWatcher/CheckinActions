# -*- coding: utf-8 -*-

import requests
import re
import http.client as http_client
import logging
import argparse


def get_cookie():
	parser = argparse.ArgumentParser()
	parser.add_argument('--cookie', type=str, default = None)
	args = parser.parse_args()
	return args.cookie


def new_cookie(r, prev):
	pattern = r"(?<=SESSION=).*?(?=;)"
	res = re.findall(pattern, r.text)
	if res:
		return res[0]
	else:
		return prev


def check_report(cookie):
	url = "https://jzsz.uestc.edu.cn/wxvacation/checkRegisterNew"
	headers = {
		"Connection": "keep-alive",
		"Cookie": "JSESSIONID=" + cookie,
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
		"X-Tag": "flyio",
		"content-type": "application/json",
		"encode": "false",
		"Referer": "https://servicewechat.com/wx521c0c16b77041a0/28/page-frame.html",
		"Accept-Encoding": "gzip, deflate, br"
	}
	r = requests.get(url, headers=headers, verify=False)
	
	return r.json()['data']['appliedTimes'], new_cookie(r, cookie)


def do_report(cookie):
	url = "https://jzsz.uestc.edu.cn/wxvacation/monitorRegisterForReturned"
	headers = {
		"Connection": "keep-alive",
		"Content-Length": "219",
		"cookie": "JSESSIONID="+cookie,
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
		"x-tag": "flyio",
		"content-type": "application/json",
		"encode": "false",
		"Referer": "https://servicewechat.com/wx521c0c16b77041a0/28/page-frame.html",
		"Accept-Encoding": "gzip, deflate, br"
	}
	json = {
		"healthCondition": "正常",
		"todayMorningTemperature": "36°C~36.5°C",
		"yesterdayEveningTemperature": "36°C~36.5°C",
		"yesterdayMiddayTemperature": "36°C~36.5°C",
		"location": "四川省成都市郫都区科化一路23号"
	}
	r = requests.post(url, headers=headers, json=json, verify=False)
	return new_cookie(r, cookie)


def init_log():
	http_client.HTTPConnection.debuglevel = 1

	logging.basicConfig()
	logging.getLogger().setLevel(logging.DEBUG)
	requests_log = logging.getLogger("requests.packages.urllib3")
	requests_log.setLevel(logging.DEBUG)
	requests_log.propagate = True


if __name__ == '__main__':
	#init_log()
	cookie = get_cookie()
	flag, cookie = check_report(cookie)
	if not flag:
		cookie = do_report(cookie)
	print(cookie)
