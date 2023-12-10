from chatgpt import ChatGPTDialogue
from dalle2 import Dalle2Communication
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI
from github import GitHubUploader
from document import DocumentEditor
from starlette.middleware.cors import CORSMiddleware

is_debug = False

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"]
)

@app.get("/")
def main_generate_theme_example():
    """サンプル出力用

    Returns:
        ret: json出力向けdict
    """
    framework = "Django REST framework,Pygame"
    # ret = run_generation(framework=framework)
    ret = run_generation_with_documents(framework=framework)
    return ret

@app.get("/{framework}")
def main_generate_theme(framework: str):
    """指定したフレームワークでの出力を得る.3つまで入力可能．カンマ区切りで入力する

    Returns:
        ret: json出力向けdict
    """
    # ret = run_generation(framework=framework)
    ret = run_generation_with_documents(framework=framework)
    return ret

def run_generation(framework):
    # output_dir 静的出力ファイルの保存場所の定義
    output_dir = "output/"
    output_dir = Path(output_dir+datetime.now().strftime('%Y%m%d_%H%M%S'))
    output_dir.mkdir(exist_ok=True, parents=True)

    # まずは勉強会の目標地点の概要を出力→dict型で出力結果を保持
    cgd = ChatGPTDialogue()
    cgd.clear_messages(need_default_messages=False)
    with open("system_instruction.md", "r", encoding="utf-8") as f:
        s = f.readlines()
        s = "".join(s)
    cgd.add_system_message(s)
    with open("user_ask_abstract_api.md", "r", encoding="utf-8") as f:
        s = f.readlines()
        s = "".join(s)
        framework_list = ["", "", ""]
        for i, t in enumerate(framework.split(",")):
            framework_list[i] = t
        s = s.replace("$$$FW001$$$", framework_list[0]).replace("$$$FW002$$$", framework_list[1]).replace("$$$FW003$$$", framework_list[2])
    cgd.add_user_message(s)
    cgd.add_assistant_message()
    if is_debug:
        print(cgd.show_current_messages())
    with open(output_dir.joinpath("assistant_out_abstract.txt"), "w", encoding="utf-8") as f:
        f.write(cgd.show_current_messages()[-1])
    theme_abst = {}
    state_num = 0
    k_list, v_list = [], []
    for s in cgd.show_current_messages()[-1].split("\n"):
        # print(k_list, v_list, s, state_num)
        if state_num == 0:
            if "出力物タイトル" in s:
                state_num += 1
        elif state_num == 1:
            k_list.append(s.lstrip("*- "))
            state_num += 1
        elif state_num == 2:
            if "出力物内容" in s:
                state_num += 1
        elif state_num == 3 and len(s) >= 1:
            v_list.append(s)
        else:
            if "初心者に5段階で説明するため、段階に分割したタイトル" in k_list or "分割したタイトルの説明" in k_list:
                theme_abst["".join(k_list)] = v_list
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
    d2c.download_image_latest(output_dir.joinpath("theme_image.png"))


    # TBD: 分割した勉強会内容の詳細・実装例を示す
    # title = theme_abst["タイトル"]
    # general_info = theme_abst["概要"]
    # hashtag = theme_abst["ハッシュタグ"]
    # outline = theme_abst["初心者に5段階で説明するため、段階に分割したタイトル"]
    # outline_info = theme_abst["分割したタイトルの説明"]
    # image_url = d2c.images_url[-1]
    # for i, ol in enumerate(outline):
    #     cgdp = ChatGPTDialogue()
    #     cgdp.clear_messages(need_default_messages=False)
    #     with open("system_instruction.md", "r", encoding="utf-8") as f:
    #         s = f.readlines()
    #         s = "".join(s)
    #     cgdp.add_system_message(s)
    #     with open("user_ask_content.md", "r", encoding="utf-8") as f:
    #         s = f.readlines()
    #         s = "".join(s)
    #         s = s.replace("$$$タイトル$$$", title).replace("$$$概要$$$", general_info).replace("$$$順序$$$", "".join(outline)).replace("$$$選択項目$$$", ol)
    #     print(s)
    #     cgdp.add_user_message(s)
    #     cgdp.add_assistant_message()
    #     output_dir.joinpath(f"chapter{i+1:02}").mkdir(exist_ok=True, parents=True)
    #     with open(output_dir.joinpath(f"chapter{i+1:02}", "assistant_out.txt"), "w", encoding="utf-8") as f:
    #         f.write(cgdp.show_current_messages()[-1])

    # 出力変数：jsonでかえす
    ret = {}
    ret["output_dir"] = str(output_dir)
    ret["title"] = theme_abst["タイトル"]
    ret["general_info"] = theme_abst["概要"]
    ret["hashtag"] = theme_abst["ハッシュタグ"]
    ret["outline"] = theme_abst["初心者に5段階で説明するため、段階に分割したタイトル"]
    ret["outline_info"] = theme_abst["分割したタイトルの説明"]
    ret["image_url"] = d2c.images_url[-1]

    return ret

def run_generation_with_documents(framework):
    # output_dir 静的出力ファイルの保存場所の定義
    output_dir = "output/"
    output_dir = Path(output_dir+datetime.now().strftime('%Y%m%d_%H%M%S'))
    output_dir.mkdir(exist_ok=True, parents=True)

    # まずは勉強会の目標地点の概要を出力→dict型で出力結果を保持
    cgd = ChatGPTDialogue()
    cgd.clear_messages(need_default_messages=False)
    with open("system_instruction.md", "r", encoding="utf-8") as f:
        s = f.readlines()
        s = "".join(s)
    cgd.add_system_message(s)
    with open("user_ask_abstract_api.md", "r", encoding="utf-8") as f:
        s = f.readlines()
        s = "".join(s)
        framework_list = ["", "", ""]
        for i, t in enumerate(framework.split(",")):
            framework_list[i] = t
        s = s.replace("$$$FW001$$$", framework_list[0]).replace("$$$FW002$$$", framework_list[1]).replace("$$$FW003$$$", framework_list[2])
    cgd.add_user_message(s)
    cgd.add_assistant_message()
    if is_debug:
        print(cgd.show_current_messages())
    with open(output_dir.joinpath("assistant_out_abstract.txt"), "w", encoding="utf-8") as f:
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
            k_list.append(s.lstrip("*- "))
            state_num += 1
        elif state_num == 2:
            if "出力物内容" in s:
                state_num += 1
        elif state_num == 3 and len(s) >= 1:
            v_list.append(s)
        else:
            if "初心者に5段階で説明するため、段階に分割したタイトル" in k_list or "分割したタイトルの説明" in k_list:
                theme_abst["".join(k_list)] = v_list
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
    d2c.download_image_latest(output_dir.joinpath("theme_image.png"))

    # フロントエンド向け変数たち
    title = theme_abst["タイトル"]
    general_info = theme_abst["概要"]
    hashtag = theme_abst["ハッシュタグ"]
    outline = theme_abst["初心者に5段階で説明するため、段階に分割したタイトル"]
    outline_info = theme_abst["分割したタイトルの説明"]
    image_url = d2c.images_url[-1]

    print("タイトル", title)
    print("ハッシュタグ", hashtag)
    print("概要", general_info)
    print("アウトライン", outline)
    print("アウトラインの概要", outline_info)

    # 勉強会内容のドキュメント生成
    doc_dir = output_dir.joinpath("documents")
    doc_dir.mkdir(exist_ok=True, parents=True)
    editor = DocumentEditor(doc_dir)
    editor.add_h1(title)
    editor.add_h2("概要")
    editor.add_content(general_info)
    editor.add_h2("目次")
    for i, ol in enumerate(outline):
        info = outline_info[i]
        editor.add_content(f"1. [{ol}](chapter{i+1:02})")
        editor.add_content(f"    - {info}")    
    editor.write()

    # 分割した勉強会内容の詳細・実装例を示す
    for i, ol in enumerate(outline):
        cgdp = ChatGPTDialogue()
        cgdp.clear_messages(need_default_messages=False)
        with open("system_instruction.md", "r", encoding="utf-8") as f:
            s = f.readlines()
            s = "".join(s)
        cgdp.add_system_message(s)
        with open("user_ask_content.md", "r", encoding="utf-8") as f:
            s = f.readlines()
            s = "".join(s)
            s = s.replace("$$$タイトル$$$", title).replace("$$$概要$$$", general_info).replace("$$$順序$$$", "".join(outline)).replace("$$$選択項目$$$", ol)
        print(s)
        cgdp.add_user_message(s)
        cgdp.add_assistant_message()
        output_dir.joinpath(f"chapter{i+1:02}").mkdir(exist_ok=True, parents=True)
        with open(output_dir.joinpath(f"chapter{i+1:02}", "assistant_out.txt"), "w", encoding="utf-8") as f:
            f.write(cgdp.show_current_messages()[-1])
        
        # 分割した勉強会内容のドキュメント生成
        chapter_doc_dir = doc_dir.joinpath(f"chapter{i+1:02}")
        chapter_doc_dir.mkdir(exist_ok=True, parents=True)
        chapter_editor = DocumentEditor(chapter_doc_dir)
        chapter_state_num = 0
        chapter_k_list, chapter_v_list = [], []
        for s in cgdp.show_current_messages()[-1].split("\n"):
            if chapter_state_num == 0:
                if "出力物タイトル" in s:
                    chapter_state_num += 1
            elif chapter_state_num == 1:
                k_list.append(s.lstrip("*- "))
                chapter_state_num += 1
            elif chapter_state_num == 2:
                if "出力物内容" in s:
                    chapter_state_num += 1
            elif chapter_state_num == 3 and len(s) >= 1:
                v_list.append(s)
            else:
                k = "".join(k_list)
                v = "\n".join(v_list)
                if k == "教材タイトル":
                    chapter_editor.add_h1(v)
                else:
                    chapter_editor.add_h2(k)
                    chapter_editor.add_content(v)
                k_list, v_list = [], []
                chapter_state_num = 0
        chapter_editor.write()

    # 出力変数：jsonでかえす
    ret = {}
    ret["output_dir"] = str(output_dir)
    ret["title"] = theme_abst["タイトル"]
    ret["general_info"] = theme_abst["概要"]
    ret["hashtag"] = theme_abst["ハッシュタグ"]
    ret["outline"] = theme_abst["初心者に5段階で説明するため、段階に分割したタイトル"]
    ret["outline_info"] = theme_abst["分割したタイトルの説明"]
    ret["image_url"] = d2c.images_url[-1]

    return ret
