from flask import Flask, request
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import requests
import time


# ####################### 设置区 #######################
hit_group_id = 233333333    # 需要命中的群号，小于等于0时取消该匹配条件
hit_user_id = 0             # 需要命中的Q号，小于等于0时取消该匹配条件

reply_message = "4000"            # 命中后需要回复的信息
# #####################################################

total_send_count = 1        # 命中回复的总次数（防止程序错误导致刷屏）

@app.route('/', methods=["POST"])
def receive_post_data():
    data = request.get_json()
    # print(data)
    if data['post_type'] == 'message':  # 消息
        group_id = data['group_id']     # 发送该消息的群号
        user_id = data['user_id']       # 发送该消息的Q号
        message = data['message']       # 该消息的正文
        print(data)
        if (hit_group_id <= 0 or group_id == hit_group_id) and (hit_user_id <= 0 or user_id == hit_user_id):
            if str(message).startswith('[CQ:at,qq=all]'):   # 命中“@全体成员”
                global total_send_count
                if total_send_count > 0:
                    total_send_count -= 1
                    # 进一步判断？
                    print("\033[0;31;40m", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " 命中消息", "\033[0m")
                    print(message)
                    # 随机延时？
                    send_message_once(data['message_type'], group_id, reply_message)     # 回复信息
    elif data['post_type'] == 'notice':
        pass
    # else:
        # print("忽略上报")

    return "OK"


def send_message_once(message_type: str, group_id: str, message: str):
    url = "http://127.0.0.1:5700/send_msg"  # 这里要加上http://，不然会报错
    # data = request.get_json()  # 获取上报消息
    params = {
        "message_type": message_type,
        "group_id": group_id,
        "message": message
    }
    requests.get(url, params=params)


def send_message(message):
    url = "http://127.0.0.1:5700/send_msg"  # 这里要加上http://，不然会报错
    data = request.get_json()  # 获取上报消息
    params = {
        "message_type": data['message_type'],
        "group_id": data['group_id'],
        "message": message
    }
    requests.get(url, params=params)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5701)
