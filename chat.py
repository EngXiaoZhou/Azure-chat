# 需要额外安装依赖azure.identity和azure-ai-inference
import os
import re
import json

from collections import deque
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

# 读取json文件
config_file = open("config.json", "r", encoding="utf-8")
config = json.load(config_file)

config_file.close()

endpoint = os.getenv("AZURE_INFERENCE_SDK_ENDPOINT",
                     config["account"]["endpoint"])
model_name = os.getenv("DEPLOYMENT_NAME", config["account"]["modelName"])
key = os.getenv("AZURE_INFERENCE_SDK_KEY",
                config["account"]["token"])
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# json中读取部分复用参数
system_messages = config["model"]["systemMessage"]
max_messages = config["model"]["maxHistoryMessages"]
stream_mode = config["model"]["streamMode"]
# 初始化信息队列，更好维护信息长度
messages = deque(maxlen=max_messages)
messages.append(SystemMessage(content=system_messages))

loop = True
while loop:
    input_text = input("您：")
    messages.append(UserMessage(content=input_text))
    response = client.complete(
        messages=list(messages),
        model=model_name,
        max_tokens=config["model"]["maxTokens"],
        temperature=config["model"]["temperature"],
        top_p=config["model"]["topP"],
        stop=config["model"]["stop"],
        frequency_penalty=config["model"]["frequencyPenalty"],
        presence_penalty=config["model"]["presencePenalty"],
        timeout=config["model"]["timeout"],
        stream=stream_mode
    )

    assistant_reply = ""
    if stream_mode:
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
    else:
        assistant_reply = response.choices[0]["message"]["content"]
        # 去除空思考部分
        assistant_reply = re.sub(r"<think>\s*</think>", "", assistant_reply, flags=re.DOTALL)
        # 去除多余换行符，空字符
        assistant_reply = re.sub(r"\n\n", "\n", assistant_reply, flags=re.DOTALL)
        print(assistant_reply)

    # 保留上下文中去除思考部分
    content_assistant_reply = re.sub(r"<think>.*?</think>", "", assistant_reply, flags=re.DOTALL)
    messages.append(AssistantMessage(content=content_assistant_reply))
