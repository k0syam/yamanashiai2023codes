from chatgpt import ChatGPTDialogue
from dalle2 import Dalle2Communication


is_debug = True


def main_generate_theme():
    # まずは勉強会の目標地点の概要を出力→dict型で出力結果を保持
    cgd = ChatGPTDialogue()
    cgd.clear_messages(need_default_messages=False)
    with open("system_instruction.md", "r", encoding="utf-8") as f:
        s = f.readlines()
        s = "".join(s)
    cgd.add_system_message(s)
    with open("user_ask_abstract.md", "r", encoding="utf-8") as f:
        s = f.readlines()
        s = "".join(s)
    cgd.add_user_message(s)
    cgd.add_assistant_message()
    if is_debug:
        print(cgd.show_current_messages())
    with open("assistant_out_abstract.txt", "w", encoding="utf-8") as f:
        f.write(cgd.show_current_messages()[-1])
    theme_abst = {}
    state_num = 0
    k_list, v_list = [], []
    for s in cgd.show_current_messages()[-1].split("\n"):
        print(k_list, v_list, s, state_num)
        if state_num == 0:
            if "出力物タイトル" in s:
                state_num += 1
        elif state_num == 1:
            k_list.append(s)
            state_num += 1
        elif state_num == 2:
            if "出力物内容" in s:
                state_num += 1
        elif state_num == 3 and len(s) >= 1:
            v_list.append(s)
        else:
            theme_abst["".join(k_list)] = "".join(v_list)
            k_list, v_list = [], []
            state_num = 0
    if len(v_list) >= 1:
        theme_abst["".join(k_list)] = "".join(v_list)

    if is_debug:
        print(theme_abst)
    # イメージをDALL-E 2で生成
    d2c = Dalle2Communication()
    d2c.add_image_generation(theme_abst["目標地点を想起させるイメージに用いる画像生成プロンプト"])
    d2c.download_image_latest("theme_image.png")

    # TBD: 分割した勉強会内容の詳細・実装例を示す


if __name__ == "__main__":
    main_generate_theme()
