from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Navigate to the home page and take a screenshot
    page.goto("http://127.0.0.1:5000/")
    page.screenshot(path="jules-scratch/verification/home.png")

    # Navigate to the leaderboard page and take a screenshot
    page.goto("http://127.0.0.1:5000/leaderboard")
    page.screenshot(path="jules-scratch/verification/leaderboard.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
