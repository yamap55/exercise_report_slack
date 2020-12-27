"""日付関連共通関数群"""

from datetime import datetime

from dateutil import relativedelta


def get_last_monday() -> datetime:
    """
    先週の月曜日を返す

    Returns
    -------
    datetime
        先週の月曜日
    """
    now = datetime.now()
    return now - relativedelta.relativedelta(
        weeks=1, days=now.weekday(), hour=0, minute=0, second=0
    )


def convert_timestamp_to_mmdda(ts: str) -> str:
    """
    文字列のタイムスタンプを「MM/DD（a）」形式に変換する

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
