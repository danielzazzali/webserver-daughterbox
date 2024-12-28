import unittest
from unittest.mock import patch, MagicMock
from models.network_model import get_ip_and_mask


class TestNetworkModel(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_ip_and_mask_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="IP4.ADDRESS[1]: 192.168.1.2/24\n")
        expected_result = {'ip': '192.168.1.2', 'mask': '24'}
        self.assertEqual(get_ip_and_mask('AP'), expected_result)

    @patch('subprocess.run')
    def test_get_ip_and_mask_command_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stderr="Error")
        with self.assertRaises(RuntimeError):
            get_ip_and_mask('AP')

    @patch('subprocess.run')
    def test_get_ip_and_mask_value_error(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="Some other output\n")
        with self.assertRaises(ValueError):
            get_ip_and_mask('AP')


if __name__ == '__main__':
    unittest.main()