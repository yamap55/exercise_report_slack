"""application settings"""
import locale
import os

from slack_sdk import WebClient

# データの収集及び発言を行うチャンネル名
TARGET_CHANNEL = os.environ["TARGET_CHANNEL"]
# 集計対象の発言を行うユーザ名（ボットユーザ名）
TARGET_SLACK_BOT_NAME = "USLACKBOT"
# 集計の対象とする発言（この発言のスレッド内容を集計とする）
TARGET_SLACK_MESSAGE = "リマインダー : 運動しましょう！（運動したらこのスレッドに内容を記載してください）"
# 運動目標を記載する元発言（この発言のスレッド内容を運動目標とする）
TARGET_SLACK_MESSAGE_GOAL = "リマインダー : 今週の運動目標をこのスレッドに記載しましょう！"
# 運動目標を転記する際のPrefix
GOAL_MESSAGE_POST_PREFIX = "運動目標"
# 集計の報告をはじめるメッセージ
POST_FIRST_MESSAGE = "先週の運動結果報告"

locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
