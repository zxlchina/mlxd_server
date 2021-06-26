import time
import os
import sys
import json
import requests
import OpenSSL
import certifi
import logging

import sys

sys.path.append("/home/lichzhang/code/JKTW/server/tools")
from commonlib import *




def handle_item(item):
    key_name = {'used_points','mlj','buyer_openid','payer_is_leaguer','settlement_total_fee','trade_state','promotion_fee','time_start','has_promotion','weeklyup','remark','total_refund_fee','time_end','shop_buyer_count','order_fee','order_source','buyer_nick','shop_id','buyer_headimgurl','out_trade_no','total_fee','points_deduct_fee'}
    #key_name = {'out_trade_no'}
    
    field_list = []
    value_list = []

    for key in item:
        if key not in key_name:
            #print("key no in key list, key=", key)
            continue

        field_list.append(key)
        if type(item[key]) in {bool, int}:
            value_list.append(str(item[key]))
            # print(str(item[key]))
        else:
            value_list.append("\"" +  item[key] + "\"")
            # print(item[key].encode('utf-8'))
            
    
    sql = "insert into order_list (%s) values (%s)" % (",".join(field_list), ",".join(value_list))
    # print(sql.encode('utf-8'))
    return item["out_trade_no"], sql


def get_data(sid):
    from_data_on = 0
    page_size = 20
    while True:
        try:
            url = "https://payapp.weixin.qq.com/mdmgr/orderv2/list?sid=%s&page_size=%d&from_date_on=%d&shop_id=0&emp_id=0&auth_mch_id=130501667&_ver=3.37.6" % (sid, page_size, from_data_on)
            print(url)
            response = requests.get(url)
        except Exception as err:
            logging.error(self.log_prefix + "get Exception:" + str(err))
            print("get Exception:" + str(err))
            return None

        # response.encoding='utf-8'
        #print(type(response.content))
        res_text = response.content.decode('utf-8').strip()
        #print(res_text.encode('utf-8'))
        json_data = json.loads(res_text)
        if json_data["retcode"] != 0:
            print("ret=", json_data["retcode"])
            return None

        orders = json_data["data"]["orders"]
        for item in orders:
            tradeno, sql = handle_item(item)
            from_data_on = item["time_end"]
            res,errno, errmsg  = get_result_with_error(sql)
            if res is None:
                print("run insert sql error|tradeno=%s" % tradeno)
                if errno == 1062:
                    print("tradeno exist, so stop")
                    return False
                
        if len(orders) < page_size:
            print("len(orders)=%d|exit" % len(orders))
            break 
            
    #print(res_text.encode('utf-8'))
    return False


if __name__=='__main__':
    #get_data("i_0p3KO7gkSXamWxlvugto6A")

    logging.basicConfig(format='%(asctime)s %(message)s',filename='log_auto_get_data.log',level=logging.DEBUG)

    init_db()
    index = 0
    while True:
        index = index + 1
        logging.info("Try %d" % index)
        get_data("i__MnPgwD8QpGzhSSXg4pAfg")
        logging.info("Try Over %d" % index)
        time.sleep(10)

