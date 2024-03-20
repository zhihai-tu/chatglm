"""
作业二

实现 role-play 对话数据生成工具，要求包含下列功能：

基于一段文本（自己找一段文本，复制到提示词就可以了，比如你可以从小说中选取一部分文本，注意文本要用 markdown 格式）生成角色人设，可借助 ChatGLM 实现。
给定两个角色的人设，调用 CharacterGLM 交替生成他们的回复。
将生成的对话数据保存到文件中。
（可选）设计图形界面，通过点击图形界面上的按钮执行对话数据生成，并展示对话数据。
"""

import time
from dotenv import load_dotenv
load_dotenv()

from api import get_chatglm_response_via_sdk, get_characterglm_response

def generate_character_profiles(text):
    """
    基于输入文本生成角色人设
    
    Args:
        text (str): 输入文本
    
    Returns:
        str: 某个角色的人设信息
    """
    prompt = f"根据以下文本,生成某个角色的详细人设信息，约100字左右:\n\n{text}"
    
    response =  get_chatglm_response_via_sdk(
        messages=[
            {
                "role": "user",
                "content": prompt.strip()
            }
        ]
    )

    print("".join(response))
    return response


def generate_dialogue(character1, character2, name1, name2, history):
    """
    基于给定的角色人设交替生成对话
    
    Args:
        character1 (str): 角色1的人设
        character2 (str): 角色2的人设
    
    Returns:
        str: 生成的对话文本
    """
    #prompt = f"根据以下两个角色的人设,生成一段对话:\n\n{character1}\n\n{character2}"
    
    character_meta = {
        "user_info": character1,
        "bot_info": character2,
        "user_name": name1,
        "bot_name": name2
    }

    messages = history
    answer = "".join(get_characterglm_response(messages, meta=character_meta))
    print(name2 + ":" + answer)
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

    text1 = """
    孙悟空，是在小说《西游记》中登场的主要角色之一，为一只道行高深的猴子，别名孙行者、孙猴子。自封美猴王、齐天大圣。因曾在天庭掌管御马监而又被称为弼马温，在取经完成后被如来佛祖授封为斗战胜佛。
    在小说中，孙悟空出身花果山，是由灵石中吸收天地灵气、日月精华，经风吹日晒孕育而成之石猴，在出海后自须菩提祖师处修得七十二变地煞术。修行后他曾先后闯龙宫、地府，取得能随使用者心意自由变化大小的如意金箍棒、并自阎罗王的生死簿上除籍取得永寿。经天界玉皇大帝招安后，由于未受邀蟠桃会并遭讥讽，孙悟空以“齐天大圣”之名大闹天宫、只身与天兵天将相持，后遭释迦如来镇压于五行山（五指山）下。他在封印五百年后被南海观世音点化，保护唐三藏法师前往西天取经，协同猪八戒、沙悟净和白龙马艰辛克难伏魔降妖。旅途中，孙悟空屡次运用其武艺与智慧，拯救为妖怪所劫的唐僧师徒。历经九九八十一难后，终至西天取得真经功成正果。
    孙悟空为东亚汉字文化圈中智勇兼备的代表性角色，被诸多文学、戏曲、影视作品重新演绎。此类作品在设计上多所沿用原著中孙悟空所使用之金箍棒、筋斗云、七十二变、分身术等等法宝神通，或是参考其本身聪明、调皮、活泼、忠诚、嫉恶如仇等性格特征。
    """

    text2 = """
    唐僧、唐三藏原型是唐代玄奘法师。宋《大唐三藏取经诗话》中，也以“玄奘”来称呼唐三藏，[1]小说中，唐三藏性格善良慈悲且意志坚定，但有时又显得迂腐且不辨是非，《西游记》中，唐僧所持宝物为观世音菩萨所赠的九环锡杖和锦斓袈裟，在故事最后，唐三藏修成正果，受封旃檀功德佛。[注 1]真实的历史中，玄奘所译经典至今尚有心经与药师经等，当时法师走陆路出新疆葱岭（今帕米尔高原）到印度，回国后应唐太宗之命根据旅途所见所闻编纂出了《大唐西域记》，到1560年代中，明作家吴承恩改写成章回小说《西游记》。
    今日不明佛教的大众受到《西游记》影响，常误解“三藏”为玄奘专属的称号。实际上，“三藏法师”是一种敬称，指精通佛教圣典三大类别“经、律、论”等三藏的法师，又称三藏比丘、三藏圣师，或略称三藏，因此，将三藏之号特指一人是错误的。称“唐三藏”意在尊称其为“唐国的三藏法师”，有避其名讳之用。除玄奘外，史上著名三藏法师还有东汉安世高、东晋鸠摩罗什与法显、南朝宋求那跋陀罗、唐实叉难陀、义净与大广智不空等；日本史上唯一的三藏法师为灵仙法师。
    """

    character1 = generate_character_profiles(text1)
    character2 = generate_character_profiles(text2)

    init_msg = "你好，让我们开始聊天吧。"
    history = [
        {"role": "assistant", "content": init_msg}
    ]
    print("=========================================================")
    print("孙悟空：" + init_msg)

    for i in range(1, 10):
        if i%2 == 1:
            c1 = "".join(character1)
            c2 = "".join(character2)
            n1 = "孙悟空"
            n2 = "唐僧"
        else:
            c1 = "".join(character2)
            c2 = "".join(character1)
            n1 = "唐僧"
            n2 = "孙悟空" 

        answer =  generate_dialogue(c1, c2, n1, n2, invert_roles(history))
        history.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    homework_02()
