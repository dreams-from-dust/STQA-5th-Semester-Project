import pytest
from playwright.sync_api import Page, expect

def test_toolshop_automation(page: Page):
    # 1. Open the website
    page.goto("https://practicesoftwaretesting.com/", wait_until="networkidle")

    # 2. UI TEST: Hover over Sign In
    signin_link = page.get_by_role("link", name="Sign in")
    signin_link.hover()
    page.wait_for_timeout(1000)

    # 3. UI TEST: Hover over Home
    page.get_by_role("link", name="Home").hover()
    
    # 4. Navigate to Login Page
    signin_link.click()

    # 5. NEGATIVE TEST: Invalid Login
    page.get_by_placeholder("Email").fill("wrong@test.com")
    page.get_by_placeholder("Password").fill("wrongpass")
    page.get_by_role("button", name="Login").click()
    expect(page.locator(".alert-danger")).to_be_visible() 
    
    # 6. POSITIVE TEST: Successful Login
    page.get_by_placeholder("Email").clear()
    page.get_by_placeholder("Email").fill("customer@practicesoftwaretesting.com")
    page.get_by_placeholder("Password").clear()
    page.get_by_placeholder("Password").fill("welcome01")
    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/account") 

    # 7. FUNCTIONAL: Search for a Product
    page.get_by_role("link", name="Home").click()
    search_bar = page.get_by_placeholder("Search")
    search_bar.fill("Hammer")
    page.keyboard.press("Enter")
    page.wait_for_timeout(2000) 

    # 8. VERIFY: Search Results
    hammer_card = page.locator(".card").filter(has_text="Hammer").first
    expect(hammer_card).to_be_visible()

    # 9. FUNCTIONAL: Add Item to Cart
    hammer_card.click()
    page.wait_for_load_state("networkidle")
    
    # Click Add to Cart
    add_btn = page.get_by_role("button", name="Add to cart")
    add_btn.wait_for(state="visible")
    add_btn.click()
    
    # 10. VERIFY: Cart Updated
    cart_icon = page.locator(".badge, #cart-quantity, [data-test='cart-quantity']").first
    expect(cart_icon).to_contain_text("1", timeout=15000)
    
    print("\n--- ALL 10 TESTS PASSED SUCCESSFULLY ---")
