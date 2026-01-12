# Contributing to Desktop Weather Widget

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to Desktop Weather Widget. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

---

## 🐛 Reporting Bugs

Before creating bug reports, please check the [existing issues](https://github.com/malkosvetnik/Desktop-Weather-Widget/issues) to avoid duplicates.

### How to Submit a Good Bug Report

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce**
- **Provide specific examples**
- **Describe the behavior you observed** and **what you expected**
- **Include screenshots** if possible
- **Include your environment details:**
  - OS version (e.g., Windows 11 23H2)
  - Python version
  - Widget version
  - Error messages from console

**Template:**
```markdown
**Bug Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Launch widget
2. Click on '...'
3. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happened

**Environment:**
- OS: Windows 11 23H2
- Python: 3.11.5
- Widget Version: v2.2.3

**Console Output:**
```
[Paste error messages here]
```

**Screenshots:**
[If applicable]
```

---

## 💡 Suggesting Enhancements

Enhancement suggestions are welcome! Before creating enhancement suggestions, please check if it already exists in the [issues](https://github.com/malkosvetnik/Desktop-Weather-Widget/issues).

### How to Submit a Good Enhancement Suggestion

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this would be useful** to most users
- **List some examples** of how it would be used
- **Include mockups or screenshots** if applicable

---

## 🔧 Pull Requests

### Development Process

1. **Fork the repository**
2. **Create a new branch** from `main`:
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add: New skin system for widget customization"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/my-new-feature
   ```
7. **Submit a Pull Request**

### Commit Message Guidelines

Use the following prefixes:
- `Add:` - New feature
- `Fix:` - Bug fix
- `Update:` - Update to existing feature
- `Remove:` - Remove feature or code
- `Refactor:` - Code refactoring (no functionality change)
- `Docs:` - Documentation only changes
- `Style:` - Code style changes (formatting, etc.)
- `Test:` - Adding or updating tests

**Examples:**
```
Add: Battery status display for laptops
Fix: Windows Location now uses PowerShell API
Update: Improved tooltip styling
Docs: Add installation instructions for Windows 10
```

### Code Style

- **Follow PEP 8** style guide
- **Use descriptive variable names**
- **Add comments** for complex logic
- **Keep functions small and focused**
- **Use type hints** where applicable

**Example:**
```python
def updateBatteryStatus(self) -> None:
    """
    Update battery status display (laptops only).
    
    Shows battery percentage, charging status, and appropriate icon.
    Updates every 5 seconds via timer.
    """
    if not PSUTIL_AVAILABLE:
        return
    
    try:
        battery = psutil.sensors_battery()
        # ... implementation ...
```

### Testing

Before submitting a PR:
- [ ] Test on Windows 10 and Windows 11
- [ ] Test with different screen resolutions
- [ ] Test with different languages (Serbian + English)
- [ ] Test with different unit systems (Metric + Imperial)
- [ ] Test online and offline scenarios
- [ ] Check console for errors
- [ ] Verify no performance regressions

---

## 🌐 Translations

Help translate the widget to more languages!

1. Open `weather_widget_final.pyw`
2. Find the `self.translations` dictionary
3. Add your language:

```python
self.translations = {
    "sr": { ... },  # Serbian
    "en": { ... },  # English
    "de": {         # German (example)
        "refresh_interval": "Aktualisierung:",
        "feels_like": "Fühlt sich an wie",
        # ... add all keys ...
    }
}
```

4. Submit a PR with your translation

---

## 📝 Documentation

Improvements to documentation are always welcome!

- Fix typos
- Clarify unclear sections
- Add examples
- Update screenshots
- Translate to other languages

---

## 🎨 Design Guidelines

### UI/UX Principles

- **Minimalism:** Keep interface clean and uncluttered
- **Readability:** Use appropriate font sizes and colors
- **Consistency:** Maintain consistent spacing, colors, and styling
- **Accessibility:** Consider color-blind users, high-contrast needs
- **Performance:** Avoid heavy animations or frequent updates

### Color Palette

Current theme:
- Background: `rgba(15, 20, 30, 0.85)` (semi-transparent dark blue)
- Text: `rgba(255, 255, 255, 0.8)` (white, 80% opacity)
- Accent: `rgba(144, 202, 249, 0.5)` (light blue)
- Success: `#4CAF50` (green)
- Warning: `#FFC107` (orange)
- Error: `#F44336` (red)

---

## 🆘 Questions?

If you have questions:
- Check the [README.md](README.md)
- Check [existing issues](https://github.com/malkosvetnik/Desktop-Weather-Widget/issues)
- Open a new issue with the `question` label

---

## 📜 Code of Conduct

Be respectful, inclusive, and constructive. We're all here to make great software!

---

**Thank you for contributing! 🌤️**
