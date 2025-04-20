import os
from volcenginesdkarkruntime import Ark
from typing import Optional
os.environ["ARK_API_KEY"] = "726049fd-3560-495f-96e6-51a81ac51260"
endpoint_id = "ep-20250420153708-ljgx6" # doubao 1.5
# endpoint_id = "ep-20250420152045-kpmvb" # doubao thinking



def llm_completions(endpoint_id, prompt, system_prompt=None, config=None):
    client = Ark(
        # 此为默认路径，您可根据业务所在地域进行配置
        base_url="https://ark.cn-beijing.volces.com/api/v3"
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    )
    messags = []
    if system_prompt:
        messags.append(
            {"role": "system", "content": system_prompt}
        )
    messags.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    default_config = {"max_tokens": 100, "temperature": 0.7, "top_p": 0.9}
    if config:
        default_config.update(config)
    response = client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model=endpoint_id,
        messages=messags,
        **default_config,
        tools=None,
        response_format = {"type": "text"} # {"type": "json_object"}
    )
    return response.choices[0].message.reasoning_content, response.choices[0].message.content


def doubao_completion(endpoint_id, messages, tools=None)-> str:

    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
    )

    # 获取回复
    response = None
    try:
        response = client.chat.completions.create(
            model=endpoint_id,
            messages = messages,
            stream=False,
            tools=tools,
            top_p=0.5,
            max_tokens=1000,
        )
        return response
    except Exception as e: 
        print("Error: {}".format(e))
    return response