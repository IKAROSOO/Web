const downloadBtn = document.getElementById('download-btn');

downloadBtn.addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    chrome.tabs.sendMessage(tab.id, {
        action: "DownloadBtn_clicked"
    });
})