# QA Playwright Automation Framework

Automated testing framework for D365 Finance & Operations and FourHands e-commerce platform.

## 🚀 Features

- **Playwright Python** - Modern browser automation
- **BrowserStack Integration** - Cloud testing on real devices
- **D365 F&O Testing** - Sales orders, workflows, navigation
- **FourHands E-commerce** - Cart, checkout, product pages
- **GitHub Actions** - CI/CD ready
- **Allure Reports** - Beautiful test reports

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- BrowserStack account

## 🛠️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/zkyko/QA-playwright-automation.git
cd QA-playwright-automation
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Set up environment variables

Create a `.env` file:

```bash
# D365 Configuration
D365_BASE_URL=https://fourhands-test.sandbox.operations.dynamics.com
D365_USERNAME=your_username
D365_PASSWORD=your_password

# BrowserStack Configuration  
BROWSERSTACK_USERNAME=your_bs_username
BROWSERSTACK_ACCESS_KEY=your_bs_key

# Test Configuration
HEADED=false
TIMEOUT=30000
```

## 🧪 Running Tests

### Local Execution

```bash
# Run all tests
pytest tests/ -v

# Run smoke tests only
pytest tests/ -m smoke -v

# Run D365 tests
pytest tests/d365/ -v

# Run with visible browser
pytest tests/ -v --headed
```

### BrowserStack Cloud

```bash
# Install BrowserStack SDK
npm install -g browserstack-sdk

# Run on BrowserStack
browserstack-sdk pytest tests/d365/ -v
```

## 🎯 Test Structure

```
tests/
├── d365/                          # D365 F&O tests
│   ├── test_d365_auth.py         # Authentication
│   ├── test_d365_sales_order.py  # Sales orders
│   └── conftest.py               # D365 fixtures
├── fh/                            # FourHands tests
│   ├── test_fh_cart.py           # Shopping cart
│   ├── test_fh_checkout.py       # Checkout flow
│   └── test_fh_pdp.py            # Product pages
└── conftest.py                    # Global fixtures

pages/
├── d365/                          # D365 page objects
│   ├── sales_order_page.py
│   └── login_page.py
└── fh/                            # FourHands page objects
    ├── cart_page.py
    └── checkout_page.py
```

## 🔄 GitHub Actions

Tests can be triggered via GitHub Actions:

1. Go to **Actions** tab
2. Select workflow:
   - **Smoke Tests** - Quick validation
   - **BrowserStack Tests** - Full regression
3. Click **Run workflow**

### Scheduled Runs

Tests automatically run:
- **Daily at 2 AM UTC** (main regression suite)
- Manually on-demand

## 📊 Test Reports

### Allure Reports

```bash
# Generate report
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

### BrowserStack Dashboard

View test recordings and logs:
https://automate.browserstack.com/dashboard

## 🔐 Authentication

### Local Testing
- First run saves session cookies to `storage_state/`
- Subsequent runs reuse cookies (fast!)

### BrowserStack
- Uses programmatic login
- No manual authentication needed

## 🏷️ Test Markers

```bash
# Smoke tests (quick)
pytest -m smoke

# E2E tests (comprehensive)
pytest -m e2e

# D365 specific
pytest -m d365

# FourHands specific  
pytest -m fourhands
```

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Run tests locally
4. Submit pull request

## 📝 License

Proprietary - FourHands Internal Use Only

## 📞 Support

- **Team**: QA Automation
- **Contact**: [Your Email]
