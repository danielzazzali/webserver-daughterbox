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


    if (rememberedWifiConnections.length > 0) {
        const rememberedWifiPanel = document.createElement('div');
        rememberedWifiPanel.classList.add('remembered-wifi-panel');

        const rememberedWifiTitle = document.createElement('h3');
        rememberedWifiTitle.textContent = 'Remembered Wi-Fi Networks';
        rememberedWifiPanel.appendChild(rememberedWifiTitle);

        rememberedWifiConnections.forEach(connection => {
            const connectionItem = document.createElement('div');
            connectionItem.classList.add('connection-item');

            const connectionName = document.createElement('span');
            connectionName.classList.add('connection-name');
            connectionName.textContent = connection.name;
            connectionItem.appendChild(connectionName);

            const autoconnectStatus = document.createElement('span');
            autoconnectStatus.classList.add('autoconnect-status');
            autoconnectStatus.textContent = connection.autoconnect === 'yes' ? 'Autoconnect: On' : 'Autoconnect: Off';
            connectionItem.appendChild(autoconnectStatus);

            const toggleButton = document.createElement('button');
            toggleButton.classList.add('toggle-button');
            toggleButton.textContent = connection.autoconnect === 'yes' ? 'Disable' : 'Enable';
            toggleButton.onclick = () => toggleAutoconnect(connection.name, connection.autoconnect);
            connectionItem.appendChild(toggleButton);

            rememberedWifiPanel.appendChild(connectionItem);
        });

        container.appendChild(rememberedWifiPanel);
    }
}

async function toggleAutoconnect(connectionName, currentStatus) {
    const newStatus = currentStatus === 'yes' ? 'no' : 'yes';
    if (newStatus === 'yes') {
        await setAutoconnectOnToWifiConnection(connectionName);
    } else {
        await setAutoconnectOffToWifiConnection(connectionName);
    }
    await changeContentToWifi();
}