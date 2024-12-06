
// TODO
async function changeContentToWifi() {
    const data = null;

    const contentPanel = document.getElementById('content-panel');
    contentPanel.innerHTML = '';

    const wifiSettingsContainer = document.createElement('div');
    wifiSettingsContainer.classList.add('wifi-settings-container');

    const title = document.createElement('h2');
    title.textContent = 'Wi-Fi Settings';
    wifiSettingsContainer.appendChild(title);

    contentPanel.appendChild(wifiSettingsContainer);

}