# Contributing to Desktop Weather Widget

First off, thank you for considering contributing to Desktop Weather Widget! 🎉

## How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots** (if applicable)
- **Environment**:
  - Windows version
  - Python version (if running from source)
  - Monitor resolution
  - Widget size setting

### Suggesting Features 💡

Feature requests are welcome! Please provide:

- **Clear description** of the feature
- **Use case** - why is this useful?
- **Mockups/examples** (if applicable)

### Pull Requests 🔧

1. **Fork** the repository
2. **Create a branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test thoroughly**
5. **Commit** with clear messages (`git commit -m 'Add amazing feature'`)
6. **Push** to your branch (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/desktop-weather-widget.git
cd desktop-weather-widget

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the widget
python weather_widget_final.py
```

## Code Style

- Follow **PEP 8** style guide
- Use **meaningful variable names**
- Add **comments** for complex logic
- Keep functions **focused and small**

## Testing

Before submitting, please test:

- [ ] Widget launches without errors
- [ ] All features work as expected
- [ ] No performance degradation
- [ ] Works on different resolutions
- [ ] API calls succeed

## Areas We Need Help With

- **Translations** - Add support for more languages
- **Weather providers** - Integration with other APIs
- **Themes** - Custom color schemes
- **Documentation** - Improve README, add tutorials
- **Testing** - Unit tests, integration tests
- **Features** - See GitHub Issues for ideas

## Questions?

Feel free to open an issue with the `question` label!

Thank you for contributing! ❤️
