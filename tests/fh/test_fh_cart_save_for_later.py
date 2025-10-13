"""
FourHands Cart - Save for Later Tests

Migrated from Selenium: Cart_SaveProductLater_TS_T1075.java
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.fh_home_page import FourHandsHomePage
from pages.fh_product_detail_page import FourHandsProductDetailPage
from pages.fh_cart_page import FourHandsCartPage
from pages.fh_top_navigation_page import FourHandsTopNavigationPage


pytestmark = [pytest.mark.fourhands, pytest.mark.cart]


@pytest.fixture
def fh_cart_page(fh_authenticated_page: Page):
    """Provide FourHands cart page with clean state."""
    page = fh_authenticated_page
    nav = FourHandsTopNavigationPage(page)
    cart = FourHandsCartPage(page)
    
    # Clean cart before test
    with allure.step("Cleanup: Clear cart and saved items"):
        if nav.cart_bucket_check() == "cart":
            nav.click_cart_bucket()
            cart.remove_all_products()
            cart.remove_all_saved_for_later()
            nav.click_dismiss_cart_banner()
    
    yield page


@allure.feature("Cart")
@allure.story("Save for Later")
@allure.title("TS-T1075: Verify Save for Later")
@pytest.mark.smoke
@pytest.mark.e2e
def test_cart_save_for_later(fh_cart_page: Page, fh_test_product: str):
    """
    Test: Verify product can be saved for later from cart.
    
    Steps:
        1. Add product to cart
        2. Navigate to cart
        3. Click 'Save for Later' on product
        4. Verify product moved to 'Saved for Later' section
    
    Expected:
        - Product removed from cart
        - Product appears in 'Saved for Later'
        - Cart count decreases
        - Saved for Later count increases
    
    Migrated from: Cart_SaveProductLater_TS_T1075.java
    """
    page = fh_cart_page
    nav = FourHandsTopNavigationPage(page)
    pdp = FourHandsProductDetailPage(page)
    cart = FourHandsCartPage(page)
    
    with allure.step(f"Navigate to product: {fh_test_product}"):
        pdp.navigate_to_product(fh_test_product)
    
    with allure.step("Add product to cart"):
        nav.click_add_to_cart_button()
        nav.click_dismiss_cart_banner()
    
    with allure.step("Navigate to cart"):
        nav.click_cart_bucket()
    
    with allure.step("Click 'Save for Later' on product"):
        cart.click_save_for_later_from_cart()
    
    with allure.step("Verify product moved to 'Saved for Later' section"):
        assert cart.verify_one_item_moved_to_saved_for_later(), \
            "Product was not moved to Saved for Later section"
    
    with allure.step("Cleanup: Remove saved items"):
        cart.remove_all_saved_for_later()


@allure.feature("Cart")
@allure.story("Save for Later")
@allure.title("TS-T1077: Move Saved Item Back to Cart")
@pytest.mark.smoke
def test_cart_move_saved_item_to_cart(fh_cart_page: Page, fh_test_product: str):
    """
    Test: Verify saved item can be moved back to cart.
    
    Steps:
        1. Add product to cart
        2. Save product for later
        3. Click 'Move to Cart' from Saved for Later section
        4. Verify product moved back to cart
    
    Expected:
        - Product removed from Saved for Later
        - Product appears in cart
        - Cart count increases
    
    Migrated from: Cart_SaveProductLater_MovetoCart_TS_T1077.java
    """
    page = fh_cart_page
    nav = FourHandsTopNavigationPage(page)
    pdp = FourHandsProductDetailPage(page)
    cart = FourHandsCartPage(page)
    
    with allure.step(f"Setup: Add product {fh_test_product} to cart"):
        pdp.navigate_to_product(fh_test_product)
        nav.click_add_to_cart_button()
        nav.click_dismiss_cart_banner()
        nav.click_cart_bucket()
    
    with allure.step("Save product for later"):
        cart.click_save_for_later_from_cart()
        assert cart.verify_one_item_moved_to_saved_for_later(), \
            "Product was not saved"
    
    with allure.step("Move saved product back to cart"):
        cart.click_move_to_cart_from_saved()
    
    with allure.step("Verify product is back in cart"):
        assert cart.verify_product_in_cart(fh_test_product), \
            "Product was not moved back to cart"
    
    with allure.step("Cleanup"):
        cart.remove_all_products()


@allure.feature("Cart")
@allure.story("Save for Later")
@allure.title("TS-T1078: Move All Saved Items to Cart")
@pytest.mark.e2e
def test_cart_move_all_saved_to_cart(fh_cart_page: Page):
    """
    Test: Verify all saved items can be moved to cart at once.
    
    Steps:
        1. Add multiple products to cart
        2. Save all products for later
        3. Click 'Move All to Cart'
        4. Verify all products moved back to cart
    
    Expected:
        - All products removed from Saved for Later
        - All products appear in cart
        - Saved for Later section is empty
    
    Migrated from: Cart_SaveProductLater_MoveAlltoCart_TS_T1078.java
    """
    page = fh_cart_page
    nav = FourHandsTopNavigationPage(page)
    pdp = FourHandsProductDetailPage(page)
    cart = FourHandsCartPage(page)
    
    test_products = ["108422-001", "108422-002"]  # Multiple products
    
    with allure.step(f"Setup: Add {len(test_products)} products and save them"):
        for product in test_products:
            pdp.navigate_to_product(product)
            nav.click_add_to_cart_button()
            nav.click_dismiss_cart_banner()
        
        nav.click_cart_bucket()
        
        # Save all products
        for _ in test_products:
            cart.click_save_for_later_from_cart()
    
    with allure.step("Verify all products are in Saved for Later"):
        saved_count = cart.get_saved_for_later_count()
        assert saved_count == len(test_products), \
            f"Expected {len(test_products)} saved items, found {saved_count}"
    
    with allure.step("Click 'Move All to Cart'"):
        cart.click_move_all_to_cart()
    
    with allure.step("Verify all products moved to cart"):
        cart_count = cart.get_cart_item_count()
        assert cart_count == len(test_products), \
            f"Expected {len(test_products)} items in cart, found {cart_count}"
        
        saved_count = cart.get_saved_for_later_count()
        assert saved_count == 0, \
            f"Expected 0 saved items, found {saved_count}"
    
    with allure.step("Cleanup"):
        cart.remove_all_products()


@allure.feature("Cart")
@allure.story("Save for Later")
@allure.title("TS-T1076: Verify Empty Saved for Later Section")
@pytest.mark.smoke
def test_cart_saved_for_later_empty_state(fh_cart_page: Page):
    """
    Test: Verify empty state message when no saved items.
    
    Steps:
        1. Navigate to cart with no saved items
        2. Verify empty state message displays
    
    Expected:
        - "No saved items" message or similar displays
        - Saved for Later section indicates it's empty
    
    Migrated from: Cart_SavedforLater_Empty_TS_T1076.java
    """
    page = fh_cart_page
    nav = FourHandsTopNavigationPage(page)
    cart = FourHandsCartPage(page)
    
    with allure.step("Navigate to cart"):
        nav.click_cart_bucket()
    
    with allure.step("Verify Saved for Later section is empty"):
        assert cart.verify_saved_for_later_empty(), \
            "Saved for Later section should show empty state"
        
        saved_count = cart.get_saved_for_later_count()
        assert saved_count == 0, \
            f"Expected 0 saved items, found {saved_count}"
