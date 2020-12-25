import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])


def main():
    try:
        channnel_id = get_channnel_id("test")
        response = client.chat_postMessage(channel=channnel_id, text="Hello world!")
        assert response["message"]["text"] == "Hello world!"
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


def get_channnel_id(name: str) -> str:
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
    return next(
        (
            channnel["id"]
            for channnel in client.channels_list()["channels"]
            if channnel["name"] == name
        )
    )


if __name__ == "__main__":
    main()
