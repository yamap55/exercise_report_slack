"""application settings"""
import locale
import os

from slack_sdk import WebClient

# データの収集及び発言を行うチャンネル名
TARGET_CHANNEL = "test"
# 集計対象の発言を行うユーザ名（ボットユーザ名）
TARGET_SLACK_BOT_NAME = "USLACKBOT"
# 集計の対象とする発言（この発言のスレッド内容を集計とする）
TARGET_SLACK_MESSAGE = "Reminder: hoge."
# 集計の報告をはじめるメッセージ
POST_FIRST_MESSAGE = "先週の運動結果報告"


locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
