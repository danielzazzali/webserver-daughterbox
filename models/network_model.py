import subprocess

from config.constants import NMCLI_GET_IP4_ADDRESS


def get_ip_and_mask(connection) -> dict:
    """
    Retrieves the IP address and subnet mask for the specified network interface.

    Args:
        connection (str): The name of the network connection (e.g., 'WLAN', 'ETH').

    Returns:
        dict: A dictionary containing the IP address and subnet mask with the key 'ip'.

    Raises:
        RuntimeError: If the command to fetch network details fails.
        ValueError: If the IP address and mask cannot be found.
    """

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