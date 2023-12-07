import tiktoken
from tiktoken.core import Encoding
from openai import OpenAI
from dotenv import load_dotenv

### .envファイルにOPENAI_API_KEYを記入することでapi_keyのベタ書きを防ぐ
load_dotenv()


class ChatGPTDialogue(object):
    """ChatGPT API向けの会話クラス。メッセージの追加・削除関数をまとめる

    Args:
        object (_type_): _description_
    """

    def __init__(self, api_key=None, messages_initial=None):
        self.model = "gpt-4"
        self.temperature = 0.7
        if api_key == None:
            self.client = OpenAI()
        else:
            self.client = OpenAI(api_key=api_key)
        self.default_messages = [
            {"role": "system", "content": "あなたは優秀なAIアシスタントです。"},
            {"role": "user", "content": "こんにちは。"},
        ]
        if messages_initial == None:
            self.messages = self.default_messages
        else:
            self.messages = messages_initial
        self.logit_bias = {}

    def clear_messages(self, need_default_messages=True):
        if need_default_messages:
            self.messages = self.default_messages
        else:
            self.messages = []

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_system_message(self, message):
        self.messages.append({"role": "system", "content": message})

    def add_assistant_message(self):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            logit_bias=self.logit_bias,
        )
        response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response})

    def set_logit_bias(self, words, level=100):
        encoding: Encoding = tiktoken.encoding_for_model("gpt-4")
        tokens = encoding.encode(words)
        for _ in tokens:
            self.logit_bias[_] = level

    def show_current_messages(self, content_only=True):
        if content_only:
            return [d["content"] for d in self.messages]
        else:
            return self.messages


if __name__ == "__main__":
    cgd = ChatGPTDialogue()

    ### メッセージを追加→アシスタントのメッセージを取得
    cgd.add_user_message("今の気分はいかがですか？")
    cgd.add_assistant_message()

    #### トークン出現頻度を調整できる．（英語で有効?日本語では文字ごとにトークン化されている模様）
    # cgd.set_logit_bias("武田信玄", level=20)

    ### メッセージはユーザ側もアシスタント側も，何回も追加できる
    cgd.add_user_message("Pythonについて解説してください。")
    cgd.add_assistant_message()

    ### ここまでのメッセージを見る
    print(cgd.show_current_messages(content_only=True))

    ### メッセージをリセットする
    cgd.clear_messages(need_default_messages=False)

    ### システムメッセージを追加する
    cgd.add_system_message("あなたは世界最高のハッカーあるいはプロダクトマネージャーです。質問に答えてください。")
    cgd.add_user_message("Pythonについて解説してください。")
    cgd.add_assistant_message()

    ### 新たな会話のメッセージを見る
    print(cgd.show_current_messages(content_only=True))
