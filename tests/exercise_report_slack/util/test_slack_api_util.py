from unittest import mock

from exercise_report_slack.util.slack_api_util import get_user_name


class TestGetUserName:
    @mock.patch("exercise_report_slack.util.slack_api_util.client.users_info")
    def test_nomal_case(self, mock_client):
        mock_client.return_value = {"user": {"real_name": "REAL_NAME"}}

        actual = get_user_name("USER_ID")
        expected = "REAL_NAME"

        assert actual == expected
        mock_client.assert_called_once_with(user="USER_ID")
