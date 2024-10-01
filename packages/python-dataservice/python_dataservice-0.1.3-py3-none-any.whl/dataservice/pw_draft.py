import asyncio
from playwright.async_api import async_playwright, Playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.on("request", lambda request: print(">>", request.method, request.url))
        page.on("response", lambda response: print("<<", response.status, response.url))
        response = await page.goto("https://finance.yahoo.com")
        print(await page.title())
        await browser.close()


asyncio.run(main())