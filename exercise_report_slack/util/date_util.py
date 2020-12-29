"""日付関連共通関数群"""

from datetime import datetime

from dateutil import relativedelta


def get_last_monday(now=None) -> datetime:
    """
    指定日付の1週間前の月曜日を取得

    Parameters
    ----------
    now : datetime, optional
        指定日付, by default datetime.now()

    Returns
    -------
    datetime
        1週間前の月曜日
    """
    now = now if now else datetime.now()
    return now - relativedelta.relativedelta(
        weeks=1, days=now.weekday(), hour=0, minute=0, second=0
    )


def convert_timestamp_to_mmdda(ts: str) -> str:
    """
    文字列のタイムスタンプを「MM/DD（a）」形式に変換

    Parameters
    ----------
    ts : str
        タイムスタンプ

    Returns
    -------
    str
        「MM/DD（a）」形式の日付
        例: 12/23（水）
    """
    return datetime.fromtimestamp(float(ts)).strftime("%m/%d（%a）")
