"""
Enhanced Behave environment setup with multi-language support
"""
import os
import subprocess
import tempfile
from datetime import datetime
from typing import Optional

import allure
from behave import fixture, use_fixture
from faker import Faker
from pydantic_settings import BaseSettings
from selenium.webdriver import ChromeOptions, FirefoxOptions, FirefoxProfile
from selenium.webdriver.chrome.service import Service
from splinter import Browser
from splinter.driver.webdriver import BaseWebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.element_utils import ElementUtils
from utils.language_manager import LanguageManager
from utils.locator_loader import LocatorLoader


class Settings(BaseSettings):
    EMAIL: str = ""
    PASSWORD: str = ""
    BASE_URL: str = "https://google.com"
    HEADLESS: bool = False
    BROWSER_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Global tracking for language features
LANGUAGE_FEATURES_TRACKING_FILE = os.path.join(
    tempfile.gettempdir(), "behave_language_features.flag"
)


def set_language_features_used():
    """Mark that language features have been used"""
    try:
        with open(LANGUAGE_FEATURES_TRACKING_FILE, 'w') as f:
            f.write("True")
    except Exception:
        pass


def check_language_features_used():
    """Check if language features have been used"""
    try:
        if os.path.exists(LANGUAGE_FEATURES_TRACKING_FILE):
            with open(LANGUAGE_FEATURES_TRACKING_FILE, 'r') as f:
                return f.read().strip() == "True"
    except Exception:
        pass
    return False


def cleanup_language_features_tracking():
    """Clean up tracking file"""
    try:
        if os.path.exists(LANGUAGE_FEATURES_TRACKING_FILE):
            os.remove(LANGUAGE_FEATURES_TRACKING_FILE)
    except Exception:
        pass


@fixture
def chrome(context, **kwargs):
    """Setup Chrome browser with enhanced options"""
    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )
    
    if settings.HEADLESS:
        chrome_options.add_argument('--headless')
    
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(executable_path=ChromeDriverManager().install())
    
    chrome: BaseWebDriver = Browser(
        "chrome", service=service, options=chrome_options, **kwargs
    )
    chrome.wait_time = settings.BROWSER_TIMEOUT
    context.chrome = chrome
    yield context.chrome
    context.chrome.quit()


@fixture
def firefox(context, **kwargs):
    """Setup Firefox browser with enhanced options"""
    firefox_options = FirefoxOptions()
    firefox_profile = FirefoxProfile()

    # Set Firefox preferences
    firefox_profile.set_preference("dom.webnotifications.enabled", False)
    firefox_profile.set_preference("dom.push.enabled", False)
    firefox_profile.set_preference("signon.rememberSignons", False)
    firefox_profile.set_preference("signon.passwordEditCapture.enabled", False)
    firefox_profile.set_preference("dom.webdriver.enabled", False)
    firefox_profile.set_preference("useAutomationExtension", False)
    firefox_profile.set_preference("marionette.enabled", False)

    firefox_options.profile = firefox_profile

    if settings.HEADLESS:
        firefox_options.add_argument('--headless')
    
    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")
    firefox_options.add_argument("--disable-gpu")

    service = Service(executable_path=GeckoDriverManager().install())

    firefox: BaseWebDriver = Browser(
        "firefox", service=service, options=firefox_options, **kwargs
    )
    firefox.wait_time = settings.BROWSER_TIMEOUT
    context.firefox = firefox
    yield context.firefox
    context.firefox.quit()


def before_tag(context, tag):
    """Setup fixtures based on tags"""
    if tag == "fixture.chrome":
        use_fixture(chrome, context)
    if tag == "fixture.firefox":
        use_fixture(firefox, context)


def before_all(context):
    """Initialize the enhanced multi-language framework"""
    cleanup_language_features_tracking()
    
    # Setup screenshot directory
    current_dir = os.getcwd()
    path = f"{current_dir}/reports/screenshots"
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except OSError:
            print(f"Cannot create the folder: {path}")
    context.screenshot_dir = path
    context.fake = Faker()

    # Get language configuration
    language = context.config.userdata.get('language', 'english')
    context.current_language = language
    
    # Language mapping
    language_code_mapping = {
        'english': 'en',
        'vietnamese': 'vi',
        'en': 'en',
        'vi': 'vi'
    }
    language_code = language_code_mapping.get(language.lower(), 'en')
    
    # Initialize components
    context.language_manager = LanguageManager(default_language=language_code)
    context.locator_loader = LocatorLoader(default_language=language)
    context.scenarios_with_language_tags = set()
    
    print(f"Framework initialized:")
    print(f"  - Language: {language} (code: {language_code})")
    print(f"  - Base URL: {settings.BASE_URL}")
    print(f"  - Headless: {settings.HEADLESS}")


def before_scenario(context, scenario):
    """Setup for each scenario"""
    # Setup element utils for available browsers
    if hasattr(context, 'firefox'):
        context.firefox_utils = ElementUtils(
            context.firefox.driver, 
            context.language_manager
        )

    if hasattr(context, 'chrome'):
        context.chrome_utils = ElementUtils(
            context.chrome.driver, 
            context.language_manager
        )

    # Handle language tags
    language_related_tags = []
    for tag in scenario.tags:
        if tag.startswith('language.') or tag in ['multilang', 'cross-language', 'language-switching']:
            language_related_tags.append(tag)
    
    if language_related_tags:
        context.scenarios_with_language_tags.update(language_related_tags)
        set_language_features_used()

    # Set scenario-specific language
    for tag in scenario.tags:
        if tag.startswith('language.'):
            scenario_language = tag.replace('language.', '')
            context.language_manager.set_language(scenario_language)
            context.locator_loader.set_language(scenario_language)
            set_language_features_used()
            break


def after_scenario(context, scenario):
    """Cleanup after scenario"""
    if hasattr(context, 'language_manager'):
        default_language = context.config.userdata.get('language', 'english')
        language_code_mapping = {
            'english': 'en',
            'vietnamese': 'vi',
            'en': 'en',
            'vi': 'vi'
        }
        default_code = language_code_mapping.get(default_language.lower(), 'en')
        context.language_manager.set_language(default_code)
        context.locator_loader.set_language(default_language)


def after_all(context):
    """Final cleanup and reporting"""
    if "allure" in context.config.format:
        subprocess.run(["allure", "generate", "allure-results"])
    
    language_features_used = check_language_features_used()
    
    if hasattr(context, 'language_manager'):
        print("\n=== Language Framework Summary ===")
        print(f"Default language: {context.current_language}")
        print(f"Supported languages: {context.language_manager.get_supported_languages()}")
        
        if language_features_used:
            print(f"Language features used: {getattr(context, 'scenarios_with_language_tags', set())}")
            
            validation_result = context.language_manager.validate_language_completeness('en')
            has_missing_translations = False
            
            for lang, categories in validation_result.items():
                if any(missing_keys for missing_keys in categories.values() if missing_keys):
                    has_missing_translations = True
                    break
            
            if has_missing_translations:
                print("Warning: Missing translations found")
            else:
                print("✅ All languages have complete translations!")
        else:
            print("ℹ️  No language features used in this run")
    
    cleanup_language_features_tracking()


def after_step(context, step):
    """Enhanced step cleanup with screenshots"""
    if step.status == "failed":
        browsers = ['chrome', 'firefox']

        for browser in browsers:
            if f"fixture.{browser}" in context.tags and hasattr(context, browser):
                try:
                    browser_driver = getattr(context, browser).driver
                    
                    # Allure screenshot
                    if "allure" in context.config.format:
                        try:
                            current_lang = getattr(context, 'language_manager', None)
                            lang_suffix = f"_{current_lang.current_language}" if current_lang else ""
                            
                            allure.attach(
                                browser_driver.get_screenshot_as_png(),
                                name=f"screenshot_{browser}{lang_suffix}",
                                attachment_type=allure.attachment_type.PNG,
                            )
                        except Exception as e:
                            print(f"Failed Allure screenshot for {browser}: {e}")

                    # Local screenshot
                    try:
                        suffix = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
                        current_lang = getattr(context, 'language_manager', None)
                        lang_suffix = f"_{current_lang.current_language}" if current_lang else ""

                        screenshot_name = f'screenshot_{browser}{lang_suffix}_{suffix}.png'
                        screenshot_path = f'{context.screenshot_dir}/{screenshot_name}'
                        browser_driver.save_screenshot(screenshot_path)
                        print(f"Screenshot saved: {screenshot_path}")
                    except Exception as e:
                        print(f"Failed local screenshot for {browser}: {e}")

                except Exception as e:
                    print(f"Screenshot error for {browser}: {e}")


# Utility functions for step files
def get_element_utils(context, browser_name='chrome') -> Optional[ElementUtils]:
    """Get ElementUtils for specified browser"""
    utils_attr = f"{browser_name}_utils"
    return getattr(context, utils_attr, None)


def get_locators_for_page(context, page_name, locator_name=None):
    """Get locators for page"""
    if not hasattr(context, 'locator_loader'):
        return []
        
    if locator_name:
        return context.locator_loader.get_locators(page_name, locator_name)
    else:
        return context.locator_loader.load_locators(page_name)


def switch_language_for_test(context, language_code):
    """Switch language during test"""
    if hasattr(context, 'language_manager'):
        context.language_manager.set_language(language_code)
        
        locator_language_mapping = {
            'en': 'english',
            'english': 'english',
            'vi': 'vietnamese',
            'vietnamese': 'vietnamese'
        }
        locator_language = locator_language_mapping.get(language_code.lower(), 'english')
        context.locator_loader.set_language(locator_language)
        set_language_features_used()


def get_text_in_current_language(context, text_key, category='messages'):
    """Get text in current language"""
    if hasattr(context, 'language_manager'):
        set_language_features_used()
        return context.language_manager.get_text_by_category(category, text_key)
    else:
        return f"[Missing: {text_key}]"
