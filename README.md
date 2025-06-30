# Enhanced Multi-Language Test Automation Framework

## Overview

This enhanced test automation framework provides comprehensive multi-language support for web application testing using Behave with Gherkin syntax. It includes robust element utilities, language management, locator loading, and fallback mechanisms to ensure reliable testing across different languages and locales.

## 🚀 Key Features

### ✅ Multi-Language Support
- **English and Vietnamese** with automatic fallback mechanisms
- **Dynamic language switching** during test execution
- **Language validation** and completeness checking
- **Bulk text operations** for better performance

### ✅ Enhanced Element Utilities
- **Robust element interactions** with retry mechanisms
- **Multi-locator strategy** support (ID, XPath, CSS, etc.)
- **JavaScript fallback** execution for complex interactions
- **Advanced form handling** (input, dropdown, checkbox, etc.)
- **Element visibility** and state verification

### ✅ BDD with Gherkin Syntax
- **Clean, readable scenarios** using Gherkin
- **Reusable step definitions** for common actions
- **Scenario outlines** for data-driven testing
- **Tag-based execution** for test organization

### ✅ Multi-Browser Support
- **Chrome and Firefox** support with parallel execution
- **Headless mode** for CI/CD integration
- **Browser-specific configurations** and optimizations
- **Cross-browser compatibility** testing

### ✅ Comprehensive Reporting
- **Allure reports** with rich visualizations
- **HTML reports** with detailed step information
- **Screenshot capture** on test failures
- **JUnit XML** for CI/CD integration

## 📋 Repository Structure

```
enhanced-behave-automation/
├── features/
│   ├── __init__.py
│   ├── environment.py           # Behave hooks and setup
│   ├── properties.py           # Test configuration
│   ├── demo.feature            # Main feature tests
│   ├── login.feature           # Login specific tests
│   └── steps/
│       ├── __init__.py
│       ├── common_steps.py     # Common step definitions
│       ├── login_steps.py      # Login step definitions
│       └── navigation_steps.py # Navigation step definitions
├── utils/
│   ├── __init__.py
│   ├── element_utils.py        # Enhanced element utilities
│   ├── language_manager.py     # Multi-language support
│   └── locator_loader.py       # Dynamic locator loading
├── locators/
│   ├── english/
│   │   ├── __init__.py
│   │   ├── common_elements.py
│   │   ├── login_page.py
│   │   └── transfer_page.py
│   └── vietnamese/
│       ├── __init__.py
│       ├── common_elements.py
│       ├── login_page.py
│       └── transfer_page.py
├── expectations/
│   └── languages/
│       ├── __init__.py
│       ├── english.py
│       └── vietnamese.py
├── examples/
│   └── demo_usage_examples.py
├── reports/
│   └── screenshots/
├── pyproject.toml              # Dependencies
├── behave.ini                  # Behave configuration
├── requirements.txt            # Alternative dependency file
├── .gitignore
├── README.md
└── TEST_EXECUTION_GUIDE.md
```

## 🛠️ Installation

### Prerequisites
- Python 3.12 or higher
- Chrome or Firefox browser
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/quannguyen560/enhanced-behave-automation.git
cd enhanced-behave-automation

# Install dependencies (using poetry)
poetry install

# Or using pip
pip install -r requirements.txt

# Install browser drivers (automatic via webdriver-manager)
# Drivers will be downloaded automatically on first run
```

### Environment Configuration
Create a `.env` file in the root directory:
```env
EMAIL=test@example.com
PASSWORD=testpassword123
BASE_URL=https://your-app.com
HEADLESS=false
BROWSER_TIMEOUT=30
```

## 🚀 Usage Examples

### Basic Test Execution
```bash
# Run all tests
behave

# Run with specific browser
behave -D browser=chrome

# Run with specific language
behave -D language=vietnamese

# Run specific tags
behave --tags=@smoke
behave --tags=@multilang
behave --tags=@login

# Run in headless mode
behave -D headless=true
```

### Advanced Execution
```bash
# With Allure reporting
behave -f allure_behave.formatter:AllureFormatter -o allure-results

# Generate Allure report
allure serve allure-results

# With HTML reporting
behave -f html -o reports/html_report.html

# Run specific feature
behave features/login.feature

# Run with multiple formats
behave -f pretty -f json -o reports/results.json
```

### Multi-Language Testing
```bash
# Test in English (default)
behave --tags=@multilang

# Test in Vietnamese
behave -D language=vietnamese --tags=@multilang

# Cross-language validation
behave --tags=@cross-language
```

## 📝 Writing Tests

### Feature File Example
```gherkin
@fixture.chrome
Feature: Login Functionality

  @smoke @login
  Scenario: Successful login with valid credentials
    Given User is on the login page
    When User enters username "testuser@example.com"
    And User enters password "ValidPassword123"
    And User clicks login button
    Then User should be redirected to dashboard
    And User should see welcome message

  @multilang @login
  Scenario Outline: Multi-language login validation
    Given The test is configured for <language> language
    And User is on the login page
    When User clicks the login button without entering credentials
    Then User should see <error_type> validation message

    Examples:
      | language   | error_type |
      | english    | required   |
      | vietnamese | required   |
```

### Step Definition Example
```python
from behave import given, when, then
from features.environment import get_element_utils, get_locators_for_page

@given("User is on the login page")
def step_user_on_login_page(context):
    element_utils = get_element_utils(context, 'chrome')
    element_utils.navigate_to_page('/login')

@when('User enters username "{username}"')
def step_enter_username(context, username):
    locators = get_locators_for_page(context, 'login_page', 'USERNAME_FIELD')
    element_utils = get_element_utils(context, 'chrome')
    element_utils.input_text(locators, username)

@then("User should see welcome message")
def step_verify_welcome_message(context):
    element_utils = get_element_utils(context, 'chrome')
    success = element_utils.verify_message('welcome')
    assert success, "Welcome message not found"
```

## 🔧 Framework Architecture

### Core Components

1. **ElementUtils** (`utils/element_utils.py`)
   - Enhanced element interactions with retry mechanisms
   - Multi-language text support
   - JavaScript execution fallbacks
   - Comprehensive element state verification

2. **LanguageManager** (`utils/language_manager.py`)
   - Dynamic language switching
   - Automatic fallback mechanisms
   - Language validation and completeness checking
   - Bulk text operations

3. **LocatorLoader** (`utils/locator_loader.py`)
   - Language-specific locator loading
   - Multi-strategy locator support
   - Automatic fallback to other languages
   - Locator validation and caching

4. **Environment Setup** (`features/environment.py`)
   - Browser fixture management
   - Language configuration
   - Test lifecycle hooks
   - Enhanced reporting and screenshots

### Language Support

The framework supports multiple languages with automatic fallback:

```python
# Language switching
language_manager.set_language('vi')  # Switch to Vietnamese
locator_loader.set_language('vietnamese')

# Automatic fallback
element_utils.click_button_by_any_language_text('login')

# Temporary language switching
with language_manager.switch_language_temporarily('vi'):
    vietnamese_text = language_manager.get_message('welcome')
```

### Locator Management

Locators are organized by language and page:

```python
# English locators (locators/english/login_page.py)
class LoginPageLocators:
    USERNAME_FIELD = [
        ("id", "username"),
        ("name", "email"),
        ("css", "input[type='email']")
    ]
    
    LOGIN_BUTTON = [
        ("id", "login-btn"),
        ("xpath", "//button[contains(text(), 'Login')]"),
        ("css", ".login-button")
    ]

# Vietnamese locators (locators/vietnamese/login_page.py)
class LoginPageLocators:
    LOGIN_BUTTON = [
        ("xpath", "//button[contains(text(), 'Đăng nhập')]"),
        ("xpath", "//button[contains(text(), 'Login')]"),  # Fallback
        ("css", ".login-button")
    ]
```

## 🧪 Testing Best Practices

### 1. Multi-Language Test Design
```python
def test_login_multi_language():
    for lang in ['en', 'vi']:
        language_manager.set_language(lang)
        locator_loader.set_language('english' if lang == 'en' else 'vietnamese')
        
        # Test logic remains the same
        element_utils.click_button_by_text('login')
        assert element_utils.verify_message('login_success')
```

### 2. Robust Element Interactions
```python
# Use multiple locator strategies
locators = [
    ("id", "login-btn"),
    ("xpath", "//button[contains(text(), 'Login')]"),
    ("css", ".login-button"),
    ("xpath", "//button[contains(text(), 'Đăng nhập')]")  # Vietnamese fallback
]

success = element_utils.click_with_retry(locators)
```

### 3. Error Handling
```python
try:
    element_utils.click_button_by_text('login')
except Exception as e:
    logger.error(f"Login failed: {e}")
    # Try fallback approach
    element_utils.click_button_by_any_language_text('login')
```

## 📊 Reporting and Monitoring

### Allure Reports
Generate rich, interactive reports with:
- Test execution timeline
- Step-by-step details
- Screenshots on failures
- Language and browser information
- Trend analysis

### HTML Reports
Simple HTML reports with:
- Test results summary
- Failed step details
- Screenshots embedded
- Execution logs

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Run Behave Tests
  run: |
    behave -f allure_behave.formatter:AllureFormatter -o allure-results
    
- name: Generate Allure Report
  run: allure generate allure-results --clean
  
- name: Upload Test Results
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: allure-report/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

### Adding New Languages
1. Create language file in `expectations/languages/`
2. Add locator files in `locators/{language}/`
3. Update language mapping in `LanguageManager`
4. Add test scenarios for the new language

### Adding New Pages
1. Create locator files for each supported language
2. Add page-specific step definitions
3. Create feature files for the new page
4. Update documentation

## 📚 Advanced Features

### Parallel Execution
```bash
# Install behave-parallel
pip install behave-parallel

# Run tests in parallel
behave --processes 4
```

### Custom Formatters
```python
# Custom formatter example
class CustomFormatter(Formatter):
    def feature(self, feature):
        # Custom feature formatting
        pass
```

### Environment-specific Configuration
```python
# config/environments.py
ENVIRONMENTS = {
    'dev': {
        'BASE_URL': 'https://dev.example.com',
        'TIMEOUT': 10
    },
    'staging': {
        'BASE_URL': 'https://staging.example.com',
        'TIMEOUT': 15
    },
    'prod': {
        'BASE_URL': 'https://example.com',
        'TIMEOUT': 30
    }
}
```

## 📈 Performance Optimizations

- **Locator Caching**: Loaded locators are cached for better performance
- **Bulk Operations**: Get multiple texts in single operation
- **Lazy Loading**: Locators loaded only when needed
- **Smart Fallbacks**: Efficient fallback mechanisms
- **Connection Pooling**: Reuse browser instances where possible

## 🔒 Security Considerations

- **Credential Management**: Use environment variables for sensitive data
- **Screenshot Sanitization**: Avoid capturing sensitive information
- **Test Data Isolation**: Use isolated test environments
- **Access Control**: Implement proper access controls for test environments

## 📝 License

This framework is designed for educational and testing purposes. Please ensure compliance with your organization's policies when using in production environments.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information
4. Include logs and screenshots when possible

---

**Happy Testing! 🚀**