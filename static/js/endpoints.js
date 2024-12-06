async function fetchWithErrorHandling(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error(`Request failed: ${response.statusText}`);
        }
    } catch (error) {
        console.error("Error:", error);
        return { error: error.message };
    }
}

async function getEthernetIpAndMask() {
    return await fetchWithErrorHandling('/ethernet_ip_and_mask');
}

async function setEthernetIpAndMask(ip, mask) {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip, mask })
    };
    return await fetchWithErrorHandling('/set_ethernet_ip_and_mask', options);
}

async function rebootSystem() {
    return fetchWithErrorHandling(`/reboot`, {
        method: 'POST'
    });
}

async function shutdownSystem() {
    return fetchWithErrorHandling(`/shutdown`, {
        method: 'POST'
    });
}

async function getWifiIpAndMask() {
    return await fetchWithErrorHandling('/wifi_ip_and_mask');
}

async function getRememberedWifiConnections() {
    return await fetchWithErrorHandling('/remembered_wifi_connections');
}

async function scanWifiNetworks() {
    return await fetchWithErrorHandling('/scan_wifi_networks');
}

async function getActiveWifiConnection() {
    return await fetchWithErrorHandling('/active_wifi_network');
}

async function connectToNewAp(ssid, password) {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ssid, password })
    };
    return await fetchWithErrorHandling('/connect_to_new_ap', options);
}

async function disconnectFromWifiConnection(connection_name) {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ connection_name })
    };
    return await fetchWithErrorHandling('/disconnect_from_wifi_connection', options);
}

async function connectToKnownWifiConnection(connection_name) {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ connection_name })
    };
    return await fetchWithErrorHandling('/connect_to_known_wifi_connection', options);
}

async function deleteKnownWifiConnection(connection_name) {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ connection_name })
    };
    return await fetchWithErrorHandling('/delete_known_wifi_connection', options);
}

async function setAutoconnectOnToWifiConnection(connection_name) {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ connection_name })
    };
    return await fetchWithErrorHandling('/set_autoconnect_on_to_wifi_connection', options);
}

async function setAutoconnectOffToWifiConnection(connection_name) {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ connection_name })
    };
    return await fetchWithErrorHandling('/set_autoconnect_off_to_wifi_connection', options);
}

