---
layout: default
title: Installation
---

# 📋 Installation

There are several ways to install py-ntlm-proxy, depending on your preferences and needs.

## Requirements

Before you begin, ensure your system meets the following requirements:

- **Operating System**: Windows 10/11
- **Python**: 3.13 or higher
- **Dependencies**: All dependencies are managed via the project configuration

## Installation Methods

### Option 1: Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. This is the recommended installation method for the best performance.

```powershell
# Clone the repository
git clone https://github.com/ProfAndreaPollini/py-ntlm-proxy.git
cd py-ntlm-proxy

# Install dependencies using uv
uv sync
```

### Option 2: Using pip

If you prefer using the standard Python package manager:

```powershell
# Clone the repository
git clone https://github.com/ProfAndreaPollini/py-ntlm-proxy.git
cd py-ntlm-proxy/py-ntlm-proxy

# Install dependencies
pip install -r requirements.txt
```

### Option 3: Development Installation

For contributors or those who want to modify the code:

```powershell
# Clone the repository
git clone https://github.com/ProfAndreaPollini/py-ntlm-proxy.git
cd py-ntlm-proxy

# Install in development mode
pip install -e .
```

## Next Steps

After installation, proceed to the [Quick Start](quick-start) guide to configure and run the proxy.
