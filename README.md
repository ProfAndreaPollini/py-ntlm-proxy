# py-ntlm-proxy

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A modern NTLM/NTLMv2 authenticating HTTP proxy with a graphical user interface. Think of it as a modernized "cntlm" with better usability and Windows integration.

## 🚀 Features

- **NTLM/NTLMv2 Authentication**: Seamlessly authenticate with corporate proxies using NTLM protocol
- **Modern GUI**: Built with CustomTkinter for a sleek, dark-themed interface
- **System Tray Integration**: Runs quietly in the background with system tray icon
- **Secure Credential Storage**: Passwords are stored securely using Windows Credential Manager
- **Real-time Monitoring**: Live request logging and statistics
- **Easy Configuration**: User-friendly configuration interface
- **Performance Optimized**: Uses winloop for enhanced network performance when available

## 📋 Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.13 or higher
- **Dependencies**: All dependencies are managed via the project configuration

## 🛠️ Installation

### Option 1: Using uv (Recommended)

```powershell
# Clone the repository
git clone https://github.com/yourusername/py-ntlm-proxy.git
cd py-ntlm-proxy

# Install dependencies using uv
uv sync
```

### Option 2: Using pip

```powershell
# Clone the repository
git clone https://github.com/yourusername/py-ntlm-proxy.git
cd py-ntlm-proxy/py-ntlm-proxy

# Install dependencies
pip install -r requirements.txt
```

### Option 3: Development Installation

```powershell
# Clone the repository
git clone https://github.com/yourusername/py-ntlm-proxy.git
cd py-ntlm-proxy

# Install in development mode
pip install -e .
```

## 🚀 Quick Start

### 1. Start the Proxy

```powershell
python py-ntlm-proxy/main.py
```

The application will start with a GUI interface. If this is your first time running it, you'll need to configure your credentials through the Configuration tab.

#### Initial Configuration

1. Open the **Configuration tab** in the GUI
2. Enter your domain credentials:
   - **Username**: Your domain username
   - **Domain**: Your domain name
   - **Password**: Your password (will be stored securely in Windows Credential Manager)
   - **Parent Proxy**: Your corporate proxy address (if applicable)
   - **Listen Port**: The port for the local proxy (default: 3128)
3. Click **"Save Credentials and Restart"** to apply the settings

### 2. Configure Your Applications

Once the proxy is running (default port 3128), configure your applications to use:

- **Proxy Server**: `127.0.0.1`
- **Port**: `3128` (or your configured port)

## ⚙️ Configuration

The application provides a user-friendly GUI for configuration:

### GUI Configuration

1. **Status Tab**: Monitor proxy status, uptime, and request statistics
2. **Configuration Tab**: Set up authentication and proxy settings
3. **Activity Log Tab**: View real-time request logs

### Manual Configuration

Configuration is stored in: `%LOCALAPPDATA%\PythonNtlmProxy\cntlm.ini`

```ini
[Auth]
Username = your_username
Domain = your_domain

[Proxy]
ParentProxy = corporate-proxy.company.com:8080
ListenPort = 3128
```

## 📊 Usage Examples

### Basic Proxy Setup

```powershell
# Start with default settings
python py-ntlm-proxy/main.py
```

### Custom Port Configuration

Configure through the GUI or modify the config file to use a different port:

```ini
[Proxy]
ListenPort = 8080
```

### Corporate Environment

For corporate environments with existing proxy infrastructure:

```ini
[Proxy]
ParentProxy = corporate-proxy.company.com:8080
ListenPort = 3128
```

## 🔧 Advanced Configuration

### Environment Variables

The application respects the following environment variables:

- `LOCALAPPDATA`: Configuration directory location

### Logging

Logs are written to the console and can be viewed in the Activity Log tab of the GUI.

### Performance Tuning

- The application automatically uses `winloop` if available for better performance
- Supports up to 50 recent requests in the activity log (configurable)

## 🐛 Troubleshooting

### Common Issues

#### 1. Authentication Failures

- Verify your credentials in the Configuration tab of the GUI
- Ensure your domain and username are correct
- Check that your corporate proxy supports NTLM authentication

#### 2. Connection Issues

- Verify the parent proxy address and port
- Check your network connectivity
- Ensure the listen port is not already in use

#### 3. GUI Issues

- Ensure you have the latest version of CustomTkinter installed
- Check that all dependencies are properly installed

### Debug Mode

To enable verbose logging, modify the logging configuration in `main.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s"
)
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```powershell
# Clone and setup development environment
git clone https://github.com/yourusername/py-ntlm-proxy.git
cd py-ntlm-proxy
uv sync --dev

# Run tests (if available)
python -m pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on top of [proxy.py](https://github.com/abhinavsingh/proxy.py) for the core proxy functionality
- Uses [ntlm-auth](https://github.com/jborean93/ntlm-auth) for NTLM authentication
- GUI built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Inspired by the original [cntlm](http://cntlm.sourceforge.net/) project

## 📞 Support

- Create an issue on GitHub for bug reports or feature requests
- Check the [troubleshooting section](#-troubleshooting) for common problems
- Review the [configuration section](#️-configuration) for setup help

## 🗺️ Roadmap

- [ ] Linux/macOS support
- [ ] Support for additional authentication methods
- [ ] Configuration import/export
- [ ] Proxy chain support
- [ ] Performance metrics and analytics
- [ ] Auto-update functionality

---

Made with ❤️ for corporate developers who need a modern NTLM proxy solution.
