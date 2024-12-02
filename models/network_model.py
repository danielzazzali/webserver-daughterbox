import subprocess

from config.constants import NMCLI_GET_IP4_ADDRESS
from models.wifi_model import get_active_wifi_connection


def get_ip_and_mask() -> dict:
    """
    Retrieves the IP address and subnet mask for the specified network interface.

    Returns:
        dict: A dictionary containing the IP address and subnet mask with the key 'ip'.

    Raises:
        RuntimeError: If the command to fetch network details fails.
        ValueError: If the IP address and mask cannot be found.
    """

    connection = get_active_wifi_connection()["SSID"]

    command = NMCLI_GET_IP4_ADDRESS.format(connection)

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

    ip, mask = None, None

    for line in result.stdout.splitlines():
        if 'IP4.ADDRESS' in line:
            parts = line.split(':')
            ip_mask = parts[1].strip()
            ip, mask = ip_mask.split('/')
            break

    if ip is None or mask is None:
        raise ValueError("Could not find the IP address and mask for the connection 'AP'.")

    return {'ip': ip, 'mask': mask}