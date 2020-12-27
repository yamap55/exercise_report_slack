import locale
from datetime import datetime

import pytest
from exercise_report_slack.util.date_util import convert_timestamp_to_mmdda, get_last_monday


class TestGetLastMonday:
    def test_nomal_case(self):
        d = datetime.strptime("2020/01/23 4:5:6", "%Y/%m/%d %H:%M:%S")
        assert d.weekday() == 3  # 2020/01/23 は木曜

        actual = get_last_monday(d)
        expected = datetime.strptime("2020/01/13", "%Y/%m/%d")

        assert actual == expected


class TestConvertTimestampToMmdda:
    @pytest.fixture(scope="function", autouse=True)
    def setLocale(self):
        default_locale = "C.UTF-8"
        locale.setlocale(locale.LC_TIME, default_locale)
        yield
        locale.setlocale(locale.LC_TIME, default_locale)

    def test_nomal_case(self):
        ts = datetime.strptime("2020/01/23 4:5:6", "%Y/%m/%d %H:%M:%S").timestamp()
        actual = convert_timestamp_to_mmdda(str(ts))
        expected = "01/23（Thu）"

        assert actual == expected

    def test_jajp_locale(self):
        locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")

        ts = datetime.strptime("2020/01/23 4:5:6", "%Y/%m/%d %H:%M:%S").timestamp()
        actual = convert_timestamp_to_mmdda(str(ts))
        expected = "01/23（木）"

        assert actual == expected
