from unittest import mock

import pytest
from exercise_report_slack.util.slack_api_util import get_channel_id, get_user_name
from slack_sdk.errors import SlackApiError


class TestGetUserName:
    @mock.patch("exercise_report_slack.util.slack_api_util.client.users_info")
    def test_nomal_case(self, mock_client):
        mock_client.return_value = {"user": {"real_name": "REAL_NAME"}}

        actual = get_user_name("USER_ID")
        expected = "REAL_NAME"

        assert actual == expected
        mock_client.assert_called_once_with(user="USER_ID")

    @mock.patch("exercise_report_slack.util.slack_api_util.client.users_info")
    def test_not_exists_user_id(self, mock_client):
        # APIにアクセスしたくないため、モックで例外を投げている
        # ユニットテストとしては意味がないが、仕様記載の意味で記載しておく
        mock_client.side_effect = SlackApiError("a", "b")

        with pytest.raises(SlackApiError):
            get_user_name("NOT_EXISTS_USER_ID")


class TestGetChannelId:
    @mock.patch("exercise_report_slack.util.slack_api_util.client.conversations_list")
    def test_nomal_case(self, mock_client):
        mock_client.return_value = {
            "channels": [
                {"name": "CHANNEL_NAME1", "id": "CHANNEL_ID1"},
                {"name": "CHANNEL_NAME2", "id": "CHANNEL_ID2"},
            ]
        }

        actual = get_channel_id("CHANNEL_NAME1")
        expected = "CHANNEL_ID1"

        assert actual == expected
        mock_client.assert_called_once_with()

    @mock.patch("exercise_report_slack.util.slack_api_util.client.conversations_list")
    def test_not_exists_channel_name(self, mock_client):
        mock_client.return_value = {"channels": []}

        with pytest.raises(ValueError):
            get_channel_id("CHANNEL_NAME")
