# 直出模式，输入会等到模型全部输出完毕再返回响应
import os
import re

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.getenv("AZURE_INFERENCE_SDK_ENDPOINT",
                     "你的API链接")
model_name = os.getenv("DEPLOYMENT_NAME", "DeepSeek-R1")
key = os.getenv("AZURE_INFERENCE_SDK_KEY",
                "你的API token（令牌）")
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
        timeout=60
    )

    assistant_reply = response.choices[0]["message"]["content"]
    # 去除空思考部分
    assistant_reply = re.sub(r"<think>\s*</think>", "", assistant_reply, flags=re.DOTALL)
    # 去除多余换行符，空字符
    assistant_reply = re.sub(r"\n\n", "\n", assistant_reply, flags=re.DOTALL)
    print(assistant_reply)

    # 保留上下文中去除思考部分
    content_assistant_reply = re.sub(r"<think>.*?</think>", "", assistant_reply, flags=re.DOTALL)
    messages.append(AssistantMessage(content=content_assistant_reply))
