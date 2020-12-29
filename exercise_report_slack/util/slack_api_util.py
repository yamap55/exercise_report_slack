"""Slack APIを操作する関数群"""
from time import sleep
from typing import Any, Dict, List, Optional

from exercise_report_slack.settings import client


def get_channel_id(name: str) -> str:
    """
    指定されたチャンネルのチャンネルIDを取得する

    Parameters
    ----------
    name : str
        チャンネル名

    Returns
    -------
    str
        チャンネルID

    Raises
    -------
    ValueError
        存在しないチャンネル名の場合
    """
    # https://api.slack.com/methods/conversations.list
    try:
        return next(
            (
                channel["id"]
                for channel in client.conversations_list()["channels"]
                if channel["name"] == name
            )
        )
    except StopIteration:
        raise ValueError("not exists channel name.")


def get_user_name(user_id: str) -> str:
    """
    指定されたユーザIDのユーザ名を取得する

    Parameters
    ----------
    user_id : str
        ユーザID

    Returns
    -------
    str
        ユーザ名

    Raises
    -------
    SlackApiError
        存在しないユーザIDの場合
    """
    # https://api.slack.com/methods/users.info
    return client.users_info(user=user_id)["user"]["real_name"]


def post_message(
    channel_id: str, text: str, thread_ts: Optional[str] = None, mention_users: List[str] = []
) -> Dict[str, Any]:
    """
    指定されたチャンネルにメッセージをポストする

    Parameters
    ----------
    channel_id : str
        チャンネルID
    text : str
        ポストする内容
    thread_ts : Optional[str], optional
        リプライとしたい場合に指定するタイムスタンプ, by default None
    mention_users : List[str], optional
        メンションを指定するユーザID
        テキストの先頭に空白区切りで付与します
        2人以上が指定されている場合はメンション後に改行を追加します, by default []

    Returns
    -------
    Dict[str, Any]
        ポストしたメッセージのデータ
    """
    # https://api.slack.com/methods/chat.postMessage
    mentions = [f"<@{u}>" for u in mention_users]
    mentions_postfix = "\n" if len(mentions) > 1 else ""
    send_message = " ".join(mentions) + mentions_postfix + text

    res = client.chat_postMessage(channel=channel_id, text=send_message, thread_ts=thread_ts)
    return res.data


def get_channel_message(channel_id: str, oldest: float) -> List[Dict[str, Any]]:
    """
    指定されたチャンネルのメッセージを取得する

    Parameters
    ----------
    channel_id : str
        チャンネルID
    oldest : float
        取得を行う最初の時間

    Returns
    -------
    List[Dict[str, Any]]
        指定されたチャンネルのメッセージ
    """
    # https://api.slack.com/methods/conversations.history
    option = {"channel": channel_id, "oldest": oldest}
    response = client.conversations_history(**option).data
    messages_all = response["messages"]
    while response["has_more"]:
        sleep(1)  # need to wait 1 sec before next call due to rate limits
        response = client.conversations_history(
            **option, cursor=response["response_metadata"]["next_cursor"]
        ).data
        messages = response["messages"]
        messages_all = messages_all + messages
    return messages_all


def get_replies(channel_id: str, message: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    指定されたメッセージのリプライを返す

    Parameters
    ----------
    channel_id : str
        チャンネルID
    message : Dict[str, Any]
        リプライを取得する対象のメッセージ

    Returns
    -------
    List[Dict[str, Any]]
        リプライメッセージ
        リプライがついていない場合は空のリスト
    """
    # https://api.slack.com/methods/conversations.replies
    if "thread_ts" not in message:
        return []
    return client.conversations_replies(channel=channel_id, ts=message["thread_ts"]).data[
        "messages"
    ]
