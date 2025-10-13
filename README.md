# Four Hands QA Automation Framework

[![Azure Pipeline](https://dev.azure.com/fourhands/QA/_apis/build/status/qa-automation?branchName=main)](https://dev.azure.com/fourhands/QA/_build/latest?definitionId=1&branchName=main)
[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)](https://playwright.dev/)
[![BrowserStack](https://img.shields.io/badge/browserstack-enabled-orange.svg)](https://www.browserstack.com/)

Production-ready test automation framework for **Microsoft Dynamics 365 Finance & Operations** and **FourHands e-commerce platform** using **Playwright Python**.

---

## 🎯 Overview

### Key Features

- ✅ **40+ Automated Tests** across D365 and FourHands platforms
- ✅ **Playwright Python** - Modern, reliable browser automation
- ✅ **BrowserStack Integration** - Cross-browser cloud testing
- ✅ **Allure Reporting** - Beautiful test reports with screenshots & videos
- ✅ **Azure DevOps CI/CD** - Automated testing on every PR and deployment
- ✅ **Page Object Model** - Maintainable and scalable test architecture
- ✅ **Parallel Execution** - Fast test runs with pytest-xdist
- ✅ **Azure Key Vault** - Secure credential management

### Test Coverage

| Platform | Test Count | Coverage |
|----------|-----------|----------|
| **D365 F&O** | 4+ tests | Login, Sales Orders, Navigation |
| **FourHands** | 37+ tests | Cart, Checkout, Product Details |
| **Total** | 41+ tests | Core user journeys |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (3.11 recommended)
- Git
- Node.js 16+ (for Allure reports)

### Installation

```bash
# Clone repository
git clone https://dev.azure.com/fourhands/QA/_git/fourhands-qa-automation
cd fourhands-qa-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Run Tests

```bash
# Run smoke tests (fast)
./scripts/run_tests_local.sh smoke

# Run E2E tests
./scripts/run_tests_local.sh e2e

# Run on BrowserStack
./scripts/run_tests_browserstack.sh smoke

# Generate Allure report
./scripts/generate_allure_report.sh
```

---

## 📂 Project Structure

```
fourhands-qa-automation/
├── tests/                      # Test suites
│   ├── d365/                   # D365 F&O tests
│   └── fh/                     # FourHands e-commerce tests
├── pages/                      # Page Object Model
│   ├── d365/                   # D365 page objects
│   ├── fh/                     # FourHands page objects
│   └── base_page.py
├── utils/                      # Utilities & helpers
│   ├── waits.py
│   ├── auth_helper.py
│   └── env.py
├── configs/                    # Configuration files
│   ├── playwright_config.py
│   └── browserstack_config.py
├── scripts/                    # Helper scripts
│   ├── run_tests_local.sh
│   ├── run_tests_browserstack.sh
│   └── generate_allure_report.sh
├── docs/                       # Documentation
│   ├── AZURE_SETUP.md
│   ├── BROWSERSTACK_INTEGRATION.md
│   └── LOCAL_DEVELOPMENT.md
├── azure-pipelines.yml         # Main CI/CD pipeline
├── azure-pipelines-pr.yml      # PR validation
├── azure-pipelines-browserstack.yml  # BrowserStack tests
├── conftest.py                 # Pytest configuration
├── pytest.ini                  # Pytest settings
├── requirements.txt            # Python dependencies
└── browserstack.yml            # BrowserStack configuration
```

---

## 🔄 CI/CD Pipelines

### 1. Main Pipeline (azure-pipelines.yml)

**Triggers:** Push to `main` or `develop`

**Stages:**
1. **Smoke Tests** - Fast validation (2-3 minutes)
2. **E2E Tests** - Full regression (15-20 minutes)
3. **Allure Report** - Generate and publish reports

### 2. PR Validation (azure-pipelines-pr.yml)

**Triggers:** Pull Requests to `main` or `develop`

**Purpose:** Fast feedback on code changes (smoke tests only)

### 3. BrowserStack Pipeline (azure-pipelines-browserstack.yml)

**Triggers:** Scheduled (nightly) or Manual

**Purpose:** Cross-browser testing on real devices

**Parameters:**
- Test Suite: `smoke` | `e2e` | `all`
- Browsers: `chrome,edge,safari`
- OS: `Windows` | `OS X` | `Both`

---

## 🧪 Test Categories

### Test Markers

| Marker | Description | Usage |
|--------|-------------|-------|
| `smoke` | Quick smoke tests | `pytest -m smoke` |
| `e2e` | End-to-end tests | `pytest -m e2e` |
| `d365` | D365 ERP tests | `pytest -m d365` |
| `fourhands` | FourHands tests | `pytest -m fourhands` |
| `cart` | Shopping cart tests | `pytest -m cart` |
| `checkout` | Checkout tests | `pytest -m checkout` |
| `slow` | Slow-running tests | `pytest -m "not slow"` |

### Example Usage

```bash
# Run only smoke tests
pytest tests/ -m smoke -v

# Run FourHands E2E tests
pytest tests/fh/ -m e2e -v

# Run all except slow tests
pytest tests/ -m "not slow" -v

# Run cart and checkout tests
pytest tests/ -m "cart or checkout" -v
```

---

## 📊 Reporting

### Allure Reports

Beautiful, interactive test reports with:
- 📸 Screenshots on every step
- 🎬 Video recordings
- 📋 Page HTML captures
- ⏱️ Execution timeline
- 📈 Historical trends
- 🏷️ Test categorization

**View Reports:**
```bash
# Local
./scripts/generate_allure_report.sh

# Azure DevOps
# Navigate to: Pipeline Run → Artifacts → allure-report
```

### BrowserStack Dashboard

Access test sessions with video recordings:
- URL: https://automate.browserstack.com/dashboard/v2
- Features: Live debugging, network logs, console logs

---

## 🔐 Configuration

### Environment Variables

Required environment variables (configured in Azure Key Vault):

| Variable | Description |
|----------|-------------|
| `D365_BASE_URL` | D365 environment URL |
| `D365_USERNAME` | D365 login email |
| `D365_PASSWORD` | D365 password |
| `FH_BASE_URL` | FourHands base URL |
| `FH_USERNAME` | FourHands login email |
| `FH_PASSWORD` | FourHands password |
| `BROWSERSTACK_USERNAME` | BrowserStack username |
| `BROWSERSTACK_ACCESS_KEY` | BrowserStack access key |

### Local Setup

Create `.env` file from template:
```bash
cp .env.example .env
# Edit with your credentials
```

### Azure DevOps Setup

1. Configure Azure Key Vault
2. Add secrets to Key Vault
3. Update service connection in pipelines

See: [docs/AZURE_SETUP.md](docs/AZURE_SETUP.md)

---

## 🛠️ Development

### Writing New Tests

```python
import pytest
import allure
from playwright.sync_api import Page

@allure.feature("Shopping Cart")
@pytest.mark.smoke
@pytest.mark.fourhands
def test_add_to_cart(authenticated_page: Page):
    """Test adding product to cart"""
    with allure.step("Navigate to product page"):
        authenticated_page.goto("/product/123")
    
    with allure.step("Add to cart"):
        authenticated_page.click("button[data-testid='add-to-cart']")
    
    with allure.step("Verify cart count"):
        cart_count = authenticated_page.text_content(".cart-count")
        assert cart_count == "1", "Cart should contain 1 item"
```

### Page Object Example

```python
from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_to_cart_btn = "button[data-testid='add-to-cart']"
    
    def add_to_cart(self):
        self.page.click(self.add_to_cart_btn)
        self.wait_for_load_state()
```

### Running Tests

```bash
# Local (visible browser)
pytest tests/ -v --headed

# Headless
pytest tests/ -v

# Parallel execution
pytest tests/ -n auto -v

# With Allure
pytest tests/ -v --alluredir=reports/allure-results
```

---

## 📚 Documentation

- [Azure DevOps Setup Guide](docs/AZURE_SETUP.md)
- [BrowserStack Integration](docs/BROWSERSTACK_INTEGRATION.md)
- [Local Development Guide](docs/LOCAL_DEVELOPMENT.md)

---

## 🤝 Contributing

### Branch Strategy

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
./scripts/run_tests_local.sh smoke

# Commit with conventional commits
git commit -m "feat: Add checkout validation tests"

# Push and create PR
git push origin feature/your-feature-name
```

### Commit Convention

```
<type>(<scope>): <subject>

Types: feat, fix, test, docs, refactor, chore

Examples:
- feat(cart): Add save-for-later tests
- fix(d365): Resolve login timeout
- test(checkout): Add payment validation
- docs: Update setup guide
```

### Code Quality

```bash
# Format code
black tests/ pages/ utils/

# Lint
flake8 tests/ pages/ utils/

# Type checking
mypy tests/ pages/ utils/
```

---

## 🎯 Success Metrics

- **Test Coverage:** 85%+
- **Execution Time:** <20 minutes (full E2E suite)
- **Pass Rate:** 95%+
- **PR Validation:** <5 minutes
- **BrowserStack Compatibility:** Chrome, Safari, Edge

---

## 🔧 Troubleshooting

### Common Issues

**Import Errors:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Browser Not Found:**
```bash
playwright install chromium
```

**Authentication Failures:**
```bash
# Check .env file
# Recreate auth session if needed
```

See [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) for more details.

---

## 📞 Support

- **Documentation:** [docs/](docs/)
- **Internal Wiki:** https://wiki.fourhands.com/qa
- **Slack:** #qa-automation
- **Team:** QA Automation Team
- **Playwright Docs:** https://playwright.dev
- **BrowserStack Docs:** https://www.browserstack.com/docs

---

## 📝 License

Proprietary - FourHands Internal Use Only

---

## 🙏 Acknowledgments

Built with:
- [Playwright](https://playwright.dev/) - Modern browser automation
- [Pytest](https://docs.pytest.org/) - Python testing framework
- [Allure](https://docs.qameta.io/allure/) - Test reporting
- [BrowserStack](https://www.browserstack.com/) - Cross-browser testing
- [Azure DevOps](https://azure.microsoft.com/en-us/services/devops/) - CI/CD platform

---

**Built with ❤️ by the Four Hands QA Automation Team**

**Version:** 2.0.0  
**Last Updated:** October 2025  
**Maintained by:** Nischal Bhandari & QA Team
