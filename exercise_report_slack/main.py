"""main"""
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Tuple

from slack_sdk.errors import SlackApiError

import exercise_report_slack.settings as settings
from exercise_report_slack.util.date_util import convert_timestamp_to_mmdda, get_last_week_range
from exercise_report_slack.util.slack_api_util import (
    get_channel_id,
    get_channel_message,
    get_replies,
    get_user_name,
    post_message,
)

client = settings.client


def __get_target_messages(
    messages: List[Dict[str, Any]], user: str, target_message: str
) -> List[Dict[str, Any]]:
    """
    対象のメッセージ群から指定のユーザが指定の発言をしているメッセージを取得

    Parameters
    ----------
    messages : List[Dict[str, Any]]
        探索対象とするメッセージ群
    user : str
        ユーザID
    target_message : str
        探索対象とするメッセージ（完全一致）

    Returns
    -------
    List[Dict[str, Any]]
        メッセージ群
    """
    return [
        message
        for message in messages
        if (message["user"] == user) & (message["text"] == target_message)
    ]


def main() -> None:
    """main"""
    try:
        channel_id = get_channel_id(settings.TARGET_CHANNEL)
        monday, sunday = get_last_week_range()
        oldest = monday.timestamp()
        latest = sunday.timestamp()
        messages = get_channel_message(channel_id, oldest, latest)

        # 目標設定取得
        target_goal_messages = __get_target_messages(
            messages, settings.TARGET_SLACK_BOT_NAME, settings.TARGET_SLACK_MESSAGE_GOAL
        )
        goal_messages = __get_post_messages(
            channel_id, target_goal_messages, settings.GOAL_MESSAGE_POST_PREFIX
        )

        # 運動実績取得
        target_first_messages = __get_target_messages(
            messages, settings.TARGET_SLACK_BOT_NAME, settings.TARGET_SLACK_MESSAGE
        )
        experience_messages = __get_post_messages(channel_id, target_first_messages)

        print("goal_messages:", goal_messages)
        print("experience_messages:", experience_messages)

        # まとめメッセージをポスト
        res = post_message(channel_id, settings.POST_FIRST_MESSAGE)
        ts = res["ts"]
        # まとめメッセージに対してリプライ
        for message in goal_messages + experience_messages:
            post_message(channel_id, message, thread_ts=ts)

    except SlackApiError as e:
        # TODO: エラーハンドリングはデフォルトのままなのでもう少し考慮が必要
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
    except ValueError as e:
        print(e)


def __f(channel_id: str, target_first_message: Dict[str, Any]) -> Tuple[str, Dict[str, List[str]]]:
    target_messages = get_replies(channel_id, target_first_message)
    if not target_messages:
        # リプライがついていない場合
        date_str = convert_timestamp_to_mmdda(target_first_message["ts"])
        return date_str, {}
    first_message = target_messages.pop(0)
    date_str = datetime.fromtimestamp(float(first_message["thread_ts"])).strftime("%m/%d（%a）")
    d = defaultdict(list)
    for message in target_messages:
        d[message["user"]].append(message["text"])
    return date_str, d


def __get_message_by_date(
    channel_id: str, target_first_messages: List[Dict[str, Any]]
) -> List[Tuple[str, Dict[str, List[str]]]]:
    """
    日付、ユーザ毎のメッセージを取得

    Parameters
    ----------
    channel_id : str
        チャンネルID
    target_first_messages : List[Dict[str, Any]]
        集計対象のメッセージ一覧

    Returns
    -------
    List[Tuple[str, Dict[str, List[str]]]]
        日付毎、ユーザ毎のメッセージ
        [(日付,{ユーザID: [メッセージ]}),]
    """
    output_dict: Dict[str, Dict[str, List[str]]] = dict(
        # 同日付は考慮していないため上書きする
        [__f(channel_id, target_first_message) for target_first_message in target_first_messages]
    )
    # 最新日付が上位にきているため、日付を基準にしてソート
    result = sorted(output_dict.items(), key=lambda x: x[0])
    return result


def __get_post_messages(
    channel_id: str, target_first_messages: List[Dict[str, Any]], prefix: str = None
) -> List[str]:
    """
    POSTを行うメッセージ群を取得

    Parameters
    ----------
    channel_id : str
        チャンネルID
    target_first_messages : List[Dict[str, Any]]
        集計対象のメッセージ一覧
    prefix : str, optional
        POSTメッセージのprefix, by default 日付（MM/DD）

    Returns
    -------
    List[str]
        ポストするメッセージ群
    """
    message_by_date = __get_message_by_date(channel_id, target_first_messages)
    nl = "\n"

    def f(prefix, user_messages):
        messsages = [
            f"{get_user_name(user_id)}{nl}{nl.join(messages)}"
            for user_id, messages in user_messages.items()
        ]
        return prefix + "\n" + "\n\n".join(messsages)

    return [
        f(prefix if prefix else date_str, user_messages)
        for date_str, user_messages in message_by_date
    ]


if __name__ == "__main__":
    main()
