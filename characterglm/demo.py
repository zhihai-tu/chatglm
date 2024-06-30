"""
在demo主函数中，设置以下几个变量，可根据实际情况修改：

1、设定第一个角色的名称
    name1 = "孙悟空"
2、设定第二个角色的名称
    name2 = "唐僧"
3、设定对话的开场白，即第一个角色说的第一句话
    init_msg = "你好，让我们开始聊天吧。"
4、对话次数，即角色1和角色2总计说话的次数
    k=15
5、在story_01.txt中复制粘贴一段文本，文本主要是对角色1的介绍
6、在stroy_02.txt中复制粘贴一段文本，文本主要是对角色2的介绍

程序运行：
执行命令：py demo.py

生成的对话结果将保存至：output.txt中
"""

import os
from zhipuai import ZhipuAI

# 智谱开放平台API key，补充你自己的API key
API_KEY: str = os.getenv("API_KEY", "")

# chatglm通用大模型sdk
def get_chatglm_response_via_sdk(messages):
    
    client = ZhipuAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages,
        stream=True,
    )
    for chunk in response:
        yield chunk.choices[0].delta.content

# characterglm超拟人大模型sdk        
def get_characterglm_response_via_sdk(messages, meta):

    client = ZhipuAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="charglm-3",
        meta=meta,
        messages=messages,
        stream=True,
    )
    for chunk in response:
        yield chunk.choices[0].delta.content
    
# 根据人物简介生成角色人设信息
def generate_character_profiles(text):
    """
    基于输入文本生成角色人设
    
    Args:
        text (str): 输入文本
    
    Returns:
        str: 某个角色的人设信息
    """
    prompt = f"根据以下文本,生成某个角色的详细人设信息，在100个字以内:\n\n{text}"
    
    response =  get_chatglm_response_via_sdk(
        messages=[
            {
                "role": "user",
                "content": prompt.strip()
            }
        ]
    )
    return "".join(response)

# 生成一轮对话
def generate_dialogue(character1, character2, name1, name2, history):
    """
    基于给定的角色人设交替生成对话
    
    Args:
        character1 (str): 角色1的人设
        character2 (str): 角色2的人设
    
    Returns:
        str: 生成的对话文本
    """
    
    character_meta = {
        "user_info": character1,
        "bot_info": character2,
        "user_name": name1,
        "bot_name": name2
    }

    messages = history
    answer = "".join(get_characterglm_response_via_sdk(messages, meta=character_meta))
    return answer

# 角色置换（user <=> assistant）
def invert_roles(messages):
    """
    Inverts the roles (user/assistant) in a list of message dictionaries.
    Returns a new list with the inverted roles.
    """
    new_messages = []
    for message in messages:
        if 'role' in message:
            if message['role'] == 'user':
                new_messages.append({'role': 'assistant', 'content': message['content']})
            elif message['role'] == 'assistant':
                new_messages.append({'role': 'user', 'content': message['content']})
        else:
            new_messages.append(message)
    return new_messages

# 主函数
def demo():

    print("####################程序开始####################")

    #设定两个角色的名称
    name1 = "孙悟空"
    name2 = "唐僧"
    #角色1开场白
    init_msg = "师傅，什么时候才能取到真经啊。"
    #k为对话的次数
    k=15

	# 读取txt文件中的文本内容（人物描述信息）
    with open('story_01.txt', 'r', encoding='utf-8') as file:
        # 读取文件内容
        text1 = file.read()
    with open('story_02.txt', 'r', encoding='utf-8') as file:
        # 读取文件内容
        text2 = file.read()

    #根据文本内容，调用chatglm-4生成人设
    character1 = generate_character_profiles(text1)
    character2 = generate_character_profiles(text2)

    # 打印角色人设
    print(name1 + "-人设：" + character1)
    print(name2 + "-人设：" + character2)

    #将开场白写入文件中
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(name1 + "：" + init_msg)

    history = [
        {"role": "assistant", "content": init_msg}
    ]

    #根据人设，调用CharacterGLM，交替自动生成答复
    for i in range(1, k):
        if i%2 == 1:
            c1 = character1
            c2 = character2
            n1 = name1
            n2 = name2
        else:
            c1 = character2
            c2 = character1
            n1 = name2
            n2 = name1

        answer =  generate_dialogue(c1, c2, n1, n2, invert_roles(history))

        #将答复追加写入文件中
        with open('output.txt', 'a', encoding='utf-8') as file:
            file.write("\n" + n2 + "：" + answer)

        history.append({"role": "assistant", "content": answer})
    
    print("####################程序结束####################")

if __name__ == "__main__":
    demo()
