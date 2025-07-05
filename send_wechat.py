#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的微信消息发送工具
用法: python send_wechat.py "联系人名字" "消息内容"
"""
import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from desktop_automation.cli import _execute_actions

def send_wechat_message(contact_name, message_content):
    """发送微信消息"""
    workflow_file = "src/desktop_automation/successful_workflows/send_wechat_parameterized.json"
    
    with open(workflow_file, 'r', encoding='utf-8') as f:
        action_sequence = json.load(f)
    
    workflow_params = {
        "contact_name": contact_name,
        "message_content": message_content
    }
    
    print(f"正在给 {contact_name} 发送消息...")
    _execute_actions(action_sequence, None, workflow_params)
    print("消息发送完成!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python send_wechat.py \"联系人名字\" \"消息内容\"")
        print("示例: python send_wechat.py \"张三\" \"你好，这是自动发送的消息\"")
        sys.exit(1)
    
    contact_name = sys.argv[1]
    message_content = sys.argv[2]
    
    send_wechat_message(contact_name, message_content)