# Local Development Guide
## Four Hands QA Automation Framework

Complete guide for setting up and running tests locally.

---

## 📋 Prerequisites

- **Python 3.8+** (recommended: Python 3.11)
- **Git**
- **Node.js 16+** (for Allure reports)
- **Code Editor** (VS Code recommended)

---

## 🚀 Step 1: Initial Setup

### 1.1 Clone Repository

```bash
# Clone from Azure DevOps
git clone https://dev.azure.com/fourhands/QA/_git/fourhands-qa-automation
cd fourhands-qa-automation

# Or from GitHub (if using GitHub)
git clone https://github.com/fourhands/qa-automation.git
cd qa-automation
```

### 1.2 Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 1.3 Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Optional: Install all browsers
playwright install
```

### 1.4 Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
nano .env  # or use your preferred editor
```

**.env file example:**
```bash
# D365 Configuration
D365_BASE_URL=https://fourhands-test.sandbox.operations.dynamics.com
D365_COMPANY=FH
D365_USERNAME=qa-test@fourhands.com
D365_PASSWORD=YourSecurePassword

# FourHands Configuration
FH_BASE_URL=https://fh-test-fourhandscom.azurewebsites.net
FH_USERNAME=qa-test@fourhands.com
FH_PASSWORD=YourSecurePassword

# BrowserStack Configuration (optional for local runs)
BROWSERSTACK_USERNAME=your_bs_username
BROWSERSTACK_ACCESS_KEY=your_bs_access_key

# Test Configuration
HEADED=true
TIMEOUT=30000
```

---

## 🧪 Step 2: Running Tests Locally

### 2.1 Using Helper Scripts (Recommended)

```bash
# Make scripts executable (first time only)
chmod +x scripts/*.sh

# Run smoke tests
./scripts/run_tests_local.sh smoke

# Run E2E tests
./scripts/run_tests_local.sh e2e

# Run all tests
./scripts/run_tests_local.sh all

# Run specific module
./scripts/run_tests_local.sh d365
./scripts/run_tests_local.sh fourhands
```

### 2.2 Using Pytest Directly

```bash
# Run all tests
pytest tests/ -v --headed

# Run smoke tests only
pytest tests/ -m smoke -v --headed

# Run E2E tests only
pytest tests/ -m e2e -v --headed

# Run specific test file
pytest tests/d365/test_d365_sales_order.py -v --headed

# Run specific test
pytest tests/fh/test_fh_cart.py::test_add_to_cart -v --headed

# Run with Allure reporting
pytest tests/ -m smoke -v --headed --alluredir=reports/allure-results
```

### 2.3 Pytest Options

| Option | Description |
|--------|-------------|
| `-v` | Verbose output |
| `--headed` | Run in headed mode (visible browser) |
| `-s` | Show print statements |
| `-x` | Stop after first failure |
| `--maxfail=N` | Stop after N failures |
| `-k "pattern"` | Run tests matching pattern |
| `-m "marker"` | Run tests with specific marker |
| `--tb=short` | Short traceback format |
| `-n auto` | Parallel execution (requires pytest-xdist) |

**Examples:**
```bash
# Run tests with "cart" in name
pytest tests/ -k "cart" -v

# Run only smoke tests for FourHands
pytest tests/fh/ -m smoke -v

# Stop after 3 failures
pytest tests/ --maxfail=3 -v

# Parallel execution (faster)
pytest tests/ -n auto -v
```

---

## 📊 Step 3: Viewing Test Results

### 3.1 Allure Reports (Recommended)

**Install Allure CLI:**
```bash
# Using npm
npm install -g allure-commandline

# Verify installation
allure --version
```

**Generate and view report:**
```bash
# After running tests with --alluredir flag
./scripts/generate_allure_report.sh

# Or manually
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

**Allure report includes:**
- Test execution summary
- Test history and trends
- Screenshots on failure
- Page HTML captures
- Video recordings
- Step-by-step breakdowns

### 3.2 Console Output

Basic pytest output in terminal:
```
tests/fh/test_fh_cart.py::test_add_to_cart PASSED      [10%]
tests/fh/test_fh_cart.py::test_remove_item PASSED      [20%]
tests/fh/test_fh_cart.py::test_update_quantity PASSED  [30%]
...
=================== 10 passed in 45.23s ====================
```

### 3.3 JUnit XML Reports

```bash
# Generate JUnit XML
pytest tests/ --junitxml=reports/junit/results.xml

# View in CI/CD tools or Jenkins
```

---

## 🐛 Step 4: Debugging Tests

### 4.1 VS Code Setup

**Install Python extension:**
1. Open VS Code
2. Install **Python** extension by Microsoft
3. Install **Playwright Test for VSCode** extension

**Debug configuration (.vscode/launch.json):**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Pytest: Current File",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "${file}",
        "-v",
        "--headed",
        "-s"
      ],
      "console": "integratedTerminal",
      "justMyCode": false
    },
    {
      "name": "Pytest: Smoke Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "tests/",
        "-m",
        "smoke",
        "-v",
        "--headed"
      ],
      "console": "integratedTerminal"
    }
  ]
}
```

### 4.2 Playwright Inspector

```bash
# Run with inspector (step-through debugging)
PWDEBUG=1 pytest tests/fh/test_fh_cart.py::test_add_to_cart -v

# Windows
set PWDEBUG=1
pytest tests/fh/test_fh_cart.py::test_add_to_cart -v
```

**Inspector features:**
- Step through test actions
- Inspect page elements
- View selectors
- Record actions
- Edit locators live

### 4.3 Using Breakpoints

**In test code:**
```python
def test_example(page):
    page.goto("https://example.com")
    
    # Add breakpoint
    import pdb; pdb.set_trace()
    
    page.click("button")
```

**Run with debugger:**
```bash
pytest tests/fh/test_fh_cart.py -s
```

### 4.4 Slow Motion

```bash
# Slow down test execution (ms delay between actions)
pytest tests/ --headed --slowmo=1000
```

### 4.5 Screenshots & Videos

**Capture on failure (automatic):**
```python
# Already configured in conftest.py
# Screenshots saved to: test-results/
```

**Manual screenshots:**
```python
def test_example(page):
    page.goto("https://example.com")
    page.screenshot(path="debug-screenshot.png")
```

**Video recording:**
```python
# Enabled by default in conftest.py
# Videos saved to: test-results/videos/
```

---

## 🔧 Step 5: Writing New Tests

### 5.1 Test Structure

```python
import pytest
import allure
from playwright.sync_api import Page

@allure.feature("Shopping Cart")
@allure.story("Add to Cart")
@pytest.mark.smoke
@pytest.mark.fourhands
def test_add_product_to_cart(authenticated_page: Page):
    """
    Test: Add product to cart from PDP
    
    Steps:
    1. Navigate to product page
    2. Click "Add to Cart"
    3. Verify cart count increases
    """
    with allure.step("Navigate to product page"):
        authenticated_page.goto("https://example.com/product/123")
    
    with allure.step("Add product to cart"):
        authenticated_page.click("button[data-testid='add-to-cart']")
    
    with allure.step("Verify cart count"):
        cart_count = authenticated_page.text_content(".cart-count")
        assert cart_count == "1"
```

### 5.2 Page Object Pattern

**Create new page object:**
```python
# pages/fh/fh_product_page.py
from pages.base_page import BasePage
from playwright.sync_api import Page

class FHProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_to_cart_btn = "button[data-testid='add-to-cart']"
        self.product_title = "h1.product-title"
        self.product_price = ".product-price"
    
    def add_to_cart(self):
        """Add current product to cart"""
        self.page.click(self.add_to_cart_btn)
        self.wait_for_load_state()
    
    def get_product_title(self) -> str:
        """Get product title"""
        return self.page.text_content(self.product_title)
```

**Use in test:**
```python
def test_add_to_cart(authenticated_page: Page):
    product_page = FHProductPage(authenticated_page)
    product_page.goto("/product/123")
    product_page.add_to_cart()
```

### 5.3 Test Markers

Available markers (defined in `pytest.ini`):

| Marker | Description |
|--------|-------------|
| `@pytest.mark.smoke` | Quick smoke tests |
| `@pytest.mark.e2e` | End-to-end tests |
| `@pytest.mark.d365` | D365 tests |
| `@pytest.mark.fourhands` | FourHands tests |
| `@pytest.mark.cart` | Shopping cart tests |
| `@pytest.mark.checkout` | Checkout tests |
| `@pytest.mark.slow` | Slow-running tests |

**Example:**
```python
@pytest.mark.smoke
@pytest.mark.fourhands
def test_homepage_loads(page: Page):
    """Quick smoke test for homepage"""
    pass
```

---

## 📁 Step 6: Project Structure

```
fourhands-qa-automation/
├── tests/                      # Test files
│   ├── d365/                   # D365 tests
│   │   └── test_d365_sales_order.py
│   └── fh/                     # FourHands tests
│       ├── test_fh_cart.py
│       ├── test_fh_checkout.py
│       └── test_fh_pdp.py
├── pages/                      # Page objects
│   ├── d365/
│   │   └── sales_order_page.py
│   ├── fh/
│   │   ├── fh_cart_page.py
│   │   ├── fh_checkout_page.py
│   │   └── fh_product_page.py
│   └── base_page.py           # Base page class
├── utils/                      # Utilities
│   ├── waits.py               # Wait strategies
│   ├── auth_helper.py         # Authentication
│   └── env.py                 # Environment config
├── configs/                    # Configurations
│   ├── playwright_config.py   # Playwright settings
│   └── browserstack_config.py # BrowserStack settings
├── scripts/                    # Helper scripts
│   ├── run_tests_local.sh
│   ├── run_tests_browserstack.sh
│   └── generate_allure_report.sh
├── docs/                       # Documentation
│   ├── AZURE_SETUP.md
│   ├── BROWSERSTACK_INTEGRATION.md
│   └── LOCAL_DEVELOPMENT.md
├── reports/                    # Test reports (gitignored)
│   ├── allure-results/
│   └── allure-report/
├── test-results/              # Screenshots, videos (gitignored)
├── storage_state/             # Auth sessions (gitignored)
├── .env                       # Environment variables (gitignored)
├── .env.example               # Environment template
├── conftest.py                # Pytest configuration
├── pytest.ini                 # Pytest settings
├── requirements.txt           # Python dependencies
├── browserstack.yml           # BrowserStack config
├── azure-pipelines.yml        # Main pipeline
├── azure-pipelines-pr.yml     # PR pipeline
└── azure-pipelines-browserstack.yml  # BrowserStack pipeline
```

---

## 🔄 Step 7: Git Workflow

### 7.1 Branch Strategy

```bash
# Create feature branch
git checkout -b feature/add-checkout-tests

# Make changes and commit
git add .
git commit -m "feat: Add checkout validation tests"

# Push to remote
git push origin feature/add-checkout-tests

# Create Pull Request in Azure DevOps
```

### 7.2 Commit Message Convention

```
<type>(<scope>): <subject>

Types:
- feat: New feature
- fix: Bug fix
- test: Add/update tests
- docs: Documentation
- refactor: Code refactoring
- chore: Maintenance

Examples:
- feat(cart): Add save-for-later functionality tests
- fix(d365): Resolve login timeout issue
- test(checkout): Add payment validation tests
- docs: Update setup guide with screenshots
```

---

## 🛠️ Step 8: Troubleshooting

### Common Issues

#### Issue 1: Import Errors

```bash
# Error: ModuleNotFoundError: No module named 'playwright'

# Solution: Activate virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue 2: Browser Not Installed

```bash
# Error: Executable doesn't exist at /path/to/browser

# Solution: Install browsers
playwright install chromium
```

#### Issue 3: Authentication Failures

```bash
# Error: Login failed / Timeout waiting for element

# Solution: Check credentials in .env file
# Recreate auth session:
pytest tests/setup/test_create_auth_session.py -v --headed
```

#### Issue 4: Slow Tests

```bash
# Optimize with parallel execution
pytest tests/ -n auto

# Or increase timeout
export TIMEOUT=60000
pytest tests/ -v
```

#### Issue 5: Port Already in Use (Allure)

```bash
# Error: Port 5000 already in use

# Solution: Kill process using port
lsof -ti:5000 | xargs kill -9

# Or use different port
allure open reports/allure-report --port 8080
```

---

## 📚 Step 9: Best Practices

### 9.1 Test Writing

✅ **Do:**
- Use descriptive test names
- Add docstrings to tests
- Use Allure steps for clarity
- Follow Page Object Model
- Keep tests independent
- Use proper assertions

❌ **Don't:**
- Hard-code test data
- Create test dependencies
- Use sleep() instead of waits
- Ignore flaky tests
- Skip error handling

### 9.2 Code Quality

```bash
# Format code with black
pip install black
black tests/ pages/ utils/

# Lint with flake8
pip install flake8
flake8 tests/ pages/ utils/

# Type checking with mypy
pip install mypy
mypy tests/ pages/ utils/
```

### 9.3 Performance

```bash
# Run smoke tests only during development
pytest tests/ -m smoke -v

# Use parallel execution for full runs
pytest tests/ -n auto -v

# Limit test discovery
pytest tests/fh/ -v  # Only FourHands tests
```

---

## ✅ Daily Development Workflow

```bash
# 1. Start your day
cd fourhands-qa-automation
source venv/bin/activate
git pull origin main

# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Write/update tests
# ... code your tests ...

# 4. Run tests locally
./scripts/run_tests_local.sh smoke

# 5. Check test results
./scripts/generate_allure_report.sh

# 6. Commit changes
git add .
git commit -m "feat: Add new test for X feature"

# 7. Push and create PR
git push origin feature/your-feature
# Create PR in Azure DevOps

# 8. Monitor PR pipeline
# Wait for PR validation to pass
```

---

## 📞 Support

- **Internal Wiki**: https://wiki.fourhands.com/qa
- **Slack Channel**: #qa-automation
- **Team Lead**: QA Manager
- **Playwright Docs**: https://playwright.dev
- **Pytest Docs**: https://docs.pytest.org

---

**Happy Testing! 🚀**
