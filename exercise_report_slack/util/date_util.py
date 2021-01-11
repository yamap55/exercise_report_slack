"""日付関連共通関数群"""

from datetime import datetime, timedelta, timezone
from typing import Tuple

JST = timezone(timedelta(hours=+9), "JST")


def get_last_week_range(now=None) -> Tuple[datetime, datetime]:
    """
    先週の範囲（月曜から日曜）をdatetimeで返す

    Parameters
    ----------
    now : datetime, optional
        指定日付, by default datetime.now()

    Returns
    -------
    Tuple[datetime, datetime]
        先週の月曜日、先週の日曜日（時間はそれぞれ0:0:0、23:59:59）
        2021/01/12（火）の場合、2021/01/04（月）, 2021/01/10（日）が返される
    """
    now = now if now else datetime.now(JST)
    # 今週の月曜日までの日数+7 を引いている = 先週の月曜日
    last_monday_date = now - timedelta(days=now.weekday() + 7)
    # 今週の月曜日までの日数+1 を引いている = 先週の日曜日
    last_sunday_date = now - timedelta(days=now.weekday() + 1)
    last_monday = datetime(
        year=last_monday_date.year, month=last_monday_date.month, day=last_monday_date.day
    )
    last_sunday = datetime(
        year=last_sunday_date.year,
        month=last_sunday_date.month,
        day=last_sunday_date.day,
        hour=23,
        minute=59,
        second=59,
        microsecond=999999,
    )
    return last_monday, last_sunday


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
    return datetime.fromtimestamp(float(ts), tz=JST).strftime("%m/%d（%a）")
