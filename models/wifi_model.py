import subprocess
from typing import List, Dict, Any

from config.constants import NMCLI_GET_WIFI_CONNECTIONS, NMCLI_SCAN_WIFI_NETWORKS, NMCLI_GET_ACTIVE_WIFI_CONNECTION, \
    NMCLI_CONNECT_TO_NEW_AP, NMCLI_DISCONNECT_FROM_WIFI_CONNECTION, NMCLI_CONNECT_TO_KNOWN_WIFI_CONNECTION, \
    NMCLI_DELETE_KNOWN_WIFI_CONNECTION, NMCLI_SET_AUTOCONNECT_ON_TO_WIFI_CONNECTION, \
    NMCLI_SET_AUTOCONNECT_OFF_TO_WIFI_CONNECTION, MAC_PREFIX_FOR_RASPBERRY


def remembered_wifi_connections() -> dict[Any, Any] | list[dict[str, str]]:
    """
    Retrieves the names and autoconnect status of Wi-Fi connections.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing the name and autoconnect status of Wi-Fi connections.

    Raises:
        RuntimeError: If the command to fetch Wi-Fi connections fails.
    """
    command = NMCLI_GET_WIFI_CONNECTIONS
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0 and not result.stdout:
        return {}

    if result.returncode != 0:
        raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

    wifi_connections: List[Dict[str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(':')
        if len(parts) >= 2:
            name = parts[0].strip()
            autoconnect = parts[1].strip()
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
    command = NMCLI_SCAN_WIFI_NETWORKS
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

    wifi_networks = []
    for line in result.stdout.splitlines():
        parts = line.split(':')
        if len(parts) >= 4:
            ssid = parts[0].strip()
            signal = parts[1].strip()
            active = parts[2].strip()
            bssid_1 = parts[3].strip()
            bssid_2 = parts[4].strip()
            bssid_3 = parts[5].strip()
            bssid_4 = parts[6].strip()
            bssid_5 = parts[7].strip()
            bssid_6 = parts[8].strip()

            bssid = f"{bssid_1}:{bssid_2}:{bssid_3}:{bssid_4}:{bssid_5}:{bssid_6}".replace("\:", ":")

            if bssid.startswith(MAC_PREFIX_FOR_RASPBERRY):
                wifi_networks.append({'SSID': ssid, 'SIGNAL': signal, 'ACTIVE': active})

    return wifi_networks


def get_active_wifi_connection() -> dict:
    """
    Retrieves the current active Wi-Fi network with its SSID, signal strength, and active status.

    Returns:
        dict: A dictionary containing SSID, signal strength, and active status of the current active Wi-Fi network.

    Raises:
        RuntimeError: If the command to fetch Wi-Fi networks fails.
    """
    command = NMCLI_GET_ACTIVE_WIFI_CONNECTION
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0 and not result.stdout:
        return {}

    if result.returncode != 0:
        raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

    lines = result.stdout.splitlines()
    if not lines:
        return {}

    parts = lines[0].split(':')
    if len(parts) >= 3:
        ssid = parts[0]
        signal = parts[1]
        active = parts[2]
        return {'SSID': ssid, 'SIGNAL': signal, 'ACTIVE': active}

    return {}


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
    command = NMCLI_CONNECT_TO_NEW_AP.format(ssid, password)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to connect to Wi-Fi network '{ssid}'. Error: {result.stderr}")

    return {'message': f"Connected to Wi-Fi network '{ssid}' successfully."}


def disconnect_from_wifi_connection(connection_name: str):
    """
    Disconnects from a network using nmcli.

    Args:
        connection_name (str): The name of the network to disconnect from.

    Raises:
        RuntimeError: If the command to disconnect from the network fails.
    """
    command = NMCLI_DISCONNECT_FROM_WIFI_CONNECTION.format(connection_name)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to disconnect from network '{connection_name}'. Error: {result.stderr}")

    print(f"Disconnected from network '{connection_name}' successfully.")


def connect_to_known_wifi_connection(connection_name: str):
    """
    Connects to a known network using nmcli.

    Args:
        connection_name (str): The name of the known network to connect to.

    Raises:
        RuntimeError: If the command to connect to the network fails.
    """
    command = NMCLI_CONNECT_TO_KNOWN_WIFI_CONNECTION.format(connection_name)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to connect to network '{connection_name}'. Error: {result.stderr}")

    print(f"Connected to network '{connection_name}' successfully.")


def delete_known_wifi_connection(connection_name: str):
    """
    Deletes a network connection using nmcli.

    Args:
        connection_name (str): The name of the connection to delete.

    Raises:
        RuntimeError: If the command to delete the connection fails.
    """
    command = NMCLI_DELETE_KNOWN_WIFI_CONNECTION.format(connection_name)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to delete connection '{connection_name}'. Error: {result.stderr}")

    print(f"Connection '{connection_name}' deleted successfully.")


def set_autoconnect_on_to_wifi_connection(connection_name: str):
    """
    Sets the autoconnect property to 'yes' for a specified network connection.

    Args:
        connection_name (str): The name of the connection to update.

    Raises:
        RuntimeError: If the command to update the connection fails.
    """
    command = NMCLI_SET_AUTOCONNECT_ON_TO_WIFI_CONNECTION.format(connection_name)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to set autoconnect to 'yes' for connection '{connection_name}'. Error: {result.stderr}")

    print(f"Autoconnect set to 'yes' for connection '{connection_name}' successfully.")


def set_autoconnect_off_to_wifi_connection(connection_name: str):
    """
    Sets the autoconnect property to 'no' for a specified network connection.

    Args:
        connection_name (str): The name of the connection to update.

    Raises:
        RuntimeError: If the command to update the connection fails.
    """
    command = NMCLI_SET_AUTOCONNECT_OFF_TO_WIFI_CONNECTION.format(connection_name)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to set autoconnect to 'no' for connection '{connection_name}'. Error: {result.stderr}")

    print(f"Autoconnect set to 'no' for connection '{connection_name}' successfully.")






