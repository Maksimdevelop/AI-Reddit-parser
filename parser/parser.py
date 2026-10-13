from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent

class Parser:
    def __init__(self):
        self.pw = None
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=True)
        self.context = self.browser.new_context(
            user_agent=UserAgent(browsers=['chrome'], os=['windows', 'macos']).random,
            viewport={"width":1920, "height":1080}
        )
        self.page = self.context.new_page()
        return self

    def close(self):
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.pw:
            self.pw.stop()
            
    def __exit__(self, exc_type, exc, tb):
        self.close()