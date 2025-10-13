"""
FourHands Product Detail Page (PDP) tests.
Converted from Selenium/Java tests.

Usage:
    pytest tests/fh/test_fh_pdp.py -m fourhands
    pytest tests/fh/test_fh_pdp.py -k "add_product" --headed
"""
import pytest
import os
from playwright.sync_api import Page
from dotenv import load_dotenv

from pages.fh_home_page import FourHandsHomePage
from pages.fh_login_page import FourHandsLoginPage
from pages.fh_product_detail_page import FourHandsProductDetailPage
from pages.fh_cart_page import FourHandsCartPage
from pages.fh_top_navigation_page import FourHandsTopNavigationPage


load_dotenv()


@pytest.fixture
def fh_authenticated_page(page: Page):
    """Provide authenticated FourHands page."""
    from pathlib import Path
    storage_path = Path("storage_state/fh_session.json")
    
    if not storage_path.exists():
        pytest.skip("FourHands storage state not found. Run: pytest tests/fh/test_fh_auth.py -k 'record' -s --headed")
    
    return page


@pytest.fixture
def fh_base_url():
    """Get FourHands base URL from environment."""
    base_url = os.getenv("FH_BASE_URL")
    if not base_url:
        pytest.skip("FH_BASE_URL not configured in .env")
    return base_url


@pytest.fixture
def fh_test_product():
    """Get test product ID from environment."""
    product_id = os.getenv("FH_ONE_ITEM", "108422-001")
    return product_id


@pytest.mark.fourhands
@pytest.mark.e2e
def test_pdp_add_product_to_cart(fh_authenticated_page: Page, fh_base_url: str, fh_test_product: str):
    """
    TS-T1070: PDP > Add to Cart > Single Product
    
    Converted from: PDP_AddProductToCart_TS_T1070.java
    
    Steps:
    1. Log into FH site (using storage state)
    2. Search for a product and go to PDP
    3. Click Add to Cart button
    4. Verify cart reflects the product
    5. Clean up - remove product from cart
    """
    page = fh_authenticated_page
    
    # Initialize page objects
    home_page = FourHandsHomePage(page)
    pdp = FourHandsProductDetailPage(page)
    cart_page = FourHandsCartPage(page)
    nav = FourHandsTopNavigationPage(page)
    
    # Navigate to home
    home_page.navigate_to_home(fh_base_url)
    
    # Clean cart first
    nav.click_cart_bucket()
    if not cart_page.is_cart_empty():
        cart_page.click_remove_all_products()
    
    # Search for product
    nav.click_search_icon()
    nav.enter_search_item(fh_test_product)
    
    # Click on product to go to PDP
    home_page.click_searched_item(fh_test_product)
    
    # Verify PDP loaded
    pdp.assert_loaded()
    
    # Verify initial quantity is 1
    initial_quantity = pdp.get_quantity()
    assert initial_quantity == 1, f"Expected quantity 1, got {initial_quantity}"
    
    # Add to cart
    nav.click_add_to_cart_button()
    page.wait_for_timeout(2000)
    
    # Dismiss cart banner if present
    nav.click_dismiss_cart_banner()
    
    # Verify cart count
    cart_count = nav.get_cart_bucket_text()
    assert cart_count == "1", f"Expected cart count 1, got {cart_count}"
    
    # Go to cart and verify product
    nav.click_cart_bucket()
    assert cart_page.is_product_in_cart(fh_test_product), \
        f"Product {fh_test_product} not found in cart"
    
    # Cleanup - remove product
    cart_page.click_remove_all_products()
    
    print(f"\n✓ Test passed: Product {fh_test_product} successfully added to cart and removed")


@pytest.mark.fourhands
@pytest.mark.e2e
def test_pdp_increment_product_quantity(fh_authenticated_page: Page, fh_base_url: str, fh_test_product: str):
    """
    TS-T1071: PDP > Increment Product Quantity
    
    Converted from: PDP_IncrementProduct_TS_T1071.java
    
    Steps:
    1. Navigate to PDP
    2. Click increment button multiple times
    3. Verify quantity increases correctly
    4. Add to cart and verify cart count
    """
    page = fh_authenticated_page
    
    # Initialize page objects
    home_page = FourHandsHomePage(page)
    pdp = FourHandsProductDetailPage(page)
    cart_page = FourHandsCartPage(page)
    nav = FourHandsTopNavigationPage(page)
    
    # Navigate and search
    home_page.navigate_to_home(fh_base_url)
    nav.click_search_icon()
    nav.enter_search_item(fh_test_product)
    home_page.click_searched_item(fh_test_product)
    
    # Increment quantity 3 times
    num_increments = 3
    pdp.click_increment_button(num_increments)
    
    # Verify quantity
    expected_quantity = 1 + num_increments  # Initial is 1
    actual_quantity = pdp.get_quantity()
    assert actual_quantity == expected_quantity, \
        f"Expected quantity {expected_quantity}, got {actual_quantity}"
    
    # Add to cart
    nav.click_add_to_cart_button()
    page.wait_for_timeout(2000)
    nav.click_dismiss_cart_banner()
    
    # Verify cart count
    cart_count = nav.get_cart_bucket_text()
    assert cart_count == str(expected_quantity), \
        f"Expected cart count {expected_quantity}, got {cart_count}"
    
    # Cleanup
    nav.click_cart_bucket()
    cart_page.click_remove_all_products()
    
    print(f"\n✓ Test passed: Quantity incremented to {expected_quantity}")


@pytest.mark.fourhands
@pytest.mark.smoke
def test_pdp_add_to_cart_button_visible(fh_authenticated_page: Page, fh_base_url: str, fh_test_product: str):
    """
    Quick smoke test to verify Add to Cart button is visible on PDP.
    """
    page = fh_authenticated_page
    
    home_page = FourHandsHomePage(page)
    pdp = FourHandsProductDetailPage(page)
    nav = FourHandsTopNavigationPage(page)
    
    # Navigate to PDP
    home_page.navigate_to_home(fh_base_url)
    nav.click_search_icon()
    nav.enter_search_item(fh_test_product)
    home_page.click_searched_item(fh_test_product)
    
    # Verify PDP elements
    pdp.assert_loaded()
    assert pdp.is_add_to_cart_enabled(), "Add to Cart button is not enabled"
    
    product_title = pdp.get_product_title()
    assert product_title, "Product title is empty"
    
    print(f"\n✓ PDP smoke test passed for product: {product_title}")


@pytest.mark.fourhands
@pytest.mark.e2e
@pytest.mark.slow
def test_pdp_availability_messaging(fh_authenticated_page: Page, fh_base_url: str):
    """
    TS-T1434/T1435: PDP > Availability ATP Messaging
    
    Converted from: PDP_AvailabilityATPMessaging tests
    
    Verify ATP (Available to Promise) messaging appears correctly.
    """
    page = fh_authenticated_page
    
    home_page = FourHandsHomePage(page)
    pdp = FourHandsProductDetailPage(page)
    nav = FourHandsTopNavigationPage(page)
    
    # Use ATP messaging user's product (from properties)
    test_product = os.getenv("FH_ONE_ITEM", "108422-001")
    
    # Navigate to PDP
    home_page.navigate_to_home(fh_base_url)
    nav.click_search_icon()
    nav.enter_search_item(test_product)
    home_page.click_searched_item(test_product)
    
    # Get availability message
    availability_msg = pdp.get_availability_message()
    
    # Verify some availability messaging exists
    assert availability_msg and availability_msg != "N/A", \
        "No availability messaging found on PDP"
    
    print(f"\n✓ Availability message found: {availability_msg}")
