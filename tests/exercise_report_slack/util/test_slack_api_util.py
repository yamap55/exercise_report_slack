from unittest import mock

import pytest
from exercise_report_slack.util.slack_api_util import get_channel_id, get_user_name, post_message
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


class TestPostMessage:
    @pytest.fixture(autouse=True)
    def setUp(self):
        class ReturnValue:
            data = {"ok": True, "ts": "1234567890.000002", "message": {}}

        with mock.patch(
            "exercise_report_slack.util.slack_api_util.client.chat_postMessage",
            return_value=ReturnValue(),
        ) as mock_method:
            self.mock_method = mock_method
            yield

    def test_all_args(self):
        actual = post_message(
            "CHANNEL_ID",
            "POST_MESSAGE",
            thread_ts="1234567890.000001",
            mention_users=["USER_ID_1", "USER_ID_2"],
        )
        expected = {"ok": True, "ts": "1234567890.000002", "message": {}}

        assert actual == expected
        self.mock_method.assert_called_once_with(
            channel="CHANNEL_ID",
            text="<@USER_ID_1> <@USER_ID_2>\nPOST_MESSAGE",
            thread_ts="1234567890.000001",
        )

    def test_required_args_only(self):
        actual = post_message("CHANNEL_ID", "POST_MESSAGE")
        expected = {"ok": True, "ts": "1234567890.000002", "message": {}}

        assert actual == expected
        self.mock_method.assert_called_once_with(
            channel="CHANNEL_ID", text="POST_MESSAGE", thread_ts=None
        )
