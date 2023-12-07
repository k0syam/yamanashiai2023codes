# yamanashiai2023codes

山梨AIハッカソン2023向けのツール群です。

## ChatGPT
### つかいかた
* .envファイルを作成する。.envファイルにはOPENAI_API_KEY=(APIキー)を記入する。
* python main.pyを実行する。-> assistant_out.mdが更新される

### プロンプト
* system_instruction.md, user_ask.md

### 使用ライブラリ
* openai
* tiktoken (logit_bias設定関数にのみ使用)
