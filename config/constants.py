PORT = 'PORT'

ETHERNET_CONNECTION = 'ETHERNET_CONNECTION'
WIRELESS_CONNECTION = 'WIRELESS_CONNECTION'

DEVICE_MODE_FILE_PATH = 'DEVICE_MODE_FILE_PATH'

REBOOT_SYSTEM = "sudo reboot"

NMCLI_GET_IP4_ADDRESS = "nmcli -f IP4.ADDRESS connection show {}"
NMCLI_SET_IP4_ADDRESS = "nmcli connection modify {} ipv4.addresses {} ipv4.method manual"
NMCLI_GET_WIFI_CONNECTIONS = "nmcli -f NAME,AUTOCONNECT,TYPE connection show | grep 'wifi'"
NMCLI_SCAN_WIFI_NETWORKS = "nmcli -f SSID,SIGNAL,ACTIVE device wifi"
NMCLI_GET_ACTIVE_WIFI_CONNECTION = "nmcli -f SSID,SIGNAL,ACTIVE device wifi | grep 'yes'"
NMCLI_CONNECT_TO_NEW_AP = "nmcli dev wifi connect '{}' password '{}' connection.autoconnect yes"
NMCLI_DISCONNECT_FROM_WIFI_CONNECTION = "nmcli connection down {}"
NMCLI_CONNECT_TO_KNOWN_WIFI_CONNECTION = "nmcli connection up {}"
NMCLI_DELETE_KNOWN_WIFI_CONNECTION = "nmcli connection delete {}"
NMCLI_SET_AUTOCONNECT_ON_TO_WIFI_CONNECTION = "nmcli connection modify '{}' connection.autoconnect yes"
NMCLI_SET_AUTOCONNECT_OFF_TO_WIFI_CONNECTION = "nmcli connection modify '{}' connection.autoconnect no"
