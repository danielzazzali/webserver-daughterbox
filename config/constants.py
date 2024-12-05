PORT = '8000'

ETHERNET_CONNECTION = 'ETH'

DEVICE_MODE_FILE_PATH = '/home/capstone/mode'

REBOOT_SYSTEM = "sudo reboot"
SHUTDOWN_SYSTEM = "sudo shutdown -h now"

NMCLI_GET_IP4_ADDRESS = "nmcli -t -f IP4.ADDRESS connection show '{}'"
NMCLI_SET_IP4_ADDRESS = "nmcli connection modify '{}' ipv4.addresses '{}' ipv4.method manual"
NMCLI_GET_WIFI_CONNECTIONS = "nmcli -t -f NAME,AUTOCONNECT,TYPE connection show | grep '802-11-wireless'"
NMCLI_SCAN_WIFI_NETWORKS = "nmcli -t -f SSID,SIGNAL,ACTIVE,BSSID device wifi"
NMCLI_GET_ACTIVE_WIFI_CONNECTION = "nmcli -t -f SSID,SIGNAL,ACTIVE device wifi | grep 'yes'"
NMCLI_CONNECT_TO_NEW_AP = "nmcli dev wifi connect '{}' password '{}'"
NMCLI_DISCONNECT_FROM_WIFI_CONNECTION = "nmcli connection down '{}'"
NMCLI_CONNECT_TO_KNOWN_WIFI_CONNECTION = "nmcli connection up '{}'"
NMCLI_DELETE_KNOWN_WIFI_CONNECTION = "nmcli connection delete '{}'"
NMCLI_SET_AUTOCONNECT_ON_TO_WIFI_CONNECTION = "nmcli connection modify '{}' connection.autoconnect yes"
NMCLI_SET_AUTOCONNECT_OFF_TO_WIFI_CONNECTION = "nmcli connection modify '{}' connection.autoconnect no"

MAC_PREFIX_FOR_RASPBERRY = "B8:27:EB"