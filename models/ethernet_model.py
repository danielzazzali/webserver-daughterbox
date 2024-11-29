import subprocess
from typing import Dict

from config.config import get_env_variable
from config.constants import ETHERNET_CONNECTION, NMCLI_SET_IP4_ADDRESS


def set_ethernet_ip_and_mask(ip: str, mask: str) -> Dict[str, str]:
    """
    Sets the IP address and subnet mask for the Ethernet connection.

    Args:
        ip (str): The new IP address to set.
        mask (str): The new subnet mask to set.

    Returns:
        Dict[str, str]: A dictionary confirming the updated IP and mask.

    Raises:
        RuntimeError: If the command to change the IP address fails.
    """
    connection_name = get_env_variable(ETHERNET_CONNECTION)

    ip_with_mask = f"{ip}/{mask}"

    command = NMCLI_SET_IP4_ADDRESS.format(connection_name, ip_with_mask)

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to set IP address '{ip_with_mask}' for connection '{connection_name}'. Error: {result.stderr}")

    # Activate the updated connection
    subprocess.run(f"nmcli connection up {connection_name}", shell=True, check=True)

    return {'ip': ip, 'mask': mask}






