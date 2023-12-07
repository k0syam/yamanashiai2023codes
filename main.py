from chatgpt import ChatGPTDialogue


def main_generate_theme():
    cgd = ChatGPTDialogue()
    cgd.clear_messages(need_default_messages=False)
    with open("system_instruction.md", "r", encoding="utf-8") as f:
        s = f.readlines()
        s = "".join(s)
    cgd.add_system_message(s)
    with open("user_ask.md", "r", encoding="utf-8") as f:
        s = f.readlines()
        s = "".join(s)
    cgd.add_user_message(s)
    cgd.add_assistant_message()
    print(cgd.show_current_messages())
    with open("assistant_out.md", "w", encoding="utf-8") as f:
        f.write(cgd.show_current_messages()[-1])


if __name__ == "__main__":
    main_generate_theme()
