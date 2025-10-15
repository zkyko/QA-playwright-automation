# 🎯 QUICK START - What You Need to Update

## ⚠️ REQUIRED: Update These 3 Things in `.env`

### 1. FourHands Login Credentials
```bash
FH_USERNAME=your_fh_email@example.com     # ← Change this
FH_PASSWORD=your_fh_password               # ← Change this
```

### 2. Your Jira Instance URL
```bash
JIRA_BASE_URL=https://yourcompany.atlassian.net   # ← Change this
```
- Replace `yourcompany` with your actual Jira subdomain
- Example: `https://fourhands.atlassian.net`
- NO trailing slash!

### 3. Your Jira Project Key
```bash
JIRA_PROJECT_KEY=QA    # ← Verify this is correct
```
- Find in Jira: Project Settings → Details → Project Key
- Examples: `QA`, `TEST`, `FHQA`
- Must be UPPERCASE

---

## ✅ Already Configured (No Changes Needed)

These are already set up in your `.env` file:

```bash
✅ D365_BASE_URL - Already set
✅ D365_USERNAME - Already set  
✅ D365_PASSWORD - Already set
✅ JIRA_EMAIL - Already set (nbhandari@austin.fourhands.com)
✅ JIRA_API_TOKEN - Already set (valid token)
✅ BROWSERSTACK - Already set
✅ Test Settings - Already set
```

---

## 🧪 Test Your Setup

```bash
# 1. Test Jira connection
python scripts/setup_jira.py

# 2. You should see:
✓ Jira connection successful
✓ Project found
✓ Zephyr Scale installed

# 3. If errors, double-check the 3 items above ☝️
```

---

## 📍 Current Status

| Item | Status |
|------|--------|
| FH Credentials | ❌ Need to update |
| Jira URL | ❌ Need to update |
| Jira Project Key | ⚠️ Verify it's correct |
| Everything else | ✅ Already configured |

---

## 🎯 Next Steps After Updating

1. Open `.env` file
2. Update the 3 items above
3. Save the file
4. Run: `python scripts/setup_jira.py`
5. If successful → You're ready to test! 🎉

---

**File Location:**
```
C:\Users\Timmy\Downloads\QA-PlayWright-Automation-w-jira-automate\QA-PlayWright-Automation w-jira\.env
```
