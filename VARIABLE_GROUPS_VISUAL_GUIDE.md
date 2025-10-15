# Azure DevOps Variable Groups - Visual Guide

## 🎨 Variable Groups Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AZURE DEVOPS LIBRARY                          │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
┌────────────────────────────────┐  ┌──────────────────────────────┐
│   QA-Automation-Config         │  │   Jira-Zephyr-Config         │
│   (Existing - 11 variables)    │  │   (NEW - 5 variables)        │
├────────────────────────────────┤  ├──────────────────────────────┤
│                                │  │                              │
│ 🌐 BROWSERSTACK                │  │ 🎯 JIRA                      │
│  • USERNAME                    │  │  • BASE_URL                  │
│  • ACCESS_KEY 🔒               │  │  • EMAIL                     │
│                                │  │  • API_TOKEN 🔒              │
│ 🛍️ FOURHANDS                   │  │  • PROJECT_KEY               │
│  • BASE_URL                    │  │  • VERSION (optional)        │
│  • USERNAME                    │  │                              │
│  • PASSWORD 🔒                 │  │                              │
│                                │  │                              │
│ 💼 D365                        │  │                              │
│  • BASE_URL                    │  │                              │
│  • COMPANY                     │  │                              │
│  • USERNAME                    │  │                              │
│  • PASSWORD 🔒                 │  │                              │
│                                │  │                              │
│ ⚙️ TEST CONFIG                 │  │                              │
│  • HEADED                      │  │                              │
│  • TIMEOUT                     │  │                              │
│                                │  │                              │
└────────────────────────────────┘  └──────────────────────────────┘
                 │                               │
                 │                               │
                 └───────────────┬───────────────┘
                                 │
                                 ▼
                   ┌──────────────────────────┐
                   │   azure-pipelines.yml     │
                   │                           │
                   │   Uses both groups for:   │
                   │   • Test execution        │
                   │   • Jira integration      │
                   │   • Reporting             │
                   └──────────────────────────┘
```

## 📊 Variables Matrix

### QA-Automation-Config (Existing)

| # | Variable | Example Value | Type | Secret |
|---|----------|---------------|------|--------|
| 1 | BROWSERSTACK_USERNAME | nbhandari_KMkNq9 | String | No |
| 2 | BROWSERSTACK_ACCESS_KEY | 1tnaMGT6bqxfiTNX9zd7 | String | 🔒 Yes |
| 3 | FH_BASE_URL | https://fh-test-fourhandscom... | URL | No |
| 4 | FH_USERNAME | your_fh_email@example.com | Email | No |
| 5 | FH_PASSWORD | your_fh_password | String | 🔒 Yes |
| 6 | D365_BASE_URL | https://fourhands-test... | URL | No |
| 7 | D365_COMPANY | FH | String | No |
| 8 | D365_USERNAME | nbhandari@austin.fourhands.com | Email | No |
| 9 | D365_PASSWORD | Kathmandu1 | String | 🔒 Yes |
| 10 | HEADED | false | Boolean | No |
| 11 | TIMEOUT | 30000 | Number | No |

### Jira-Zephyr-Config (NEW)

| # | Variable | Example Value | Type | Secret |
|---|----------|---------------|------|--------|
| 1 | JIRA_BASE_URL | https://yourcompany.atlassian.net | URL | No |
| 2 | JIRA_EMAIL | nbhandari@austin.fourhands.com | Email | No |
| 3 | JIRA_API_TOKEN | ATATT3xFfGF0B... | Token | 🔒 Yes |
| 4 | JIRA_PROJECT_KEY | QA | String | No |
| 5 | JIRA_VERSION | v1.0.0 | String | No |

## 🎯 Quick Setup Visual Guide

### Step 1: Navigate to Library
```
Azure DevOps → Pipelines → Library
```

### Step 2: Create First Group
```
┌─────────────────────────────────────────┐
│  + Variable group                       │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Variable group name:                   │
│  QA-Automation-Config                   │
│                                         │
│  Description:                           │
│  Application and test configuration     │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Add variables (11 total):              │
│  [Name]         [Value]          [🔒]   │
│  BROWSERSTACK_USERNAME  nbhandari...    │
│  BROWSERSTACK_ACCESS_KEY  1tna...  ✓   │
│  ...                                    │
└─────────────────────────────────────────┘
```

### Step 3: Create Second Group
```
┌─────────────────────────────────────────┐
│  + Variable group                       │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Variable group name:                   │
│  Jira-Zephyr-Config                     │
│                                         │
│  Description:                           │
│  Jira and Zephyr Scale integration      │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Add variables (5 total):               │
│  [Name]         [Value]          [🔒]   │
│  JIRA_BASE_URL    https://...           │
│  JIRA_EMAIL       nbhandari...          │
│  JIRA_API_TOKEN   ATATT3x...       ✓   │
│  JIRA_PROJECT_KEY QA                    │
│  JIRA_VERSION     v1.0.0                │
└─────────────────────────────────────────┘
```

### Step 4: Set Pipeline Permissions
```
For EACH variable group:

┌─────────────────────────────────────────┐
│  Pipeline permissions                   │
│                                         │
│  + [Add pipeline]                       │
│    → Select: your-pipeline-name         │
│    → Click: Authorize                   │
│                                         │
│  ✓ your-pipeline-name [Authorized]      │
└─────────────────────────────────────────┘
```

## 🔐 Security Checklist

```
Variables that MUST be marked as SECRET (🔒):

✅ BROWSERSTACK_ACCESS_KEY
   └─ Click lock icon when adding

✅ FH_PASSWORD
   └─ Click lock icon when adding

✅ D365_PASSWORD
   └─ Click lock icon when adding

✅ JIRA_API_TOKEN ⚠️ MOST IMPORTANT!
   └─ Click lock icon when adding
```

## 📝 Copy-Paste Template for Azure DevOps

### Creating Variables in Azure DevOps UI

**For QA-Automation-Config:**
```
Click "+ Add" for each variable below:

Name: BROWSERSTACK_USERNAME
Value: nbhandari_KMkNq9
Secret: [ ]

Name: BROWSERSTACK_ACCESS_KEY
Value: 1tnaMGT6bqxfiTNX9zd7
Secret: [✓]  ← CHECK THIS BOX!

Name: FH_BASE_URL
Value: https://fh-test-fourhandscom.azurewebsites.net
Secret: [ ]

Name: FH_USERNAME
Value: your_fh_email@example.com
Secret: [ ]

Name: FH_PASSWORD
Value: your_fh_password
Secret: [✓]  ← CHECK THIS BOX!

Name: D365_BASE_URL
Value: https://fourhands-test.sandbox.operations.dynamics.com
Secret: [ ]

Name: D365_COMPANY
Value: FH
Secret: [ ]

Name: D365_USERNAME
Value: nbhandari@austin.fourhands.com
Secret: [ ]

Name: D365_PASSWORD
Value: Kathmandu1
Secret: [✓]  ← CHECK THIS BOX!

Name: HEADED
Value: false
Secret: [ ]

Name: TIMEOUT
Value: 30000
Secret: [ ]
```

**For Jira-Zephyr-Config:**
```
Click "+ Add" for each variable below:

Name: JIRA_BASE_URL
Value: https://yourcompany.atlassian.net
Secret: [ ]
NOTE: Replace with your actual Jira URL!

Name: JIRA_EMAIL
Value: nbhandari@austin.fourhands.com
Secret: [ ]

Name: JIRA_API_TOKEN
Value: ATATT3xFfGF0BxUlEOAQG-AWfFM1_93IEf8OKMIPgxBDPzlTeR5MmPAnOg_7unFzVOW7MsGukdrpbWw05eouwbYDtyIp2SWCpnQPjeZqU4CqzXk25tHv0T6RUouvZoK3-oBmfjO-3lGm5QD7omsEeCDx2X0gdLT9gDqn1i34TVWaVaGo=C852BE5A
Secret: [✓]  ← CHECK THIS BOX! VERY IMPORTANT!

Name: JIRA_PROJECT_KEY
Value: QA
Secret: [ ]
NOTE: Replace with your actual project key!

Name: JIRA_VERSION
Value: v1.0.0
Secret: [ ]
NOTE: Optional - can leave blank
```

## ✅ Verification Checklist

After creating both variable groups:

```
□ QA-Automation-Config group exists
□ QA-Automation-Config has 11 variables
□ Jira-Zephyr-Config group exists
□ Jira-Zephyr-Config has 5 variables
□ BROWSERSTACK_ACCESS_KEY marked as secret (lock icon visible)
□ FH_PASSWORD marked as secret (lock icon visible)
□ D365_PASSWORD marked as secret (lock icon visible)
□ JIRA_API_TOKEN marked as secret (lock icon visible) ⚠️
□ Both groups linked to your pipeline (Pipeline permissions tab)
□ Pipeline has "Authorized" status for both groups
□ Saved both variable groups
```

## 🎓 Visual Reference: Secret vs Non-Secret

```
NON-SECRET Variable:
┌──────────────────────────────────┐
│ Name:  JIRA_BASE_URL             │
│ Value: https://yourcompany...    │  ← Value is visible
│ [ ] Keep this value secret       │  ← Checkbox UNCHECKED
└──────────────────────────────────┘

SECRET Variable:
┌──────────────────────────────────┐
│ Name:  JIRA_API_TOKEN            │
│ Value: ************************  │  ← Value is hidden
│ [✓] Keep this value secret       │  ← Checkbox CHECKED
│ 🔒                               │  ← Lock icon appears
└──────────────────────────────────┘
```

## 📞 Need Help?

**Can't find Variable Groups?**
```
Azure DevOps → Left sidebar → Pipelines → Library
```

**Can't mark variable as secret?**
```
When adding variable, look for checkbox:
"[ ] Keep this value secret"
Check it BEFORE saving!
```

**Pipeline can't access variables?**
```
Variable Group → Pipeline permissions tab
Click "+ [Add pipeline]"
Select your pipeline
Click "Authorize"
```

---

**Total Variables Needed:** 16  
**Secret Variables:** 4  
**Variable Groups:** 2  
**Setup Time:** ~10 minutes
