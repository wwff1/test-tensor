import time
from pages.sbis_page import SbisPage
from pages.sbis_page import partners_not_are_equal, check_download_file


def test_size_image(driver):
    sbis_page = SbisPage(driver)
    sbis_page.open_page("https://sbis.ru/")
    time.sleep(1)
    sbis_page.click_menu_contacts()
    time.sleep(1)
    sbis_page.click_tensor_logo()
    time.sleep(1)
    sbis_page.click_read_more_button()
    time.sleep(1)
    assert sbis_page.check_work_image_chronology(), "Фотографии хронологии имеют разный размер"
    time.sleep(2)


def test_region(driver):
    sbis_test = SbisPage(driver)
    sbis_test.open_page("https://sbis.ru/")
    time.sleep(1)
    sbis_test.click_menu_contacts()
    time.sleep(1)
    sbis_test.check_selected_region("Тюменская обл.")
    time.sleep(1)
    default_list = sbis_test.get_list_partners()
    sbis_test.click_selected_region()
    time.sleep(1)
    sbis_test.change_region("41 Камчатский край")
    time.sleep(1)
    sbis_test.check_selected_region("Камчатский край")
    time.sleep(1)
    change_list = sbis_test.get_list_partners()
    sbis_test.check_title("Камчатский край")
    time.sleep(1)
    sbis_test.check_url("41-kamchatskij-kraj")
    assert partners_not_are_equal(default_list, change_list), "Список партнеров не изменился"
    time.sleep(2)


def test_download_file(driver):
    sbis_test = SbisPage(driver)
    sbis_test.open_page("https://sbis.ru/")
    time.sleep(1)
    sbis_test.click_download_button()
    time.sleep(1)
    sbis_test.click_menu_download()
    time.sleep(1)
    plugin_file_size = sbis_test.get_plugin_file_size()
    sbis_test.click_download_plugin_file()
    time.sleep(3)
    assert check_download_file("sbisplugin-setup-web.exe", plugin_file_size), \
        "Размер скачанного файла не совпадает с указанныйм на сайте"
    time.sleep(2)
