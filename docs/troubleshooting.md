---
layout: default
title: Troubleshooting
---

# 🐛 Troubleshooting

This guide helps you solve common issues with py-ntlm-proxy.

## Common Issues

### Authentication Failures

**Symptoms:**
- Applications report "Proxy Authentication Required" errors
- Status tab shows connection errors
- Web browsers display 407 errors

**Solutions:**
1. Verify your credentials in the Configuration tab
2. Ensure your domain and username are correct
3. Check that your corporate proxy supports NTLM authentication
4. Try re-entering your password

**Detailed Steps:**
1. Open the Configuration tab
2. Re-enter your domain credentials
3. Click "Save Credentials and Restart"
4. Check the Status tab to confirm the proxy is running

### Connection Issues

**Symptoms:**
- Unable to connect to websites
- Applications timeout when trying to access the internet
- Status shows "Active" but no requests are being processed

**Solutions:**
1. Verify the parent proxy address and port
2. Check your network connectivity
3. Ensure the listen port is not already in use
4. Test connectivity to the parent proxy

**Detailed Steps:**
```powershell
# Test connection to parent proxy
Test-NetConnection -ComputerName your-proxy.company.com -Port 8080

# Check if your listen port is already in use
Get-NetTCPConnection -LocalPort 3128 -ErrorAction SilentlyContinue
```

### GUI Issues

**Symptoms:**
- The application window doesn't appear
- GUI elements are missing or distorted
- Interface doesn't respond to clicks

**Solutions:**
1. Ensure you have the latest version of CustomTkinter installed
2. Check that all dependencies are properly installed
3. Try restarting the application
4. Update your Python installation

**Detailed Steps:**
```powershell
# Upgrade CustomTkinter
pip install --upgrade customtkinter

# Reinstall dependencies
pip install -r requirements.txt
```

## Enabling Debug Mode

For more detailed logging:

1. Modify the logging configuration in `main.py`:
   ```python
   logging.basicConfig(
       level=logging.DEBUG,  # Change from INFO to DEBUG
       format="%(asctime)s - %(levelname)s - %(message)s"
   )
   ```

2. Restart the application

## Application Crashes

If the application crashes at startup:

1. Check if another instance is already running
2. Look for errors in the Windows Event Viewer
3. Try running from the command line to see error messages:
   ```powershell
   python py-ntlm-proxy/main.py
   ```

## Proxy Chain Issues

If you're using py-ntlm-proxy with other proxies:

1. Verify the proxy chain order
2. Ensure each proxy in the chain is correctly configured
3. Test each proxy individually before chaining them

## Permission Issues

If you encounter permission errors:

1. Try running the application as administrator
2. Check Windows Credential Manager access
3. Verify write permissions to `%LOCALAPPDATA%\PythonNtlmProxy`

## Reset to Default

If all else fails, you can reset to default settings:

1. Close the application
2. Delete the configuration file:
   ```powershell
   Remove-Item "$env:LOCALAPPDATA\PythonNtlmProxy\cntlm.ini"
   ```
3. Remove the stored credentials from Windows Credential Manager
4. Restart the application

## Getting Help

If you continue to experience issues:

1. Check the [GitHub Issues](https://github.com/ProfAndreaPollini/py-ntlm-proxy/issues) for similar problems
2. Create a new issue with detailed information about your problem
3. Include logs, error messages, and steps to reproduce
