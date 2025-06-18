---
layout: default
title: Configuration
---

# ⚙️ Configuration

py-ntlm-proxy offers flexible configuration options through both the GUI and manual file editing.

## GUI Configuration

The application provides a user-friendly interface with three main tabs:

### Status Tab

Monitor proxy status, uptime, and request statistics.

![Status Tab](assets/images/status-tab.png)

### Configuration Tab

Set up authentication and proxy settings:

- **Username**: Your domain username
- **Domain**: Your domain name (e.g., COMPANY or company.com)
- **Password**: Your domain password
- **Parent Proxy**: Your corporate proxy address (format: hostname:port)
- **Listen Port**: The local port where py-ntlm-proxy will listen

![Configuration Tab](assets/images/configuration-tab.png)

### Activity Log Tab

View real-time request logs and monitor traffic through the proxy.

![Activity Log Tab](assets/images/activity-log-tab.png)

## Manual Configuration

If you prefer to edit configuration files directly, py-ntlm-proxy stores its settings in:

```
%LOCALAPPDATA%\PythonNtlmProxy\cntlm.ini
```

The configuration file has the following structure:

```ini
[Auth]
Username = your_username
Domain = your_domain

[Proxy]
ParentProxy = corporate-proxy.company.com:8080
ListenPort = 3128
```

### Configuration Parameters

| Section | Parameter | Description |
|---------|-----------|-------------|
| Auth | Username | Your domain username without domain prefix |
| Auth | Domain | Your Windows domain name |
| Proxy | ParentProxy | Address of your corporate proxy (hostname:port) |
| Proxy | ListenPort | Port on which the local proxy will listen |

## Credential Storage

Passwords are not stored in the configuration file. Instead, they are securely saved in the Windows Credential Manager under the service name `PythonNtlmProxyApp`.

## Configuration Reset

To reset your configuration:

1. Delete the file at `%LOCALAPPDATA%\PythonNtlmProxy\cntlm.ini`
2. Remove the credentials from Windows Credential Manager
3. Restart the application

## Next Steps

For usage examples and advanced configurations, see the [Usage Examples](usage) and [Advanced Configuration](advanced) pages.
