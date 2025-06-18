---
layout: default
title: Quick Start
---

# 🚀 Quick Start

Once you've [installed](installation) py-ntlm-proxy, follow these steps to get up and running quickly.

## 1. Start the Proxy

Launch the application with:

```powershell
python py-ntlm-proxy/main.py
```

The application will start with a GUI interface. If this is your first time running it, you'll need to configure your credentials through the Configuration tab.

## 2. Initial Configuration

1. Open the **Configuration tab** in the GUI
2. Enter your domain credentials:
   - **Username**: Your domain username
   - **Domain**: Your domain name
   - **Password**: Your password (will be stored securely in Windows Credential Manager)
   - **Parent Proxy**: Your corporate proxy address (if applicable)
   - **Listen Port**: The port for the local proxy (default: 3128)
3. Click **"Save Credentials and Restart"** to apply the settings

![Configuration Screen](assets/images/configuration-tab.png)

## 3. Configure Your Applications

Once the proxy is running (default port 3128), configure your applications to use:

- **Proxy Server**: `127.0.0.1`
- **Port**: `3128` (or your configured port)

## 4. System Tray

The application runs in the system tray:

- **Left-click**: Open the main interface
- **Right-click**: Access the menu (Open Panel, Exit)

## 5. Monitor Activity

Switch to the **Status** tab to monitor:

- Proxy status (Active/Inactive)
- Number of requests processed
- Uptime
- Current settings

## Next Steps

For more detailed usage information, check out the [Usage Examples](usage) and [Configuration](configuration) pages.
