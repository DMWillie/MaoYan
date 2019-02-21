"""
    作者:北辰
    日期:09/02/2019
    功能:利用requests库抓取猫眼电影排行
    版本:1.0
"""

import requests
import re
import json
import time

s1 = '<dd>.*?board-index.*?>(.*?)</i>' #电影排名正则表达式
s2 = '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)"' #电影图片正则表达式
# 电影名称正则表达式
s3 = '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>'
# 电影主演正则表达式
s4 = '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>' \
     '.*?star.*?>(.*?)</p>'
# 电影上映时间正则表达式
s5 = '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>' \
     '.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>'
# 电影评分正则表达式
s6 = '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>' \
     '.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>' \
     '.*?fraction.*?>(.*?)</i>.*?</dd>'

def get_one_page(url):
    """
    抓取首页
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.81 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def parse_one_page(html):
    """
    解析页面
    """
    pattern = re.compile(s6,re.S)
    items = re.findall(pattern,html)
    # 遍历提取结果并生成字典
    for item in items:
        yield{
            'index':item[0],
            'image':item[1],
            'title':item[2].strip(),
            'actor':item[3].strip(),
            'time':item[4].strip(),
            'score':item[5].strip()+item[6].strip()
        }

def write_to_file(content):
    """
    写入文件
    """
    with open('result.txt','a',encoding='utf-8') as f:
        print(type(json.dumps(content)))  #字典序列化
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(offset):
    """
    主函数:抓取TOP100电影的相关信息
    """
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(0.5)  #增加延时等待,防止速度过快