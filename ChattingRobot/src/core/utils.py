import ollama

# 列出已经安装的模型
# print(ollama.list())
# 接收用户输入的提示词
def get_response(prompt):
    # 指定模型，传递角色 和提示词
    response = ollama.chat(
        model="qwen2:0.5b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.message.content

