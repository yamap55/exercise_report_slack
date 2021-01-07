# exercise_report_slack

[![pytest](https://github.com/yamap55/exercise_report_slack/workflows/pytest/badge.svg?branch=master)](https://github.com/yamap55/exercise_report_slack/actions?query=workflow%3Apytest)
[![lint](https://github.com/yamap55/exercise_report_slack/workflows/lint/badge.svg)](https://github.com/yamap55/exercise_report_slack/actions?query=workflow%3Alint)

## 環境詳細

- Python : 3.8.7

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
TARGET_CHANNEL=target_channel
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

## ユニットテスト実行

```
pytest
```

## SlackAPI で必要な権限

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
