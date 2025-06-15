---
layout: default
title: Usage Examples
---

# 📊 Usage Examples

This page provides common usage scenarios for py-ntlm-proxy in different environments.

## Basic Proxy Setup

For standard usage behind a corporate proxy:

```powershell
# Start with default settings
python py-ntlm-proxy/main.py
```

Then configure your applications to use `127.0.0.1:3128` as the HTTP proxy.

## Custom Port Configuration

If you need to use a different port (for example, if 3128 is already in use):

1. Configure through the GUI:
   - Open the Configuration tab
   - Set the Listen Port to your desired port (e.g., 8080)
   - Save and restart

2. Or modify the config file directly:
   ```ini
   [Proxy]
   ListenPort = 8080
   ```

3. Configure your applications to use the new port:
   - Proxy Server: `127.0.0.1`
   - Port: `8080` (or your configured port)

## Corporate Environment with Existing Proxy

For corporate environments with existing proxy infrastructure:

1. Configure the parent proxy:
   ```ini
   [Proxy]
   ParentProxy = corporate-proxy.company.com:8080
   ListenPort = 3128
   ```

2. Add your authentication details:
   ```ini
   [Auth]
   Username = your_username
   Domain = your_domain
   ```

3. Securely save your password through the GUI

## Browser Configuration

### Chrome

1. Open Settings
2. Search for "proxy"
3. Click "Open your computer's proxy settings"
4. In Windows settings:
   - Enable "Use a proxy server"
   - Address: `127.0.0.1`
   - Port: `3128` (or your configured port)

### Firefox

1. Open Settings
2. Scroll to Network Settings
3. Click "Settings"
4. Select "Manual proxy configuration"
5. HTTP Proxy: `127.0.0.1`
6. Port: `3128` (or your configured port)

## Command Line Tools

For tools like `curl` or `wget`:

```bash
# Using curl with the proxy
curl -x http://127.0.0.1:3128 https://example.com

# Using wget with the proxy
wget -e use_proxy=yes -e http_proxy=127.0.0.1:3128 https://example.com
```

## Node.js Applications

For Node.js applications:

```javascript
// Set environment variables
process.env.HTTP_PROXY = 'http://127.0.0.1:3128';
process.env.HTTPS_PROXY = 'http://127.0.0.1:3128';

// Or using the request library
const request = require('request');
const options = {
  url: 'https://example.com',
  proxy: 'http://127.0.0.1:3128'
};
request(options, function(err, res, body) {
  // ...
});
```

## Python Applications

For Python applications:

```python
import requests

proxies = {
    'http': 'http://127.0.0.1:3128',
    'https': 'http://127.0.0.1:3128',
}

response = requests.get('https://example.com', proxies=proxies)
```

## Next Steps

For more advanced configuration options, see the [Advanced Configuration](advanced) page.
