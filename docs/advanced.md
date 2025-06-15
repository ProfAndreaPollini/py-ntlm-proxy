---
layout: default
title: Advanced Configuration
---

# 🔧 Advanced Configuration

This page covers advanced configuration options and fine-tuning for py-ntlm-proxy.

## Environment Variables

The application respects the following environment variables:

- `LOCALAPPDATA`: Used to determine the configuration directory location

## Logging Configuration

Logging is configured in the main application code. To modify logging behavior:

```python
# In main.py
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbose logging
    format="%(asctime)s - %(levelname)s - %(message)s"
)
```

Available log levels:
- `logging.DEBUG`: Detailed debugging information
- `logging.INFO`: Confirmation that things are working as expected
- `logging.WARNING`: Indication that something unexpected happened
- `logging.ERROR`: Due to a more serious problem, the software has not been able to perform some function
- `logging.CRITICAL`: A serious error, indicating that the program itself may be unable to continue running

## Performance Tuning

### Event Loop Optimization

The application attempts to use `winloop` for better performance if available:

```python
try:
    import winloop
    winloop.install()
    logging.info("winloop attivato per prestazioni di rete superiori.")
except ImportError:
    logging.warning("winloop non trovato. L'event loop di default di asyncio verrà utilizzato.")
```

To ensure the best performance, install `winloop`:

```powershell
pip install winloop
```

### Memory Usage

The application limits the activity log to the most recent 50 requests by default:

```python
uri_log_queue = deque(maxlen=50)
```

You can adjust this value to control memory usage vs. log history.

## Security Considerations

### Credential Storage

Passwords are stored using the Windows Credential Manager, which provides encryption and secure storage. The application uses the `keyring` library to interface with the Credential Manager.

### Network Security

By default, the proxy only listens on `127.0.0.1`, making it accessible only from the local machine. If you need to make it available to other machines on your network, you would need to modify the hostname binding in the code.

## Customizing the User Interface

The application uses CustomTkinter for the UI. You can customize the appearance by modifying theme settings:

```python
ctk.set_appearance_mode("dark")  # Change to "light" for light theme
```

## Advanced Proxy Configuration

### Multiple Parent Proxies

While not directly supported through the GUI, you can implement proxy chaining by:

1. Run multiple instances of py-ntlm-proxy on different ports
2. Configure each instance to use the previous one as its parent proxy

### Adding Custom Headers

To add custom headers to outgoing requests, you would need to modify the `NtlmProxyPlugin` class in the source code.

## Starting at System Boot

To have py-ntlm-proxy start automatically when Windows boots:

1. Create a shortcut to the application executable or script
2. Press `Win+R` and type `shell:startup`
3. Place the shortcut in the Startup folder that opens

## Next Steps

For troubleshooting common issues, see the [Troubleshooting](troubleshooting) page.
