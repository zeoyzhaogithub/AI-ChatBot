# @Time: 2025-03-22
# @Author: zeoy
# 基于 Ollama 的聊天机器人平台搭建

"""
该模块用于充当聊天机器人的前端模块，
接收用户输入的问题,调用utils模块,获取回复,
通过streamlit模块,将回复并显示给用户
"""
import os
import sys
import time

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

# ========== 修改后的完整CSS样式 ==========
st.markdown("""
    <style>
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999;
            background: white;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .main-content {
            margin-top: 100px;
        }

        /* 用户消息容器 */
        div[data-testid="stChatMessage"][aria-label*="user"] {
            justify-content: flex-end !important;
            margin-left: auto !important;
            max-width: 85%;
        }

        /* 用户消息气泡 */
        div[data-testid="stChatMessage"][aria-label*="user"] > div:first-child {
            background-color: #007bff !important;
            color: white !important;
            border-radius: 15px 15px 0 15px !important;
            padding: 12px !important;
        }

        /* 助手消息容器 */
        div[data-testid="stChatMessage"][aria-label*="assistant"] {
            justify-content: flex-start !important;
            max-width: 85%;
        }

        /* 助手消息气泡 */
        div[data-testid="stChatMessage"][aria-label*="assistant"] > div:first-child {
            background-color: #f1f3f4 !important;
            border-radius: 15px 15px 15px 0 !important;
            padding: 12px !important;
        }

        /* 消息间距 */
        .stChatMessage {
            margin: 5px 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ========== 标题部分保持不变 ==========
header = st.container()
with header:
    st.markdown(
        "<h1 style='text-align: center; color: black;'>👒 zeoy's chat robot </h1>",
        unsafe_allow_html=True
    )
    st.markdown('<hr style="margin: 0.5rem 0;">', unsafe_allow_html=True)

# ========== 主内容容器 ==========
main_container = st.container()
with main_container:
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

# 判断是否有历史聊天记录数据，如果没有就创建，并存储所有记录消息
# st.session_state存储会话状态，用于存储会话数据

# 初始化会话
if "memory" not in st.session_state:
    # 创建一个conversationBufferMemory对象，用于存储会话记录
    st.session_state.memory = ConversationBufferMemory(
        input_key="human_input",
        output_key="ai_response"
    )
    # 添加聊天机器人的欢迎语句
    st.session_state.message = [
        {"role": "assistant", "content": "hello,welcome to zeoy's chat robot."}
    ]
    
# 遍历session_state.message列表，
for message in st.session_state.message:
    #  聊天消息 显示当前角色内容
    #  ========== 根据角色添加头像 ==========
    avatar = "👒" if message["role"] == "assistant" else "🔔"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 接收用户录入的内容
prompt = st.chat_input("请输入您要咨询的内容")

# 判断用户输入的内容是否为空
if prompt:
    # 显示用户输入的内容
    st.session_state.message.append({'role': 'user', 'content': prompt})
    with st.chat_message("user", avatar="🔔"):  # 添加用户头像
        st.markdown(prompt)
    # ========== 修改：助手消息使用新头像 ==========
    # with st.chat_message("assistant", avatar="👒"):  # 添加助手头像
        #placeholder = st.empty()
    #     full_response = ""
    #     try:
    #         for chunk in utils.get_response(st.session_state.message):
    #             # time.sleep(0.05)
    #             full_response += chunk
    #             placeholder.markdown(full_response + "▌")
    #         print(full_response)    
    #         placeholder.markdown(full_response)
    #     except Exception as e:
    #         error_msg = f"响应生成失败：{str(e)}"
    #         placeholder.markdown(error_msg)
    #         full_response = error_msg
        # st.session_state.message.append({"role": "assistant", "content": full_response})
# st.markdown('</div>', unsafe_allow_html=True)


    # # 获取机器人的回复
    response = utils.get_response(prompt)
    # 显示机器人的回复
    with st.chat_message("assistant", avatar="👒"):
        st.markdown(response)
    # 将用户输入的内容和机器人的回复添加到session_state.message列表中
    st.session_state.message.append(
        {'role': 'assistant', 'content': response}
    )
st.markdown('</div>', unsafe_allow_html=True)
    