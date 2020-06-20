const { app, BrowserWindow, shell } = require('electron');

function createWindow() {
    let win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            webSecurity: false,
            nodeIntegration: true
        }
    })
    win.loadFile('index.html');
    win.webContents.on('new-window', (e, url) => {
        e.preventDefault();
        shell.openExternal(url);
    })
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})
