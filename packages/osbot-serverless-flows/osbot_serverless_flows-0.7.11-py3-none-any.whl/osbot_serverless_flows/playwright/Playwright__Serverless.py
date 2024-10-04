from osbot_playwright.playwright.api.Playwright_CLI import Playwright_CLI
from osbot_utils.utils.Threads import async_invoke_in_new_loop
from playwright.async_api import async_playwright, Playwright

from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.base_classes.Type_Safe             import Type_Safe

class Playwright__Serverless(Type_Safe):
    playwright_cli : Playwright_CLI


    @cache_on_self
    def chrome_path(self):
        return self.playwright_cli.executable_path__chrome()

    def playwright(self) -> Playwright:
        async_target = async_playwright().start()
        return async_invoke_in_new_loop(async_target)

    def browser(self):
        async_target = self.playwright().chromium.launch(**self.browser__launch_kwargs())
        return async_invoke_in_new_loop(async_target)

    def browser__launch_kwargs(self):
        return dict(args            = ["--disable-gpu", "--single-process"],
                    executable_path = self.chrome_path()                   )

    # context = await async_playwright().start()

    #             browser = await context.chromium.launch(**launch_kwargs)
    #             page    = await browser.new_page()
    #             await page.goto                 (url)
    #
    #             screenshot = await page.screenshot(full_page=True)
    #             return bytes_to_base64(screenshot)