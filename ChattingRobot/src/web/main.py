# @Time: 2025-03-22
# @Author: zeoy
# 基于 Ollama 的聊天机器人平台搭建

"""
该模块用于充当聊天机器人的前端模块，
接收用户输入的问题，调用chat_utils模块，获取回复，
通过streamlit模块，将回复并显示给用户
"""
import os
import sys

# 获取当前文件所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上级目录的路径
parent_dir = os.path.dirname(current_dir)
# print(parent_dir)
# 添加到sys.path中
sys.path.append(parent_dir)

# streamlit库：python 代码实现前端页面开发并部署
import streamlit as st

# 聊天机器人核心模块
# ConversationBufferMemory存储聊天机器人的会话记录
from langchain.memory import ConversationBufferMemory

import core.utils as utils


# 标题
st.title("zeoy's chat robot")


# 判断是否有历史聊天记录数据，如果没有就创建，并存储所有记录消息


# st.session_state存储会话状态，用于存储会话数据
if "history" not in st.session_state:
    # 创建一个conversationBufferMemory对象，用于存储会话记录
    st.session_state.memory = ConversationBufferMemory()
    # 添加聊天机器人的欢迎语句
    st.session_state.message = [
        {"role": "assistant", "content": "welcome to zeoy's chat robot."}
    ]
    
# 遍历session_state.message列表，
for message in st.session_state.message:
    #  聊天消息 显示当前角色内容
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收用户录入的内容
promt = st.chat_input("请输入你要咨询的问题")

# 判断用户输入的内容是否为空
if promt:
    # 显示用户输入的内容
    st.session_state.message.append({'role': 'user', 'content': promt})

    st.chat_message('user').markdown(promt)
    # 获取机器人的回复
    response = utils.get_response(promt)
    # 显示机器人的回复
    with st.chat_message("assistant"):
        st.markdown(response)
    # 将用户输入的内容和机器人的回复添加到session_state.message列表中
    st.session_state.message.append(
        {'role': 'assistant', 'content': response}
    )
    