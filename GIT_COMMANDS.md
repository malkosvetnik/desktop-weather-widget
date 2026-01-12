# 🚀 Git Commands - Quick Reference

## Brzi GitHub Release v2.2.3

Copy/paste ove komande u terminal (Git Bash ili Command Prompt):

---

## 📂 PRIPREMA

```bash
# Navigate to project folder
cd Desktop-Weather-Widget

# Check status
git status

# Create screenshots folder (if doesn't exist)
mkdir screenshots
```

---

## 📸 DODAJ SCREENSHOTS

```bash
# After you capture all 19 screenshots, add them:
git add screenshots/
```

---

## 📝 COMMIT CHANGES

```bash
# Add all files
git add .

# Check what will be committed
git status

# Commit with message
git commit -m "Release v2.2.3 - Windows Location Fix

- Fixed: Windows Location now uses PowerShell API
- Added: Real GPS/Wi-Fi triangulation
- Removed: geocoder dependency
- Added: Accuracy display in meters
- Added: Automatic fallback to API location
- Updated: All documentation for v2.2.3"

# Push to GitHub
git push origin main
```

---

## 🏷️ CREATE TAG

```bash
# Create annotated tag
git tag -a v2.2.3 -m "Release v2.2.3 - Windows Location Fix"

# Push tag to GitHub
git push origin v2.2.3

# Verify tag created
git tag -l
```

---

## 🔍 CHECK REMOTE

```bash
# Check what will be pushed
git log --oneline -5

# Check remote URL
git remote -v

# Should show:
# origin  https://github.com/malkosvetnik/Desktop-Weather-Widget.git (fetch)
# origin  https://github.com/malkosvetnik/Desktop-Weather-Widget.git (push)
```

---

## 🐛 TROUBLESHOOTING

### If commit fails (username/email not set):

```bash
git config --global user.name "malkosvetnik"
git config --global user.email "your-email@example.com"
```

### If push fails (authentication):

**Option 1: HTTPS (with Personal Access Token)**
```bash
# Generate token at: https://github.com/settings/tokens
# Then use token instead of password when prompted
git push origin main
```

**Option 2: SSH**
```bash
# Check if SSH key exists
ls ~/.ssh/id_rsa.pub

# If not, generate:
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# Add to GitHub: https://github.com/settings/keys
cat ~/.ssh/id_rsa.pub

# Change remote to SSH
git remote set-url origin git@github.com:malkosvetnik/Desktop-Weather-Widget.git
```

### If tag already exists:

```bash
# Delete local tag
git tag -d v2.2.3

# Delete remote tag
git push origin :refs/tags/v2.2.3

# Recreate tag
git tag -a v2.2.3 -m "Release v2.2.3 - Windows Location Fix"
git push origin v2.2.3
```

### If you need to undo last commit:

```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Undo commit and discard changes (DANGEROUS!)
git reset --hard HEAD~1
```

---

## 📊 VERIFY UPLOAD

After pushing, check on GitHub:

1. Go to: https://github.com/malkosvetnik/Desktop-Weather-Widget
2. Check **Code** tab - should show all files
3. Check **Releases** - should show v2.2.3 tag
4. Check **README.md** - should render properly with screenshots

---

## 🔄 UPDATE AFTER RELEASE

If you need to fix something after release:

```bash
# Make changes
# Edit files...

# Commit
git add .
git commit -m "Fix: Description of fix"
git push origin main

# For hotfix release, create new tag:
git tag -a v2.2.4 -m "Hotfix v2.2.4"
git push origin v2.2.4
```

---

## 📦 CREATE GITHUB RELEASE (After push & tag)

**On GitHub Website:**

1. Go to: https://github.com/malkosvetnik/Desktop-Weather-Widget/releases/new
2. Choose tag: `v2.2.3`
3. Release title: `v2.2.3 - Windows Location Fix`
4. Description: **Copy from RELEASE_NOTES_v2.2.3.md**
5. Click **Publish release**

---

## 💾 FULL WORKFLOW (Start to Finish)

```bash
# 1. Navigate to project
cd Desktop-Weather-Widget

# 2. Add all files
git add .

# 3. Commit
git commit -m "Release v2.2.3 - Windows Location Fix"

# 4. Push
git push origin main

# 5. Create tag
git tag -a v2.2.3 -m "Release v2.2.3 - Windows Location Fix"

# 6. Push tag
git push origin v2.2.3

# 7. Go to GitHub and create release (manual step)
```

---

## 🎯 ONE-LINER (If everything is ready)

```bash
git add . && git commit -m "Release v2.2.3 - Windows Location Fix" && git push origin main && git tag -a v2.2.3 -m "Release v2.2.3" && git push origin v2.2.3
```

⚠️ **Only use if you're sure everything is correct!**

---

## ✅ CHECKLIST BEFORE RUNNING COMMANDS

- [ ] All screenshots in `screenshots/` folder
- [ ] `weather_widget_final.pyw` is the PATCHED version
- [ ] Version v2.2.3 in code
- [ ] Tested on clean system
- [ ] README.md looks good locally
- [ ] requirements.txt correct (no geocoder)

---

## 🆘 NEED HELP?

**Git Documentation:**
- https://git-scm.com/docs
- https://docs.github.com/en

**Quick Reference:**
- `git status` - Check what's changed
- `git log` - View commit history
- `git diff` - See changes
- `git branch` - List branches
- `git remote -v` - Check remote URL

---

**Srećno! 🚀**

*Git Commands Cheat Sheet for Desktop Weather Widget v2.2.3*
