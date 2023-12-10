# yamanashiai2023codes

山梨AIハッカソン2023向けのツール群です。（山本勘助晴幸バックエンド）

## ChatGPT＋DALL-E 2
### つかいかた
1. .envファイルを作成する。.envに以下の項目を各トークンAPIキーに加えて、GitHubのリポジトリも事前に準備すること！
  * OPENAI_API_KEY=(OPENAIのAPIキー)
  * GITHUB_TOKEN=(GitHubのトークン)
  * GITHUB_REPO_OWNER=(GitHubのユーザ名)
  * GITHUB_REPO_NAME=(GitHubのリポジトリ名)
1. python main.pyを実行する。(ローカル実行の場合)
1. uvicorn api:app --reload (APIたちあげ)
  * GET http://localhost:8000 -> jsonかえってきます

### 入力プロンプト
* system_instruction.md: 背景となる指示のプロンプト．
* user_ask_abstract.md: 概要を出力をするためのプロンプト．

### 出力されるもの(output/実行時刻のフォルダが作られる)
* assistant_out_abstract.txt: 勉強会の概要
* theme_abst: 勉強会概要を辞書形式で保持（main.py内）
* theme_image.png: 勉強会に付随するイメージ

### 使用ライブラリ
* openai
* tiktoken (logit_bias設定関数にのみ使用)
