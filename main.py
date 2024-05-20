import asyncio
from playwright.async_api import async_playwright
from playwright.async_api import Page
import time
from bs4 import BeautifulSoup
import pandas as pd


async def reject_cookies(page:Page ): 
    reject_cookies_button = await page.wait_for_selector('//button[@id="cc-b-custom"]')
    await reject_cookies_button.click()

async def scrape_address_of_school(page:Page):
    address_data_div = await page.wait_for_selector("//div[@class='contact-info__item']")
    inner_html_str =  await address_data_div.inner_html()
    data_content = BeautifulSoup(inner_html_str, features="lxml")
    data_content.find_all("p")
    text_parts = data_content.contents[0].get_text().split("\n")
    address, postal = text_parts[-2].strip(), text_parts[-1].strip()
    return address, postal

async def get_links(page:Page):
    await page.goto("https://innovitaskolan.se/")
    await page.wait_for_load_state()
    await reject_cookies(page=page)
    link_div = await page.wait_for_selector('//div[@class="location-module-six_v1__card-columns"]')
    data_content = BeautifulSoup(await link_div.inner_html(), features="lxml")
    return [l['href'] for l in data_content.find_all("a")]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # set headless=True to run in headless mode
        page = await browser.new_page()
        links = await get_links(page=page)
        collected = []
        for url in links:
            while True:
                try:
                    print(f"scraping {url}")
                    await page.goto(url=url)
                    await page.wait_for_load_state()
                    address, postal = await scrape_address_of_school(page=page)
                    collected.append({"address": address, "postal_information":postal})
                    break
                except Exception as e:
                    print(f"url: {url} failed with {e}")
        df = pd.DataFrame(collected)
        df.to_excel("scraped_data.xlsx")
        time.sleep(3)
        await browser.close()


asyncio.run(main())
