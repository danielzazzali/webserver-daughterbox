import unittest
from unittest.mock import patch, MagicMock
from models.ethernet_model import set_ethernet_ip_and_mask


class TestEthernetModel(unittest.TestCase):

    @patch('subprocess.run')
    def test_set_ethernet_ip_and_mask_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        ip = "192.168.1.10"
        mask = "24"
        expected_result = {'ip': ip, 'mask': mask}
        self.assertEqual(set_ethernet_ip_and_mask(ip, mask), expected_result)

    @patch('subprocess.run')
    def test_set_ethernet_ip_and_mask_command_failure(self, mock_run):
        mock_run.side_effect = [MagicMock(returncode=1, stderr="Error"), MagicMock(returncode=0)]
        ip = "192.168.1.10"
        mask = "24"
        with self.assertRaises(RuntimeError):
            set_ethernet_ip_and_mask(ip, mask)



if __name__ == '__main__':
    unittest.main()