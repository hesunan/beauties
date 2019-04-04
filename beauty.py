# -*- coding: utf-8 -*-

'''
登陆头条
搜索美女图片
爬取头条所有相关图片
'''

import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool
from requests import codes

'''
xhr网址截取
第一组：
Request URL: https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0
&format=json&keyword=%E7%BE%8E%E5%A5%B3%E5%9B%BE%E7%89%87
&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis
第三组：
https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=40
&format=json&keyword=%E7%BE%8E%E5%A5%B3%E5%9B%BE%E7%89%87
&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis
根据这些构造url
'''

headers = {
        'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 69.0.3497.100Safari / 537.36',
        'cookie': 'tt_webid=6665536812905317901; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16956e7f4a36a8-0306231921a7e4-b781636-1fa400-16956e7f4a434; CNZZDATA1259612802=1305485977-1551939864-%7C1551939864; tt_webid=6665536812905317901; __tasessionId=zmemlgbum1551941236120; csrftoken=4119b29aaf70b100514b61a8e0602de2',
        'x-requested-with': 'XMLHttpRequest'
    
    }

def get_page(offset):
    params={'aid':'24',
        'app_name':'web_search',
        'keyword':'%E7%BE%8E%E5%A5%B3%E5%9B%BE%E7%89%87',
        'offset':offset,
        'format':'json',
        'autoload':'true',
        'count':'20',
        'en_qc':'1',
        'cur_tab':'1',
        'from':'search_tab',
        'pd':'synthesis'
        }

    url='https://www.toutiao.com/api/search/content/?'+urlencode(params)
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.json()
    except:
        print('None')
print('suc1')

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title=item.get('tile')
            images=item.get('image_url')
            for image in images:
                yield{
                        'image':image,
                        'title':title
                        }
print('suc2')
 

'''               
def save_images(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response=requests.get(item.get('image'))
        if response.status_code==200:
            #构造路径
            file_path='{0}/{1}.{2}'.format(item.get('title'),md5(response.content),'.jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
                print('Downloaded image path is %s' % file_path)
            else:
                print('Already DownLoad',file_path)
    except:
        print('Failed')
print('suc3')   

'''
def save_image(item):
    img_path = 'img' + os.path.sep + item.get('title')
    print('succ2')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        resp = requests.get(item.get('image'))
        if codes.ok == resp.status_code:
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(resp.content).hexdigest(),
                file_suffix='jpg')
            if not os.path.exists(file_path):
                print('succ3')
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                print('Downloaded image path is %s' % file_path)
                print('succ4')
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image，item %s' % item)

   
def main(offset):
    json=get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)
        
GROUP_START=1
GROUP_END=10

if __name__=='__main__':
    pool=Pool()
    groups=([x*20 for x in range(GROUP_START,GROUP_END+1)])
    pool.map(main,groups)
    pool.close()
    pool.join()

print('suc4')
    
        

            
            


