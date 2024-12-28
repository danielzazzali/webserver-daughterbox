import unittest
from unittest.mock import patch, MagicMock
from models.wifi_model import remembered_wifi_connections, scan_wifi_networks, get_active_wifi_connection, \
    connect_to_new_ap, disconnect_from_wifi_connection, connect_to_known_wifi_connection, \
    delete_known_wifi_connection, set_autoconnect_on_to_wifi_connection, set_autoconnect_off_to_wifi_connection


class TestWifiModel(unittest.TestCase):

    @patch('subprocess.run')
    def test_remembered_wifi_connections(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="Home:yes\nOffice:no")
        expected_result = [{'name': 'Home', 'autoconnect': 'yes'}, {'name': 'Office', 'autoconnect': 'no'}]
        self.assertEqual(remembered_wifi_connections(), expected_result)

    @patch('subprocess.run')
    def test_scan_wifi_networks(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="SSID1:70:yes:B8:27:EB:00:00:01\nSSID2:50:no:B8:27:EB:00:00:02")
        expected_result = [{'SSID': 'SSID1', 'SIGNAL': '70', 'ACTIVE': 'yes'}, {'SSID': 'SSID2', 'SIGNAL': '50', 'ACTIVE': 'no'}]
        self.assertEqual(scan_wifi_networks(), expected_result)

    @patch('subprocess.run')
    def test_get_active_wifi_connection(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="SSID1:70:yes")
        expected_result = {'SSID': 'SSID1', 'SIGNAL': '70', 'ACTIVE': 'yes'}
        self.assertEqual(get_active_wifi_connection(), expected_result)

    @patch('subprocess.run')
    def test_connect_to_new_ap(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        ssid = "TestSSID"
        password = "TestPassword"
        expected_result = {'message': f"Connected to Wi-Fi network '{ssid}' successfully."}
        self.assertEqual(connect_to_new_ap(ssid, password), expected_result)

    @patch('subprocess.run')
    def test_disconnect_from_wifi_connection(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        connection_name = "TestConnection"
        disconnect_from_wifi_connection(connection_name)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_connect_to_known_wifi_connection(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        connection_name = "TestConnection"
        connect_to_known_wifi_connection(connection_name)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_delete_known_wifi_connection(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        connection_name = "TestConnection"
        delete_known_wifi_connection(connection_name)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_set_autoconnect_on_to_wifi_connection(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        connection_name = "TestConnection"
        set_autoconnect_on_to_wifi_connection(connection_name)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_set_autoconnect_off_to_wifi_connection(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        connection_name = "TestConnection"
        set_autoconnect_off_to_wifi_connection(connection_name)
        mock_run.assert_called_once()


if __name__ == '__main__':
    unittest.main()