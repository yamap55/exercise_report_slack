# exercise_report_slack

## 環境詳細

- Python : 3.8.6

### 事前準備

- Docker インストール
- VSCode インストール
- VSCode の拡張機能「Remote - Containers」インストール
  - https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
- 本リポジトリの clone
- `.env` ファイルを空ファイルでプロジェクト直下に作成

### 環境変数設定

```
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 開発手順

1. VSCode 起動
2. 左下の緑色のアイコンクリック
3. 「Remote-Containersa: Reopen in Container」クリック
4. しばらく待つ
   - 初回の場合コンテナ image の取得や作成が行われる
5. 起動したら開発可能

## 実行

```
python -m exercise_report_slack.main
```

## SlackAPI1 で必要な権限

```
channels:history
channels:read
chat:write
chat:write.public
groups:history
groups:read
im:read
mpim:history
mpim:read
users:read
```
