import time
import os
import sys
import json
import requests
import OpenSSL
import certifi



def get_data(sid):
    try:
        response = requests.get("https://payapp.weixin.qq.com/mdmgr/orderv2/list?sid=%s&page_size=20&from_date_on=0&shop_id=0&emp_id=0&auth_mch_id=130501667&_ver=3.37.6" % sid )
    except Exception as err:
        logging.error(self.log_prefix + "get Exception:" + str(err))
        return None

    res_text = response.text.strip()
    json_data = json.loads(res_text)
    print(json_data)
    return False


if __name__=='__main__':
    get_data("i_0p3KO7gkSXamWxlvugto6A")
    pass

