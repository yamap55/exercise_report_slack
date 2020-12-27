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
