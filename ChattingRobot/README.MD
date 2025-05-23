# 基于 Ollama 的聊天机器人平台搭建

## 聊天机器人项目简介

基于 Ollama 的聊天机器人平台搭建，基于 Ollama 模型进行训练，并使用 Flask 框架进行搭建。

## 使用方法

1. 安装依赖包

```bash
pip install ollama
pip install streamlit==1.32.0
```

2. 启动 服务

```bash
streamlit run ChattingRobot/chat_main.py
```

如果运行不成功，可以带上Python版本运行

```bash
python3.13 -m streamlit run ChattingRobot/main.py
```

3. 访问 <http://localhost:8501> 启动聊天界面

## 模型训练

1. 下载模型

# 可选：设置别名简化命令

alias python="python3.13"
