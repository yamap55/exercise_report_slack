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


def __first_message_filtering_conditions(message: Dict[str, Any]) -> bool:
    return (
        (message["user"] == settings.TARGET_SLACK_BOT_NAME)  # 既定の発言者である事
        & (message["text"] == settings.TARGET_SLACK_MESSAGE)  # 既定のメッセージである事
        # & ('thread_ts' in message) # スレッドが続いている事
    )


def main() -> None:
    """main"""
    try:
        channel_id = get_channel_id(settings.TARGET_CHANNEL)
        monday, sunday = get_last_week_range()
        oldest = monday.timestamp()
        latest = sunday.timestamp()
        messages = get_channel_message(channel_id, oldest, latest)

        target_first_messages = [
            message for message in messages if __first_message_filtering_conditions(message)
        ]
        message_by_date = __get_message_by_date(channel_id, target_first_messages)

        # まとめメッセージをポスト
        res = post_message(channel_id, settings.POST_FIRST_MESSAGE)
        ts = res["ts"]
        nl = "\n"

        # 日付毎にメッセージをまとめ、元メッセージに対してリプライを行う
        # NOTE: 後でリファクタリング
        for date_str, user_messages in message_by_date:
            messsages = [
                f"{get_user_name(user_id)}{nl}{nl.join(messages)}"
                for user_id, messages in user_messages.items()
            ]
            message = date_str + "\n" + "\n\n".join(messsages)
            post_message(channel_id, message, thread_ts=ts)

    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
    except ValueError as e:
        print(e)


def __f(channel_id, target_first_message) -> Tuple[str, Dict[str, List[str]]]:
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


if __name__ == "__main__":
    main()
