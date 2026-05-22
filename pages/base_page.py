import allure
from playwright.sync_api import Page


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def fill_field(self, locator: str, text: str):
        self.page.locator(locator).fill(text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str):
        self.page.locator(locator).click()

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: str) -> str:
        return self.page.locator(locator).inner_text()

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_for_url(self, url: str):
        self.page.wait_for_url(url)
        assert self.page.url == url, f"Ожидался редирект на {url}, текущий url: {self.page.url}"

    @allure.step("Создание скриншота и прикрепление к Allure отчёту")
    def make_screenshot(self):
        screenshot = self.page.screenshot(full_page=True)
        allure.attach(screenshot, name="Screenshot", attachment_type=allure.attachment_type.PNG)


class BasePage(PageAction):
    """
    Базовый класс для всех страниц.
    Наследуется от PageAction и предоставляет общие локаторы и методы, которые доступны на всех страницах сайта.
    Служит промежуточным слоем между PageAction и конкретными страницами. При необходимости тестирования общих
    элементов (хедер, футер, навигация и т.п.) они добавляются сюда.
    """

    def __init__(self, page: Page):
        super().__init__(page)
