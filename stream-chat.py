# 流模式，模型实时回复
import os
import re

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.getenv("AZURE_INFERENCE_SDK_ENDPOINT",
                     "你的API链接")
model_name = os.getenv("DEPLOYMENT_NAME", "API中部署的model名")
key = os.getenv("AZURE_INFERENCE_SDK_KEY",
                "你的token（令牌）")
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

system_messages = ""

messages = [
    SystemMessage(content=system_messages)
]

loop = True
while loop:
    input_text = input("您：")
    messages.append(UserMessage(content=input_text))
    response = client.complete(
        messages=messages,
        model=model_name,
        max_tokens=4000,
        timeout=60,
        stream=True
    )

    assistant_reply = ""
    buffer = ""

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            # 获取流式输出响应
            text = chunk.choices[0].delta.content
            buffer += text
            # 去除空思考部分
            buffer = re.sub(r"<think>\s*</think>", "", buffer, flags=re.DOTALL)
            # 去除多余换行符，空字符
            buffer = re.sub(r"\n\s*\n", "\n", buffer, flags=re.DOTALL)
            # 逐步打印流式输出
            print(buffer, end="", flush=True)

            assistant_reply += buffer
            buffer = ""  # 清空缓冲区，避免重复处理
    print("")  # 输出完换行


    # 保留上下文中去除思考部分
    content_assistant_reply = re.sub(r"<think>.*?</think>", "", assistant_reply, flags=re.DOTALL)
    messages.append(AssistantMessage(content=content_assistant_reply))
