from slack_sdk.errors import SlackApiError

import exercise_report_slack.settings as settings

client = settings.client


def main():
    try:
        channnel_id = get_channel_id(settings.TARGET_CHANNEL)
        response = client.chat_postMessage(channel=channnel_id, text="Hello world!")
        assert response["message"]["text"] == "Hello world!"
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


def get_channel_id(name: str) -> str:
    """
    指定されたチャンネルのチャンネルIDを返す

    Parameters
    ----------
    name : str
        チャンネル名

    Returns
    -------
    str
        チャンネルID
    """
    # https://api.slack.com/methods/conversations.list
    return next(
        (
            channel["id"]
            for channel in client.conversations_list()["channels"]
            if channel["name"] == name
        )
    )


if __name__ == "__main__":
    main()
