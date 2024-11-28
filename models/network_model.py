import re
import subprocess
from typing import List, Dict

from config.config import get_env_variable
from config.constants import IP_COMMAND_TEMPLATE, ETHERNET_NETWORK_INTERFACE_KEY, ETHERNET_CONNECTION_KEY


def get_ip_and_mask() -> dict:
    """
    Retrieves the IP address and subnet mask for the specified network interface.

    Returns:
        dict: A dictionary containing the IP address and subnet mask with the key 'ip'.

    Raises:
        RuntimeError: If the command to fetch network details fails.
        ValueError: If the IP address and mask cannot be found.
    """

    interface = get_env_variable(ETHERNET_NETWORK_INTERFACE_KEY)

    command = IP_COMMAND_TEMPLATE.format(interface)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

    ip, mask = None, None

    for line in result.stdout.splitlines():
        if 'inet ' in line:
            parts = line.strip().split()
            ip_mask = parts[1]
            ip, mask = ip_mask.split('/')
            break

    if ip is None or mask is None:
        raise ValueError(f"Could not find the IP address and mask for the interface '{interface}'.")

    return {'ip': ip, 'mask': mask}


def remembered_connections() -> List[Dict[str, str]]:
    """
    Retrieves the names and autoconnect status of Wi-Fi connections.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing the name and autoconnect status of Wi-Fi connections.

    Raises:
        RuntimeError: If the command to fetch Wi-Fi connections fails.
    """
    command = "nmcli -f NAME,AUTOCONNECT,TYPE connection show | grep 'wifi'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

    wifi_connections: List[Dict[str, str]] = []
    for line in result.stdout.splitlines():
        # Regex to match the name and autoconnect status
        match = re.match(r"^(.*?)\s{2,}(yes|no)\s", line)
        if match:
            name = match.group(1).strip()
            autoconnect = match.group(2).strip()
            wifi_connections.append({'name': name, 'autoconnect': autoconnect})

    return wifi_connections


def scan_wifi_networks() -> list:
    """
    Retrieves the list of Wi-Fi networks with their SSID, signal strength, and active status.

    Returns:
        list: A list of dictionaries containing SSID, signal strength, and active status.

    Raises:
        RuntimeError: If the command to fetch Wi-Fi networks fails.
    """
    command = "nmcli -f SSID,SIGNAL,ACTIVE device wifi"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

    wifi_networks = []
    lines = result.stdout.splitlines()
    for line in lines[1:]:  # Skip the header line
        parts = line.split()
        if len(parts) >= 3:
            ssid = parts[0]
            signal = parts[1]
            active = parts[2]
            wifi_networks.append({'SSID': ssid, 'SIGNAL': signal, 'ACTIVE': active})

    return wifi_networks


def get_active_wifi_network() -> dict:
    """
    Retrieves the current active Wi-Fi network with its SSID, signal strength, and active status.

    Returns:
        dict: A dictionary containing SSID, signal strength, and active status of the current active Wi-Fi network.

    Raises:
        RuntimeError: If the command to fetch Wi-Fi networks fails.
    """
    command = "nmcli -f SSID,SIGNAL,ACTIVE device wifi | grep 'yes'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

    lines = result.stdout.splitlines()
    if not lines:
        return {}

    parts = lines[0].split()
    if len(parts) >= 3:
        ssid = parts[0]
        signal = parts[1]
        active = parts[2]
        return {'SSID': ssid, 'SIGNAL': signal, 'ACTIVE': active}

    return {}


def delete_connection(connection_name: str):
    """
    Deletes a network connection using nmcli.

    Args:
        connection_name (str): The name of the connection to delete.

    Raises:
        RuntimeError: If the command to delete the connection fails.
    """
    command = f"nmcli connection delete {connection_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to delete connection '{connection_name}'. Error: {result.stderr}")

    print(f"Connection '{connection_name}' deleted successfully.")


def connect_to_known_network(connection_name: str):
    """
    Connects to a known network using nmcli.

    Args:
        connection_name (str): The name of the known network to connect to.

    Raises:
        RuntimeError: If the command to connect to the network fails.
    """
    command = f"nmcli connection up {connection_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to connect to network '{connection_name}'. Error: {result.stderr}")

    print(f"Connected to network '{connection_name}' successfully.")


def disconnect_from_network(connection_name: str):
    """
    Disconnects from a network using nmcli.

    Args:
        connection_name (str): The name of the network to disconnect from.

    Raises:
        RuntimeError: If the command to disconnect from the network fails.
    """
    command = f"nmcli connection down {connection_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to disconnect from network '{connection_name}'. Error: {result.stderr}")

    print(f"Disconnected from network '{connection_name}' successfully.")

def set_autoconnect_off(connection_name: str):
    """
    Sets the autoconnect property to 'no' for a specified network connection.

    Args:
        connection_name (str): The name of the connection to update.

    Raises:
        RuntimeError: If the command to update the connection fails.
    """
    command = f"nmcli connection modify '{connection_name}' connection.autoconnect no"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to set autoconnect to 'no' for connection '{connection_name}'. Error: {result.stderr}")

    print(f"Autoconnect set to 'no' for connection '{connection_name}' successfully.")


def set_autoconnect_on(connection_name: str):
    """
    Sets the autoconnect property to 'yes' for a specified network connection.

    Args:
        connection_name (str): The name of the connection to update.

    Raises:
        RuntimeError: If the command to update the connection fails.
    """
    command = f"nmcli connection modify '{connection_name}' connection.autoconnect yes"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to set autoconnect to 'yes' for connection '{connection_name}'. Error: {result.stderr}")

    print(f"Autoconnect set to 'yes' for connection '{connection_name}' successfully.")

def get_eth_ip_and_mask() -> Dict[str, str]:
    """
    Retrieves the IP address and subnet mask of the Ethernet connection.

    Returns:
        Dict[str, str]: A dictionary containing the IP address and subnet mask with the keys 'ip' and 'mask'.

    Raises:
        RuntimeError: If the command to fetch the IP address fails.
        ValueError: If the IP address and mask cannot be found.
    """
    connection_name = get_env_variable(ETHERNET_CONNECTION_KEY)

    command = f"nmcli -t -f IP4.ADDRESS connection show {connection_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

    ip_address = result.stdout.strip()
    if not ip_address:
        raise ValueError(f"Could not find the IP address for the Ethernet connection '{connection_name}'.")

    clean_ip_address = ip_address.split(':')[-1].strip()

    ip, mask = clean_ip_address.split('/') if '/' in clean_ip_address else (clean_ip_address, None)

    return {'ip': ip, 'mask': mask if mask else ''}

def set_eth_ip_and_mask(ip: str, mask: str) -> Dict[str, str]:
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
    connection_name = get_env_variable(ETHERNET_CONNECTION_KEY)
    ip_with_mask = f"{ip}/{mask}"
    command = f"nmcli connection modify {connection_name} ipv4.addresses {ip_with_mask} ipv4.method manual"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to set IP address '{ip_with_mask}' for connection '{connection_name}'. Error: {result.stderr}")

    # Activate the updated connection
    subprocess.run(f"nmcli connection up {connection_name}", shell=True, check=True)

    return {'ip': ip, 'mask': mask}


def connect_to_new_ap(ssid: str, password: str) -> Dict[str, str]:
    """
    Connects to a new Wi-Fi network using the given SSID and password.

    Args:
        ssid (str): The SSID of the Wi-Fi network.
        password (str): The password for the Wi-Fi network.

    Returns:
        Dict[str, str]: A dictionary confirming the connected SSID.

    Raises:
        RuntimeError: If the command to connect fails.
    """
    # Attempt to connect using nmcli
    command = f"nmcli dev wifi connect '{ssid}' password '{password}'"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to connect to Wi-Fi network '{ssid}'. Error: {result.stderr}")

    return {'message': f"Connected to Wi-Fi network '{ssid}' successfully."}




