#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import requests
import re
import os
import argparse
import multiprocessing
from textwrap import dedent
from itertools import izip_longest
import string
from colorama import Fore,Style,init
init(autoreset=True)

os.system('clear')
counter = 0

def ExtractTags(username):
	try:
		username = username.rstrip()
	except:
		return None
	hashtags = []
	headers = {
	    'Host': 'nitter.pussthecat.org',
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
	    'Accept-Encoding': 'gzip, deflate',
	    'Upgrade-Insecure-Requests': '1',
	    'Te': 'trailers',
	    'Connection': 'close',
	}

	response = requests.get('https://nitter.pussthecat.org/'+username.rstrip(), headers=headers)
	for line in response.content.splitlines():
		if '<a href="/search?q=' in line and '">#' in line:
			temp = line.split('<a href="/search?q=')
			for blablabla in temp:
				if '#' in blablabla:
					try:
						tags = re.search('">(.*)</a>', blablabla)
						hashtags.append(tags.group(1))
					except:
						continue
	rez = RemoveDuplicate(hashtags)
	for line in rez:
		payload = 'echo "'+line+'" >> '+args.dir+'/tags_extracted.txt'
		os.system(payload)
	print(Style.BRIGHT+Fore.YELLOW+"["+Fore.GREEN+"+"+Fore.YELLOW+"] "+Fore.WHITE+username.rstrip()+Fore.YELLOW+" -> "+Fore.GREEN+"Done.")


def RemoveDuplicate(rez):
	return list(dict.fromkeys(rez))

def Extractor(result):
	for line in result.splitlines():
		if '<a class="username" href="/' in line:
			username = re.search('<a class="username" href="/(.*)" title="', line)
			username = username.group(1)
			payload = 'echo '+username+" >>" +args.dir+'/.temp.txt'
			os.system(payload)
		try:
			if '">Load more</a>' in line:
				cursor = re.search('cursor=(.*)">Load more</a>',line)
				cursor = cursor.group(1)
				return cursor
		except:
			return None

def first(tags):
	try:
		tags = tags.rstrip()
	except:
		return None
	headers = {
	    'Host': 'nitter.pussthecat.org',
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
	    'Accept-Encoding': 'gzip, deflate',
	    'Upgrade-Insecure-Requests': '1',
	    'Te': 'trailers',
	    'Connection': 'close',
	}

	params = (
	    ('q', tags),
	)

	response = requests.get('https://nitter.pussthecat.org/search', headers=headers, params=params)
	cursor = Extractor(response.content)
	if cursor != None:
		Next(cursor,tags)
	else:
		return None

def Next(cursor,tags):
	headers = {
	    'Host': 'nitter.pussthecat.org',
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
	    'Accept': '*/*',
	    'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
	    'Accept-Encoding': 'gzip, deflate',
	    'Te': 'trailers',
	    'Connection': 'close',
	}

	params = (
	    ('f', 'tweets'),
	    ('q', tags),
	    ('cursor', cursor),
	    ('scroll', 'true'),
	)

	response = requests.get('https://nitter.pussthecat.org/search', headers=headers, params=params)
	cursor_temp = cursor
	cursor = Extractor(response.content)
	if cursor == None:
		print(Style.BRIGHT+Fore.YELLOW+"["+Fore.GREEN+"+"+Fore.YELLOW+"] "+Fore.WHITE+tags+Fore.YELLOW+" -> "+Fore.GREEN+"Done.")
		return None
	if cursor_temp == cursor:
		print(Style.BRIGHT+Fore.YELLOW+"["+Fore.GREEN+"+"+Fore.YELLOW+"] "+Fore.WHITE+tags+Fore.YELLOW+" -> "+Fore.GREEN+"Done.")
		return None
	else:
		Next(cursor,tags)


def grouper(n, iterable, padvalue=None):
	return izip_longest(*[iter(iterable)]*n, fillvalue=padvalue)




parser = argparse.ArgumentParser()
parser.add_argument('--tags', action="store_true", help="Extract Username from Tags")
parser.add_argument('--username', action="store_true", help="Extract Tags from username")
parser.add_argument('--source', type=str, required=True, help="Source file containing hashtags")
parser.add_argument('--dir', type=str, required=True, help="Directory name for result")
args = parser.parse_args()
if not os.path.isdir(args.dir):
	os.mkdir(args.dir)


if args.username:
	test_data = open(args.source)
	p = multiprocessing.Pool(50)
	for chunk in grouper(1000, test_data):
		results = p.map(first, chunk)

	with open(args.dir+"/.temp.txt") as f:
		username_result = f.read().splitlines()
	os.remove(args.dir+"/.temp.txt")
	write_username = open(args.dir+"/username_extracted.txt",'a+')
	username_result = RemoveDuplicate(username_result)
	for usernames in username_result:
		write_username.write(usernames+"\n")
	write_username.close()

if args.tags:
	test_data = open(args.source)
	proces = multiprocessing.Pool(50)
	for chunk in grouper(1000, test_data):
		results = proces.map(ExtractTags, chunk)


