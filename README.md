# yamanashiai2023codes

山梨AIハッカソン2023向けのツール群です。

## ChatGPT＋DALL-E 2
### つかいかた
1. .envファイルを作成する。.envファイルにはOPENAI_API_KEY=(APIキー)を記入する。
1. python main.pyを実行する。

### 入力プロンプト
* system_instruction.md: 背景となる指示のプロンプト．
* user_ask_abstract.md: 概要を出力をするためのプロンプト．

### 出力されるもの
* assistant_out_abstract.txt: 勉強会の概要
* theme_abst: 勉強会概要を辞書形式で保持（main.py内）
* theme_image.png: 勉強会に付随するイメージ

### 使用ライブラリ
* openai
* tiktoken (logit_bias設定関数にのみ使用)
