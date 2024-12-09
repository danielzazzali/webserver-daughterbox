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
        rememberedWifiPanel.classList.add('known-wifi-panel');

        const rememberedWifiTitle = document.createElement('h3');
        rememberedWifiTitle.textContent = 'Known Wi-Fi Networks';
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

            const forgetButton = document.createElement('button');
            forgetButton.classList.add('forget-button');
            forgetButton.textContent = 'Forget';
            forgetButton.onclick = async () => {
                await showLoading();
                await deleteKnownWifiConnection(connection.name);
                await changeContentToWifi();
            };
            connectionItem.appendChild(forgetButton);

            rememberedWifiPanel.appendChild(connectionItem);
        });

        container.appendChild(rememberedWifiPanel);
    }

    const activeWifiNetworksPanel = document.createElement('div');
    activeWifiNetworksPanel.classList.add('active-wifi-panel');

    const activeWifiNetworksTitle = document.createElement('h3');
    activeWifiNetworksTitle.textContent = 'Available Wi-Fi Networks';
    activeWifiNetworksPanel.appendChild(activeWifiNetworksTitle);

    availableWifiNetworks.forEach(network => {
        const networkItem = document.createElement('div');
        networkItem.classList.add('network-item');

        const ssid = document.createElement('span');
        ssid.classList.add('network-ssid');
        ssid.textContent = network.SSID;
        networkItem.appendChild(ssid);

        const signal = document.createElement('span');
        signal.classList.add('network-signal');
        signal.textContent = `Signal: ${network.SIGNAL}%`;
        networkItem.appendChild(signal);

        const isKnownNetwork = Array.isArray(rememberedWifiConnections) && rememberedWifiConnections.some(connection => connection.name === network.SSID);

        if (network.ACTIVE === 'yes') {
            const disconnectButton = document.createElement('button');
            disconnectButton.classList.add('disconnect-button');
            disconnectButton.textContent = 'Disconnect';
            disconnectButton.onclick = async () => {
                await showLoading();
                await disconnectFromWifiConnection(network.SSID);
                await changeContentToWifi();
            };
            networkItem.appendChild(disconnectButton);
        } else if (isKnownNetwork) {
            const connectButton = document.createElement('button');
            connectButton.classList.add('connect-button');
            connectButton.textContent = 'Connect';
            connectButton.onclick = async () => {
                await showLoading();
                await connectToKnownWifiConnection(network.SSID);
                await changeContentToWifi();
            };
            networkItem.appendChild(connectButton);
        } else {
            const connectButton = document.createElement('button');
            connectButton.classList.add('connect-button');
            connectButton.textContent = 'Connect';
            connectButton.onclick = () => showPasswordInput(network.SSID);
            networkItem.appendChild(connectButton);

            const passwordInput = document.createElement('input');
            passwordInput.classList.add('password-input');
            passwordInput.type = 'password';
            passwordInput.placeholder = 'Enter password';
            passwordInput.style.display = 'none';
            networkItem.appendChild(passwordInput);

            const confirmButton = document.createElement('button');
            confirmButton.classList.add('confirm-button');
            confirmButton.textContent = 'Confirm';
            confirmButton.style.display = 'none';
            confirmButton.onclick = async () => {
                await showLoading();
                await connectToNewAp(network.SSID, passwordInput.value);
                await changeContentToWifi();
            };
            networkItem.appendChild(confirmButton);
        }

        activeWifiNetworksPanel.appendChild(networkItem);
    });

    container.appendChild(activeWifiNetworksPanel);
}

function showPasswordInput(ssid) {
    const networkItems = document.querySelectorAll('.network-item');
    networkItems.forEach(item => {
        const ssidElement = item.querySelector('.network-ssid');
        if (ssidElement.textContent === ssid) {
            const passwordInput = item.querySelector('.password-input');
            const confirmButton = item.querySelector('.confirm-button');
            const connectButton = item.querySelector('.connect-button');
            passwordInput.style.display = 'block';
            confirmButton.style.display = 'block';
            connectButton.style.display = 'none';
        }
    });
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