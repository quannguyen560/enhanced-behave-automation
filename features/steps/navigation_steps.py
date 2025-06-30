"""
Navigation-specific step definitions
"""

from behave import given, when, then
from features.environment import get_element_utils, get_locators_for_page
from features.properties import TestProperties


@given("User is on the homepage")
def step_user_on_homepage(context):
    """
    Navigate to and verify user is on homepage
    """
    url = TestProperties.BASE_URL
    
    # Navigate to homepage
    if hasattr(context, 'chrome'):
        context.chrome.visit(url)
        print(f"Chrome navigated to homepage: {url}")
    
    if hasattr(context, 'firefox'):
        context.firefox.visit(url)
        print(f"Firefox navigated to homepage: {url}")
    
    # Verify we're on homepage
    browser = getattr(context, 'chrome', None) or getattr(context, 'firefox', None)
    if browser:
        current_url = browser.url
        assert current_url == url or current_url == f"{url}/", \
            f"Not on homepage. Current URL: {current_url}"
        print(f"Verified on homepage: {current_url}")
    else:
        assert False, "No browser available"


@when("User navigates to {page_name} page")
def step_navigate_to_page(context, page_name):
    """
    Navigate to a specific page
    
    Args:
        page_name: Name of the page to navigate to
    """
    # Map page names to URLs
    page_url_map = {
        'login': '/login',
        'dashboard': '/dashboard',
        'profile': '/profile',
        'settings': '/settings',
        'about': '/about',
        'contact': '/contact',
        'help': '/help',
        'transfer': '/transfer',
        'transactions': '/transactions'
    }
    
    endpoint = page_url_map.get(page_name.lower(), f'/{page_name.lower()}')
    url = TestProperties.get_url(endpoint)
    
    # Navigate to the page
    if hasattr(context, 'chrome'):
        context.chrome.visit(url)
        print(f"Chrome navigated to {page_name} page: {url}")
    
    if hasattr(context, 'firefox'):
        context.firefox.visit(url)
        print(f"Firefox navigated to {page_name} page: {url}")


@when("User clicks on {link_text} link")
def step_click_link(context, link_text):
    """
    Click on a link by its text
    
    Args:
        link_text: Text of the link to click
    """
    element_utils = get_element_utils(context, 'chrome') or get_element_utils(context, 'firefox')
    
    if element_utils:
        # Try to find and click the link
        link_locators = [
            ("link_text", link_text),
            ("partial_link_text", link_text),
            ("xpath", f"//a[contains(text(), '{link_text}')]"),
            ("css", f"a[href*='{link_text.lower()}']")
        ]
        
        success = element_utils.click_with_retry(link_locators)
        assert success, f"Failed to click link: {link_text}"
        print(f"Successfully clicked link: {link_text}")
    else:
        assert False, "No element utils available"


@when("User clicks on navigation menu")
def step_click_navigation_menu(context):
    """
    Click on the navigation menu (hamburger menu or main menu)
    """
    # Get locators for navigation menu
    locators = get_locators_for_page(context, 'common_elements', 'NAVIGATION_MENU')
    
    if not locators:
        # Fallback locators for common navigation patterns
        locators = [
            ("css", ".navbar-toggle"),
            ("css", ".menu-toggle"),
            ("css", ".hamburger"),
            ("xpath", "//button[contains(@class, 'navbar-toggle')]"),
            ("xpath", "//div[contains(@class, 'menu-icon')]"),
            ("id", "menu-toggle")
        ]
    
    element_utils = get_element_utils(context, 'chrome') or get_element_utils(context, 'firefox')
    
    if element_utils and locators:
        success = element_utils.click_with_retry(locators)
        assert success, "Failed to click navigation menu"
        print("Successfully clicked navigation menu")
    else:
        assert False, "No locators found for navigation menu"


@when("User goes back to previous page")
def step_go_back(context):
    """
    Navigate back to the previous page using browser back button
    """
    browser = getattr(context, 'chrome', None) or getattr(context, 'firefox', None)
    
    if browser:
        browser.back()
        print("Navigated back to previous page")
    else:
        assert False, "No browser available for navigation"


@when("User refreshes the page")
def step_refresh_page(context):
    """
    Refresh the current page
    """
    browser = getattr(context, 'chrome', None) or getattr(context, 'firefox', None)
    
    if browser:
        browser.reload()
        print("Page refreshed")
    else:
        assert False, "No browser available for refresh"


@then("User should be on {page_name} page")
def step_verify_on_page(context, page_name):
    """
    Verify user is on the specified page
    
    Args:
        page_name: Expected page name
    """
    browser = getattr(context, 'chrome', None) or getattr(context, 'firefox', None)
    
    if browser:
        current_url = browser.url.lower()
        page_name_lower = page_name.lower()
        
        assert page_name_lower in current_url, \
            f"Not on {page_name} page. Current URL: {current_url}"
        print(f"Verified on {page_name} page: {current_url}")
    else:
        assert False, "No browser available for verification"


@then("Navigation menu should be visible")
def step_verify_navigation_menu_visible(context):
    """
    Verify navigation menu is visible
    """
    locators = get_locators_for_page(context, 'common_elements', 'NAVIGATION_MENU')
    
    if not locators:
        locators = [
            ("css", ".navbar"),
            ("css", ".navigation"),
            ("css", ".main-menu"),
            ("xpath", "//nav"),
            ("id", "navigation")
        ]
    
    element_utils = get_element_utils(context, 'chrome') or get_element_utils(context, 'firefox')
    
    if element_utils and locators:
        is_visible = element_utils.verify_element_visible(locators)
        assert is_visible, "Navigation menu is not visible"
        print("Navigation menu is visible")
    else:
        assert False, "No locators found for navigation menu"


@then("Page should load successfully")
def step_verify_page_loaded(context):
    """
    Verify page has loaded successfully
    """
    browser = getattr(context, 'chrome', None) or getattr(context, 'firefox', None)
    
    if browser:
        # Check if page has a title
        title = browser.title
        assert title and len(title) > 0, "Page title is empty - page may not have loaded"
        
        # Check if page has content
        page_text = browser.html
        assert len(page_text) > 100, "Page content seems insufficient - page may not have loaded properly"
        
        print(f"Page loaded successfully. Title: {title}")
    else:
        assert False, "No browser available for verification"


@then("URL should contain {expected_text}")
def step_verify_url_contains(context, expected_text):
    """
    Verify current URL contains expected text
    
    Args:
        expected_text: Text that should be in the URL
    """
    browser = getattr(context, 'chrome', None) or getattr(context, 'firefox', None)
    
    if browser:
        current_url = browser.url.lower()
        expected_text_lower = expected_text.lower()
        
        assert expected_text_lower in current_url, \
            f"URL does not contain '{expected_text}'. Current URL: {current_url}"
        print(f"URL contains expected text '{expected_text}': {current_url}")
    else:
        assert False, "No browser available for URL verification"


@then("Breadcrumb should show {breadcrumb_path}")
def step_verify_breadcrumb(context, breadcrumb_path):
    """
    Verify breadcrumb navigation shows the expected path
    
    Args:
        breadcrumb_path: Expected breadcrumb path (e.g., "Home > Products > Details")
    """
    locators = get_locators_for_page(context, 'common_elements', 'BREADCRUMB')
    
    if not locators:
        locators = [
            ("css", ".breadcrumb"),
            ("css", ".breadcrumbs"),
            ("xpath", "//nav[@aria-label='breadcrumb']"),
            ("xpath", "//ol[contains(@class, 'breadcrumb')]"),
            ("css", "[aria-label='breadcrumb']")
        ]
    
    element_utils = get_element_utils(context, 'chrome') or get_element_utils(context, 'firefox')
    
    if element_utils and locators:
        breadcrumb_text = element_utils.get_text(locators)
        
        # Normalize the breadcrumb text for comparison
        normalized_breadcrumb = breadcrumb_text.replace('\n', ' ').replace('  ', ' ').strip()
        normalized_expected = breadcrumb_path.replace(' > ', ' ').replace('>', ' ')
        
        assert normalized_expected.lower() in normalized_breadcrumb.lower(), \
            f"Breadcrumb does not match. Expected: '{breadcrumb_path}', Found: '{normalized_breadcrumb}'"
        
        print(f"Breadcrumb verified: {normalized_breadcrumb}")
    else:
        assert False, "No locators found for breadcrumb"