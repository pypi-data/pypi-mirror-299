import asyncio
import re
from pprint import pprint

from mypy.plugins.default import partial
from playwright.async_api import async_playwright, Playwright

intercepted_requests = []
counter = 0


def get_request(request):
    global intercepted_requests
    global counter
    # print("<<", request.url)
    if "v1.0.0/conversation/realtime/read" in request.url:
        counter += 1
        print(f"intercepted {counter} request(s)")
        intercepted_requests.append(request)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.on("request", get_request)
        # page.on("response", lambda response: print("response", response.url))
        await page.goto("https://www.dailymail.co.uk/news/article-13907993/giovanni-pernice-strictly-bullying-probe-difficult-year-cleared-abuse-allegations.html")
        await page.get_by_role("button", name="Accept").click()
        await page.get_by_role("link", name=re.compile('\d+(\.\d+)?[kM]? View comments')).click()
        await page.get_by_text("Show More Comments").scroll_into_view_if_needed()
        await page.get_by_text("Show More Comments").click()
        await page.get_by_text("Show More Comments").scroll_into_view_if_needed()
        await page.get_by_text("Show More Comments").click()
        await page.get_by_text("Show More Comments").scroll_into_view_if_needed()
        await page.get_by_text("Show More Comments").click()
        if intercepted_requests:
            for request in intercepted_requests:
                print(">>", request.url)
                response = await request.response()
                print(await response.json())
        # print(await page.title())
        # if intercepted_request:
        #     int_response = await intercepted_request.response()
        #     print("int response", int_response.url)
        #     print(await int_response.json())
        # await browser.close()
        # await page.goto("https://www.dailymail.co.uk/news/article-13907993/giovanni-pernice-strictly-bullying-probe-difficult-year-cleared-abuse-allegations.html")
        # async with page.expect_response("**/v1.0.0/conversation/realtime/read") as response_info:
        #     response = await response_info.value
        #     a = await response.json()
        #     print(a)
        #     await page.get_by_role("button", name="Accept").click()
        #     await page.get_by_role("link", name=re.compile('\d+(\.\d+)?[kM]? View comments')).click()
        #     await page.get_by_text("Show More Comments").scroll_into_view_if_needed()
        #     await page.get_by_text("Show More Comments").click()
        #     await page.get_by_text("Show More Comments").scroll_into_view_if_needed()
        #     await page.get_by_text("Show More Comments").click()
        #     await page.get_by_text("Show More Comments").scroll_into_view_if_needed()
        #     await page.get_by_text("Show More Comments").click()






asyncio.run(main())