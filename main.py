from flask import Flask, url_for
import time
import random
import json
from flask import request
import os
import requests
import hashlib
import urllib
import base64
import logging
from urllib.parse import urlparse
import PIL.Image as Image
from datetime import timedelta

import sys

sys.path.append("/home/lichzhang/code/JKTW/server/tools")
from commonlib import *


g_appid="wxdf88587fa284b306"
g_secret="1667e7bf19334c26e72386f3cda0feaa"




app = Flask(__name__)


upload_file_path = "/home/lichzhang/release/ShareCard/images/"

url_path = "/mlxd"


@app.route(url_path + "/")
def hello_world():
    app.logger.debug("debug, this is a log test")
    app.logger.warning("warning, this is a log test")
    app.logger.error("error, thir is a log test")
    return "Hello World! mlxd"



@app.route(url_path + "/reply", methods=['GET', 'POST'])
def reply():
    content = escape_str(request.args.get('content', ''))
    openid = escape_str(request.args.get('openid', ''))
    sql = "insert into reply (content, author) values ('%s', '%s')" % (content, openid)

    print(sql)
    
    result, errno, errmsg = get_result_with_error(sql)
    
    if result is None:
        res = {}
        res["ret"] = -1
        res["error"] = "提交失败，请稍后再试"
        res["errno"] = errno
        res["errmsg"] = errmsg
        return json.dumps(res)


    res = {} 
    res["ret"] = 0
    return json.dumps(res) 
    
 



def get_file_name():
    #得到当前时间
    return  time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + "_" + str(int(random.uniform(1000,9999)))



# 获取今天开始的时间戳
def get_current_day_begin_timestamp():
    time_string = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d 00:00')
    timestamp = time.mktime(datetime.datetime.strptime(time_string, "%Y-%m-%d 00:00").timetuple())
    return int(timestamp)

# 获取今天开始的时间戳
def get_current_month_begin_timestamp():
    time_string = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-01 00:00')
    timestamp = time.mktime(datetime.datetime.strptime(time_string, "%Y-%m-01 00:00").timetuple())
    return int(timestamp)


# 计算这周开始的时间戳
def get_current_week_begin_timestamp():
    date1 = datetime.datetime.now()
    this_week_start_dt = str(date1-timedelta(days=date1.weekday())).split()[0]
    timestamp = time.mktime(datetime.datetime.strptime(this_week_start_dt, "%Y-%m-%d").timetuple())
    return int(timestamp)



@app.route(url_path + "/get_rank", methods=['GET'])
def get_card_type_list():

    rank_type = request.args.get('type', '0')

    time_start = get_current_month_begin_timestamp()
    time_end = int(time.time())
    if rank_type ==  "0": # 当天排行榜
        time_start = get_current_day_begin_timestamp()
    elif rank_type == "1":       # 周排行榜
        time_start = get_current_week_begin_timestamp()
    else:       # 上周
        time_end = get_current_week_begin_timestamp()
        time_start = time_end - 86400 * 7

    sql = "select * from (SELECT buyer_openid,count(distinct out_trade_no) as cnt, max(buyer_headimgurl) as buyer_headimgurl, max(buyer_nick) as buyer_nick, max(time_end) as time_end from order_list where time_end >= " + str(time_start) + " and time_end <" + str(time_end) +  " group by buyer_openid)a order by cnt desc, time_end asc"

    app.logger.warning(sql);
    result, errno, errmsg = get_result_with_error(sql)

    res = {}

    if result is None:
        res["ret"] = -1
        res["sql"] = sql
        res["errno"] = errno
        res["errmsg"] = errmsg
        return json.dumps(res)


    res["ret"] = 0
    res["buyer_list"] = []

    for item in result:
        one_buyer= {}

        one_buyer["buyer_openid"] = item[0]
        one_buyer["count"] = item[1]
        one_buyer["buyer_headimgurl"] = item[2]
        one_buyer["buyer_nick"] = item[3]


        res["buyer_list"].append(one_buyer)

    return json.dumps(res)
    



@app.route(url_path + "/code2session", methods=['GET', 'POST'])
def code_2_session():
    jscode = request.args.get('jscode', '')
    if jscode == "":
        res = {}
        res["ret"] = -1 
        res["error"] = "jscode is empty!"
        return json.dumps(res)

    #下面开始换session信息
    url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (g_appid, g_secret, jscode)

    res = requests.get(url)

    print(res.text)

    result = json.loads(res.text) 
    sql = "insert into user_info (openid) values ('%s')" % (result["openid"])
    get_result(sql)
    
    print(sql)

    return res.text




if __name__ == '__main__':
    handler = logging.FileHandler('flask2.log', encoding='UTF-8')
    # handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    print(get_file_name())
    init_db()
    app.run(host="0.0.0.0", port=5006, debug=True)



