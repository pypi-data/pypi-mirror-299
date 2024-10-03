import asyncio
from appium import webdriver
from selenium.webdriver.common.by import By  # 使用 Selenium 的 By 类
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from log78 import Logger78
from appium.options.common import AppiumOptions  # 修改这一行

class Appium78:
    def __init__(self, device_name, app_package, app_activity, appium_url="http://127.0.0.1:4723", options=None):
        self.device_name = device_name
        self.appium_url = appium_url
        self.app_package = app_package
        self.app_activity = app_activity
        self.options = options
        self.driver = None
        self.logger = Logger78.instance()

    async def initialize_driver(self):
        await self.logger.DETAIL(f"正在初始化驱动程序")
        await self.logger.DETAIL(f"self.options 类型: {type(self.options)}")
        await self.logger.DETAIL(f"self.options 内容: {self.options}")
        await self.logger.DETAIL(f"Appium URL: {self.appium_url}")
        try:
            # 使用 options 参数而不是 desired_capabilities
            self.driver = webdriver.Remote(command_executor=self.appium_url, desired_capabilities =self.options)
            await self.logger.DETAIL("驱动程序初始化成功")
            await self.logger.DETAIL(f"驱动程序会话ID: {self.driver.session_id}")
        except Exception as e:
            await self.logger.ERROR(f"初始化驱动程序时出错：{str(e)}")
            await self.logger.ERROR(f"错误类型: {type(e).__name__}")
            raise

    async def perform_swipe_down(self):
        if not self.driver:
            raise Exception("Driver not initialized")

        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.7)
        end_y = int(size['height'] * 0.3)

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        await asyncio.sleep(2)

    def find_elements(self, by, value):
        if not self.driver:
            return []
        return self.driver.find_elements(by, value)

    def click_element(self, element):
        element.click()

    def get_page_source(self):
        return self.driver.page_source if self.driver else ""

    def quit(self):
        if self.driver:
            self.driver.quit()

    def get_element_dom_by_xpath(self, xpath):
        if not self.driver:
            return ""
        element = self.driver.find_element(By.XPATH, xpath)  # 使用 By.XPATH
        return element.get_attribute("outerHTML") if element else ""