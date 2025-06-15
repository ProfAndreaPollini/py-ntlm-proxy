---
layout: default
title: Contributing
---

# 🤝 Contributing

We welcome contributions to py-ntlm-proxy! This guide explains how to contribute to the project.

## Getting Started

### Prerequisites

- Python 3.13 or higher
- Git
- A GitHub account

### Development Setup

```powershell
# Clone the repository
git clone https://github.com/ProfAndreaPollini/py-ntlm-proxy.git
cd py-ntlm-proxy

# Set up development environment
uv sync --dev  # If you have uv installed
# OR
pip install -e ".[dev]"  # Traditional approach
```

## Development Workflow

### 1. Create a Feature Branch

```powershell
# Create and switch to a new branch
git checkout -b feature/your-feature-name
```

Use a descriptive branch name that reflects the changes you're making.

### 2. Make Your Changes

Implement your feature or fix, following these guidelines:

- Follow the existing code style
- Write clear, commented code
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

Run the application to ensure your changes work correctly:

```powershell
python py-ntlm-proxy/main.py
```

If tests are available:

```powershell
python -m pytest
```

### 4. Commit Your Changes

```powershell
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add feature: description of your changes"
```

Write clear commit messages that explain the "what" and "why" of your changes.

### 5. Push to GitHub

```powershell
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

1. Go to the [py-ntlm-proxy repository](https://github.com/ProfAndreaPollini/py-ntlm-proxy)
2. Click "Pull Requests" and then "New Pull Request"
3. Select your branch as the "compare" branch
4. Review your changes and click "Create Pull Request"
5. Provide a clear description of your changes

## Code Style Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use descriptive variable and function names
- Comment complex sections of code
- Keep functions focused on a single responsibility
- Use type hints where appropriate

## Documentation

When adding or changing features, please update the documentation:

- Update docstrings for modified functions
- Update the README.md if necessary
- Add examples for new functionality

## Reporting Issues

If you find a bug or want to request a feature:

1. Check existing [issues](https://github.com/ProfAndreaPollini/py-ntlm-proxy/issues) to avoid duplicates
2. Create a new issue with a clear title and description
3. Include steps to reproduce bugs
4. Suggest solutions if you have ideas

## License

By contributing to py-ntlm-proxy, you agree that your contributions will be licensed under the project's [MIT License](https://github.com/ProfAndreaPollini/py-ntlm-proxy/blob/main/LICENSE).

Thank you for contributing to py-ntlm-proxy!
