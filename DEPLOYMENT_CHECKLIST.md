# Jira Integration - Deployment Checklist

## 🎯 Pre-Deployment Checklist

### 1. Azure DevOps Setup
- [ ] Navigate to Azure DevOps → Pipelines → Library
- [ ] Create variable group named: `Jira-Zephyr-Config`
- [ ] Add variable: `JIRA_BASE_URL` = `https://yourcompany.atlassian.net`
- [ ] Add variable: `JIRA_EMAIL` = `your.email@company.com`
- [ ] Add variable: `JIRA_API_TOKEN` = (use provided token)
- [ ] Add variable: `JIRA_PROJECT_KEY` = `QA` (or your project key)
- [ ] Mark `JIRA_API_TOKEN` as **SECRET** (click lock icon) ⚠️
- [ ] Click "Save" on variable group
- [ ] Verify pipeline has access to variable group

### 2. Local Testing (Optional but Recommended)
- [ ] Run: `python scripts/setup_jira.py`
- [ ] Verify Jira connection works
- [ ] Verify project access
- [ ] Create test cycle to verify setup
- [ ] Review generated .env file

### 3. Code Review
- [ ] Review `azure-pipelines.yml` changes
- [ ] Review `utils/jira_integration.py`
- [ ] Review `conftest_jira.py`
- [ ] Verify API token is not hardcoded in any committed files
- [ ] Check `.gitignore` includes `.env`

### 4. Test Preparation
- [ ] Identify tests to link with Jira
- [ ] Create test cases in Jira (if not already exists)
- [ ] Note test case keys (e.g., TEST-101, TEST-102, etc.)
- [ ] Add `@pytest.mark.jira('TEST-XXX')` markers to tests
- [ ] Create at least 3-5 test examples with markers

### 5. Documentation Review
- [ ] Read `JIRA_QUICKSTART.md`
- [ ] Review `docs/JIRA_INTEGRATION.md`
- [ ] Check `JIRA_IMPLEMENTATION_SUMMARY.md`
- [ ] Review example tests in `tests/test_jira_example.py`

---

## 🚀 Deployment Steps

### Step 1: Commit Changes
```bash
git status
git add .
git commit -m "feat: Add Jira/Zephyr integration to CI/CD pipeline"
```

### Step 2: Push to Feature Branch (Recommended)
```bash
git checkout -b feature/jira-integration
git push origin feature/jira-integration
```

### Step 3: Create Pull Request
- [ ] Create PR from feature branch to main/develop
- [ ] Add description of changes
- [ ] Link to this deployment checklist
- [ ] Request review from team lead

### Step 4: Monitor First Pipeline Run
- [ ] Watch pipeline execution in Azure DevOps
- [ ] Check "Setup_Jira_Test_Cycle" job completes successfully
- [ ] Verify test cycle is created in Jira
- [ ] Check "Smoke_Tests" job updates Jira
- [ ] Check "E2E_Tests" job updates Jira
- [ ] Verify "Update_Jira_Summary" finalizes cycle

### Step 5: Verify in Jira
- [ ] Open Jira → Your Project
- [ ] Navigate to Zephyr Scale
- [ ] Find test cycle: "Automated Test Run - Build {number}"
- [ ] Verify test executions are showing Pass/Fail
- [ ] Check cycle status is "Done"
- [ ] If there were failures, verify bugs were created

---

## ✅ Post-Deployment Verification

### Smoke Test (Day 1)
- [ ] Run pipeline manually
- [ ] Verify test cycle created
- [ ] Verify at least 5 tests updated in Jira
- [ ] Check Allure report generated
- [ ] Verify no pipeline errors

### Integration Test (Day 2-3)
- [ ] Run full test suite via pipeline
- [ ] Verify all marked tests update in Jira
- [ ] Intentionally fail a test to verify defect creation
- [ ] Check defect format and information
- [ ] Verify test traceability (test → test case → story)

### Team Onboarding (Week 1)
- [ ] Share `JIRA_QUICKSTART.md` with team
- [ ] Demonstrate test cycle in Jira
- [ ] Show how to add markers to tests
- [ ] Train on defect triage workflow
- [ ] Answer team questions

---

## 🐛 Troubleshooting Quick Reference

### Issue: "401 Unauthorized"
**Fix:** 
- Verify API token is correct
- Check email matches Jira account
- Regenerate token if needed at: https://id.atlassian.com/manage-profile/security/api-tokens

### Issue: "404 Not Found"
**Fix:**
- Verify `JIRA_BASE_URL` has no trailing slash
- Check project key is correct
- Ensure Zephyr Scale is installed

### Issue: Test results not updating
**Fix:**
- Verify test has `@pytest.mark.jira('TEST-XXX')` marker
- Check test case key exists in Jira
- Ensure test case is in the test cycle
- Review pipeline logs for API errors

### Issue: Pipeline fails at "Setup_Jira_Test_Cycle"
**Fix:**
- Verify variable group exists and is linked
- Check all required variables are set
- Ensure `JIRA_API_TOKEN` is marked as secret
- Test connection with: `python scripts/setup_jira.py`

### Issue: Defects not created
**Fix:**
- Check pipeline logs for "create-defects" step
- Verify user has permission to create bugs in Jira
- Check issue type "Bug" exists in project
- Review required fields in project settings

---

## 📊 Success Criteria

After deployment, you should see:

### In Azure DevOps:
✅ Pipeline runs successfully end-to-end
✅ All stages complete without errors
✅ Test results published
✅ Allure reports generated
✅ Console shows Jira URLs

### In Jira:
✅ New test cycle created for each build
✅ Test executions show Pass/Fail status
✅ Execution times recorded
✅ Test cycle marked as "Done" after run
✅ Defects created for failures (if any)

### For Team:
✅ QA can view test results in Jira
✅ Developers can see which tests failed
✅ Managers can track test coverage
✅ Full traceability: Code → Tests → Test Cases → Stories

---

## 📝 Rollback Plan

If integration causes issues:

### Option 1: Disable Jira Integration (Keep Pipeline Working)
1. Comment out Jira-related steps in `azure-pipelines.yml`:
```yaml
# - script: python utils/jira_integration.py create-cycle ...
#   displayName: 'Create Zephyr Test Cycle'
```

2. Remove Jira environment variables from test stages
3. Pipeline will still run tests, just won't update Jira

### Option 2: Revert to Previous Pipeline
```bash
git revert HEAD
git push origin main
```

### Option 3: Use Previous Pipeline Version
1. Go to Azure DevOps → Pipelines → Edit
2. Click on "..." → "History"
3. Select previous version
4. Click "Restore"

---

## 🎓 Training Resources

Share with team members:

**Quick Start:**
- `JIRA_QUICKSTART.md` - 5-minute overview

**Detailed Guides:**
- `docs/JIRA_INTEGRATION.md` - Complete documentation
- `JIRA_IMPLEMENTATION_SUMMARY.md` - Technical details

**Examples:**
- `tests/test_jira_example.py` - Sample tests with markers

**Tools:**
- `scripts/setup_jira.py` - Test your Jira connection

---

## 📞 Support Contacts

**Technical Issues:**
- Review pipeline logs in Azure DevOps
- Check Jira API documentation
- Run: `python scripts/setup_jira.py` to diagnose

**Jira Access:**
- Contact Jira administrator
- Verify user permissions
- Check Zephyr Scale installation

**Team Questions:**
- Share documentation from `docs/` folder
- Schedule walkthrough session
- Create FAQ document based on common questions

---

## ✨ Next Steps After Deployment

### Week 1:
- [ ] Monitor first 5 pipeline runs
- [ ] Address any issues that arise
- [ ] Gather team feedback
- [ ] Update documentation if needed

### Week 2:
- [ ] Add Jira markers to remaining tests
- [ ] Review auto-created defects
- [ ] Establish defect triage process
- [ ] Create dashboard in Jira for metrics

### Month 1:
- [ ] Analyze test execution trends
- [ ] Optimize defect creation rules
- [ ] Train new team members
- [ ] Document lessons learned

---

## 🎉 Ready to Deploy?

If you can check all boxes above, you're ready!

**Final Command:**
```bash
git push origin feature/jira-integration
# Or if on main branch:
git push origin main
```

Then watch your pipeline run and see the magic happen in Jira! 🚀

---

**Checklist Created:** October 14, 2025  
**Version:** 1.0  
**Status:** Ready for deployment ✅
