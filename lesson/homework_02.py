"""
作业二

实现 role-play 对话数据生成工具，要求包含下列功能：

基于一段文本（自己找一段文本，复制到提示词就可以了，比如你可以从小说中选取一部分文本，注意文本要用 markdown 格式）生成角色人设，可借助 ChatGLM 实现。
给定两个角色的人设，调用 CharacterGLM 交替生成他们的回复。
将生成的对话数据保存到文件中。
（可选）设计图形界面，通过点击图形界面上的按钮执行对话数据生成，并展示对话数据。
"""

"""
在homework_02主函数中，设置以下几个变量，可根据实际情况修改：

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
执行命令：py homework_02.py

生成的对话结果将保存至：output.txt中

注意：程序运行前需要在api.py中设置好key
"""

from api import get_chatglm_response_via_sdk, get_characterglm_response

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
    answer = "".join(get_characterglm_response(messages, meta=character_meta))
    return answer

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

def homework_02():

    print("####################程序开始####################")

    #设定两个角色的名称
    name1 = "孙悟空"
    name2 = "唐僧"
    #角色1开场白
    init_msg = "你好，让我们开始聊天吧。"
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
    homework_02()
