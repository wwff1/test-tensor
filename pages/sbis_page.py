from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os.path
import re


BYTE_TO_MEGABYTE_DIVIDER = 1048576


class SbisPage:

    def __init__(self, driver):
        self.driver = driver
        self.menu_contacts = (By.CLASS_NAME, "sbisru-Header__menu-item-1")
        self.tensor_logo = (By.CLASS_NAME, "sbisru-Contacts__logo-tensor")
        self.block_people_power = (By.XPATH, "//p[text()='Сила в людях']/..")
        self.read_more_button = (By.XPATH, "//a[@href='/about']")
        self.work_image_chronology = (By.CLASS_NAME, "tensor_ru-About__block3-image-wrapper")
        self.selected_region = (By.CLASS_NAME, "sbis_ru-Region-Chooser__text")
        self.list_partners = (By.XPATH, "//div[@id='city-id-2']/ancestor::div[@name='itemsContainer']")
        self.footer = (By.CSS_SELECTOR, "#container > div.sbisru-Footer.sbisru-Footer__scheme--default")
        self.download_button = (By.XPATH, "//a[@href='/download?tab=ereport&innerTab=ereport25']/.")
        self.menu_download = (By.XPATH, "//div[@name='TabButtons']/div[2]")
        self.download_plugin_file = (
            By.XPATH, "//a[@href='https://update.sbis.ru/Sbis3Plugin/master/win32/sbisplugin-setup-web.exe']/."
        )

    def open_page(self, url):
        """ Открытие страницы """

        self.driver.get(url)

    def click_menu_contacts(self):
        """ Клик по разделу "Контакты" """

        self.driver.find_element(*self.menu_contacts).click()

    def click_tensor_logo(self):
        """ Клик по баннеру "Тензор" """

        self.driver.find_element(*self.tensor_logo).click()

    def click_read_more_button(self):
        """ Клик по "Подробнее" в блоке "Сила в людях" """

        self.driver.switch_to.window(self.driver.window_handles[1])
        people_power_parent = self.driver.find_element(*self.block_people_power)
        read_more_button = people_power_parent.find_element(*self.read_more_button)
        read_more_button.click()

    def check_work_image_chronology(self) -> bool:
        """ Проверка размера фотографий хронологии """

        images = self.driver.find_elements(*self.work_image_chronology)
        return sizes_are_equal([image.size for image in images])

    def check_selected_region(self, name_region):
        """ Проверка  выбранного региона """

        default_region = self.driver.find_element(*self.selected_region).text
        assert default_region == name_region, "Выбран не тот регион"

    def click_selected_region(self):
        """ Клик по выбранному региону """

        self.driver.find_element(*self.selected_region).click()

    def change_region(self, name_region):
        """ Изменение выбранного региона """

        self.driver.find_element(By.XPATH, f"//li/span[text()='{name_region}']").click()

    def get_list_partners(self):
        """ Получение списока партнеров """

        list_partners = self.driver.find_element(*self.list_partners)
        assert list_partners.text, "Список партнеров пуст"
        return list_partners.text

    def check_title(self, name_title):
        """ Проверка тайтла страницы """

        assert re.search(rf'{name_title}', rf'{self.driver.title}'), \
            "Нет названия региона в title страницы"

    def check_url(self, name_url):
        """ Проверка ссылки страницы """

        assert re.search(rf'{name_url}', rf'{self.driver.current_url}'), \
            "Нет названия региона в url страницы"

    def click_download_button(self):
        """ Клик по "Скачать СБИС" """

        footer = self.driver.find_element(*self.footer)
        ActionChains(self.driver).scroll_to_element(footer).perform()
        self.driver.find_element(*self.download_button).click()

    def click_menu_download(self):
        """ Клик по "СБИС Плагин" """

        self.driver.find_element(*self.menu_download).click()

    def click_download_plugin_file(self):
        """ Клик по "Скачать" """

        self.driver.find_element(*self.download_plugin_file).click()

    def get_plugin_file_size(self):
        """ Клик по "Скачать" """

        plugin_file = self.driver.find_element(*self.download_plugin_file).text
        size = re.search(r'(\d+\.\d+)', rf'{plugin_file}')
        return float(size.group(0))


def sizes_are_equal(size_list):
    """ Проверка высоты и ширины фотографий хронологии """

    heights = {size['height'] for size in size_list}
    widths = {size['width'] for size in size_list}
    return len(heights) == 1 and len(widths) == 1


def partners_not_are_equal(default_list_partners, change_list_partners):
    """ Проверка изменения списка партнеров """

    return default_list_partners != change_list_partners


def check_download_file(file_name, file_size):
    """ Проверка загруженного файла """

    file_path = os.path.expanduser(fr"~/Downloads/{file_name}")

    if not os.path.isfile(file_path):
        return False

    download_file_size = os.stat(file_path).st_size
    if round(download_file_size / BYTE_TO_MEGABYTE_DIVIDER, 2) == file_size:
        return True

    return False
