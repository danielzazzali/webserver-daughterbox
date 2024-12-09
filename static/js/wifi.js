async function fetchWifiDataConcurrently() {
    const [rememberedWifiConnections, activeWifiConnection, availableWifiNetworks] = await Promise.all([
        getRememberedWifiConnections(),
        getActiveWifiConnection(),
        scanWifiNetworks()
    ]);

    return {
        rememberedWifiConnections: rememberedWifiConnections.connections,
        activeWifiConnection: activeWifiConnection.network,
        availableWifiNetworks: availableWifiNetworks.networks
    };
}

async function changeContentToWifi() {
    const { rememberedWifiConnections, activeWifiConnection, availableWifiNetworks } = await fetchWifiDataConcurrently();

    const contentPanel = document.getElementById('content-panel');
    contentPanel.innerHTML = '';

    const container = document.createElement('div');
    container.classList.add('wifi-settings-container');
    contentPanel.appendChild(container);

    const title = document.createElement('h2');
    title.textContent = 'Wi-Fi Settings';
    container.appendChild(title);

    if (activeWifiConnection.ACTIVE === 'yes') {
        const activeWifiPanel = document.createElement('div');
        activeWifiPanel.classList.add('connected-wifi-panel');

        const activeWifiTitle = document.createElement('h3');
        activeWifiTitle.textContent = 'Connected Wi-Fi';
        activeWifiPanel.appendChild(activeWifiTitle);

        const ssidInfo = document.createElement('p');
        ssidInfo.textContent = `SSID: ${activeWifiConnection.SSID}`;
        activeWifiPanel.appendChild(ssidInfo);

        const signalInfo = document.createElement('p');
        signalInfo.textContent = `Signal: ${activeWifiConnection.SIGNAL}%`;
        activeWifiPanel.appendChild(signalInfo);

        container.appendChild(activeWifiPanel);
    }

}