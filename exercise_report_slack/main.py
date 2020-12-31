"""main"""
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict

from slack_sdk.errors import SlackApiError

import exercise_report_slack.settings as settings
from exercise_report_slack.util.date_util import convert_timestamp_to_mmdda, get_last_monday
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
        oldest = get_last_monday().timestamp()
        messages = get_channel_message(channel_id, oldest)

        target_first_messages = [
            message for message in messages if __first_message_filtering_conditions(message)
        ]
        output_dict = {}
        for target_first_message in target_first_messages:
            target_messages = get_replies(channel_id, target_first_message)
            if not target_messages:
                # リプライがついていない場合
                date_str = convert_timestamp_to_mmdda(target_first_messages[1]["ts"])
                output_dict[date_str] = {}
                break

            first_message = target_messages.pop(0)
            date_str = datetime.fromtimestamp(float(first_message["thread_ts"])).strftime(
                "%m/%d（%a）"
            )
            d = defaultdict(list)
            for message in target_messages:
                d[message["user"]].append(message["text"])
            # 同日付は考慮していないため上書きする
            output_dict[date_str] = d

        res = post_message(channel_id, "先週の運動結果報告")
        ts = res["ts"]
        nl = "\n"

        sorted_items = sorted(output_dict.items(), key=lambda x: x[0])
        for date_str, user_messages in sorted_items:
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


if __name__ == "__main__":
    main()
