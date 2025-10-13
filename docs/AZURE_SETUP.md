# Azure DevOps Setup Guide
## Four Hands QA Automation Framework

This guide will help you set up the Four Hands QA Automation Framework with Azure DevOps CI/CD pipelines.

---

## 📋 Prerequisites

- Azure DevOps organization and project
- Azure subscription (for Azure Key Vault)
- Admin access to Azure DevOps
- Git repository access

---

## 🔐 Step 1: Configure Azure Key Vault

### 1.1 Create Azure Key Vault

```bash
# Azure CLI commands
az keyvault create \
  --name fourhands-qa-keyvault \
  --resource-group fourhands-qa-rg \
  --location eastus
```

### 1.2 Add Secrets to Key Vault

Add the following secrets:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `D365-BASE-URL` | D365 environment URL | `https://fourhands.operations.dynamics.com` |
| `D365-USERNAME` | D365 login email | `qa-test@fourhands.com` |
| `D365-PASSWORD` | D365 password | `SecurePassword123!` |
| `FH-BASE-URL` | FourHands base URL | `https://www.fourhands.com` |
| `FH-USERNAME` | FourHands login email | `qa-test@fourhands.com` |
| `FH-PASSWORD` | FourHands password | `SecurePassword123!` |
| `BROWSERSTACK-USERNAME` | BrowserStack username | `your_bs_username` |
| `BROWSERSTACK-ACCESS-KEY` | BrowserStack access key | `your_bs_access_key` |

```bash
# Example: Add secrets via Azure CLI
az keyvault secret set --vault-name fourhands-qa-keyvault --name "D365-USERNAME" --value "qa-test@fourhands.com"
az keyvault secret set --vault-name fourhands-qa-keyvault --name "D365-PASSWORD" --value "YourSecurePassword"
```

---

## 🔗 Step 2: Create Azure Service Connection

### 2.1 Create Service Principal

1. Go to **Azure DevOps** → **Project Settings** → **Service connections**
2. Click **New service connection**
3. Select **Azure Resource Manager**
4. Choose **Service principal (automatic)**
5. Configure:
   - **Scope level**: Subscription
   - **Subscription**: Select your Azure subscription
   - **Resource group**: `fourhands-qa-rg`
   - **Service connection name**: `FourHands-AzureServiceConnection`
6. Click **Save**

### 2.2 Grant Key Vault Access

```bash
# Get the service principal ID
SP_ID=$(az ad sp list --display-name "FourHands-AzureServiceConnection" --query "[0].id" -o tsv)

# Grant Key Vault access
az keyvault set-policy \
  --name fourhands-qa-keyvault \
  --spn $SP_ID \
  --secret-permissions get list
```

---

## 📦 Step 3: Import Repository to Azure DevOps

### 3.1 Create New Repository

1. Go to **Azure DevOps** → **Repos** → **Files**
2. Click **Import repository**
3. Clone URL: Your GitHub repository URL
4. Repository name: `fourhands-qa-automation`
5. Click **Import**

### 3.2 Or Push Existing Code

```bash
# Add Azure DevOps remote
git remote add azure https://dev.azure.com/fourhands/QA/_git/fourhands-qa-automation

# Push code
git push azure main
```

---

## 🚀 Step 4: Create Azure Pipelines

### 4.1 Main CI/CD Pipeline

1. Go to **Azure DevOps** → **Pipelines** → **New pipeline**
2. Select **Azure Repos Git**
3. Choose your repository: `fourhands-qa-automation`
4. Select **Existing Azure Pipelines YAML file**
5. Path: `/azure-pipelines.yml`
6. Click **Continue** → **Run**

### 4.2 PR Validation Pipeline

1. Go to **Pipelines** → **New pipeline**
2. Select **Azure Repos Git**
3. Choose your repository
4. Select **Existing Azure Pipelines YAML file**
5. Path: `/azure-pipelines-pr.yml`
6. Click **Continue** → **Save**

### 4.3 BrowserStack Pipeline

1. Go to **Pipelines** → **New pipeline**
2. Select **Azure Repos Git**
3. Choose your repository
4. Select **Existing Azure Pipelines YAML file**
5. Path: `/azure-pipelines-browserstack.yml`
6. Click **Continue** → **Save**

---

## ⚙️ Step 5: Configure Pipeline Variables

### 5.1 Pipeline-Level Variables (Optional)

Add these if not using Key Vault for everything:

1. Go to **Pipelines** → Select your pipeline → **Edit**
2. Click **Variables** (top right)
3. Add variables:
   - `D365-BASE-URL`: `https://fourhands.operations.dynamics.com`
   - `FH-BASE-URL`: `https://www.fourhands.com`

### 5.2 Variable Groups (Recommended)

1. Go to **Pipelines** → **Library** → **+ Variable group**
2. Name: `QA-Automation-Config`
3. Add variables:
   - `D365-BASE-URL`
   - `FH-BASE-URL`
   - `TIMEOUT`: `30000`
   - `HEADED`: `false`
4. **Link secrets from Azure Key Vault**:
   - Enable **Link secrets from an Azure key vault**
   - Azure subscription: `FourHands-AzureServiceConnection`
   - Key vault name: `fourhands-qa-keyvault`
   - Add all secrets
5. Save

### 5.3 Update Pipelines to Use Variable Group

Add this to each pipeline YAML after `variables:`:

```yaml
variables:
  - group: QA-Automation-Config
```

---

## 🔔 Step 6: Configure Notifications

### 6.1 Email Notifications

1. Go to **Project Settings** → **Notifications**
2. Click **New subscription**
3. Configure:
   - **Category**: Build
   - **Template**: Build completes
   - **Filter**: Pipeline = `fourhands-qa-automation`
   - **Deliver to**: QA team email
4. Save

### 6.2 Slack Integration (Optional)

```bash
# Install Azure Pipelines app in Slack
# Subscribe to pipeline in Slack channel:
@azure subscribe https://dev.azure.com/fourhands/QA/_build?definitionId=<pipeline-id>
```

---

## 📊 Step 7: Configure Test Reporting

### 7.1 Enable Test Results

Test results are automatically published by the pipeline. View them:

1. Go to **Pipelines** → **Runs**
2. Select a completed run
3. Click **Tests** tab

### 7.2 Enable Code Coverage (Optional)

Add to `azure-pipelines.yml`:

```yaml
- script: |
    pytest tests/ --cov=. --cov-report=xml --cov-report=html
  displayName: 'Run Tests with Coverage'

- task: PublishCodeCoverageResults@1
  inputs:
    codeCoverageTool: 'Cobertura'
    summaryFileLocation: 'coverage.xml'
```

### 7.3 Allure Report Dashboard

Deploy Allure report to Azure Storage or App Service:

```yaml
- task: AzureWebApp@1
  displayName: 'Deploy Allure Report'
  inputs:
    azureSubscription: 'FourHands-AzureServiceConnection'
    appName: 'fourhands-allure-reports'
    package: 'reports/allure-report'
```

---

## 🎯 Step 8: Branch Policies

### 8.1 Protect Main Branch

1. Go to **Repos** → **Branches**
2. Click `main` → **Branch policies**
3. Enable:
   - **Require a minimum number of reviewers**: 1
   - **Check for linked work items**: Optional
   - **Build validation**: Add `azure-pipelines-pr.yml`
4. Save

### 8.2 Build Validation Rules

- **PR to main**: Runs `azure-pipelines-pr.yml` (smoke tests)
- **Push to main**: Runs `azure-pipelines.yml` (full E2E)
- **Scheduled nightly**: Runs `azure-pipelines-browserstack.yml`

---

## 🔍 Step 9: Verify Setup

### 9.1 Manual Test Run

1. Go to **Pipelines** → Select `azure-pipelines.yml`
2. Click **Run pipeline**
3. Verify:
   - ✅ Python installation
   - ✅ Dependency installation
   - ✅ Playwright browser installation
   - ✅ Key Vault secrets fetched
   - ✅ Tests execute successfully
   - ✅ Allure report generated

### 9.2 PR Validation Test

1. Create a test branch
2. Make a small change
3. Create Pull Request to `main`
4. Verify PR pipeline triggers automatically
5. Check test results in PR comments

### 9.3 BrowserStack Test

1. Go to **Pipelines** → `azure-pipelines-browserstack.yml`
2. Click **Run pipeline**
3. Select parameters:
   - Test Suite: `smoke`
   - Browsers: `chrome,edge,safari`
4. Run and verify on BrowserStack dashboard

---

## 📈 Step 10: Monitoring & Dashboards

### 10.1 Azure DevOps Dashboard

1. Go to **Overview** → **Dashboards**
2. Create new dashboard: `QA Automation`
3. Add widgets:
   - **Build History**: Shows pipeline trends
   - **Test Results**: Shows pass/fail trends
   - **Deployment Status**: Shows deployment history

### 10.2 Custom Queries

Create work item queries:

```
Work Item Type = Bug
AND Tags Contains 'automation-failure'
AND State = Active
```

---

## 🛠️ Troubleshooting

### Issue: Key Vault Access Denied

**Solution:**
```bash
# Verify service connection permissions
az keyvault set-policy --name fourhands-qa-keyvault \
  --spn <service-principal-id> \
  --secret-permissions get list
```

### Issue: Playwright Browser Installation Fails

**Solution:**
Add to pipeline:
```yaml
- script: |
    playwright install-deps
    playwright install chromium
  displayName: 'Install Playwright'
```

### Issue: Tests Timeout

**Solution:**
Increase timeout in pipeline:
```yaml
jobs:
  - job: Tests
    timeoutInMinutes: 60
```

---

## 📞 Support

- **Azure DevOps Docs**: https://docs.microsoft.com/azure/devops
- **Playwright Docs**: https://playwright.dev
- **BrowserStack Docs**: https://www.browserstack.com/docs

---

## ✅ Checklist

- [ ] Azure Key Vault created and configured
- [ ] Service connection created
- [ ] Repository imported to Azure DevOps
- [ ] All 3 pipelines created
- [ ] Variable group configured
- [ ] Branch policies enabled
- [ ] Notifications configured
- [ ] First successful pipeline run
- [ ] PR validation tested
- [ ] BrowserStack pipeline tested

**Once all items are checked, your Azure DevOps CI/CD is ready! 🎉**
