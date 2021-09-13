from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

from ForSaleData import *


class SteamBot:

    def __init__(self):
        self.username = username
        self.password = password
        binary_path = r'C:\Users\MSI_GF75\Sam_voiceAssistant\venv\lib\site-packages\chromedriver_py\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=binary_path)

    def close_browser(self) -> None:
        self.driver.close()
        self.driver.quit()

    def xpath_exists(self, xpath) -> bool:
        try:
            self.driver.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False

        return exist

    def log_into_steam(self) -> None:
        driver = self.driver
        driver.get(steam_link)
        driver.maximize_window()
        driver.implicitly_wait(5)

        if (driver.find_elements_by_xpath("//*[@id='account_pulldown']") != None):
            driver.find_element_by_class_name('global_action_link').click()
            sleep(2)

            driver.find_element_by_name('username').send_keys(username)
            sleep(1)

            driver.find_element_by_name('password').send_keys(password)
            sleep(1)

            driver.find_element_by_css_selector("button[type=submit]").click()
            # driver.find_element_by_xpath('//button[@type="submit"]').click()
            sleep(2)

            self.type_steam_guard_code()

    def type_steam_guard_code(self) -> None:
        if self.xpath_exists("//input[@id='twofactorcode_entry']"):
            code = input("Type your Steam Guard code: ")
            self.driver.find_element_by_xpath("//input[@id='twofactorcode_entry']").send_keys(code)
            sleep(1)
            self.driver.find_element_by_css_selector("div[type=submit]").click()
            sleep(3)
        else:
            sleep(3)

    def enter_inventory(self) -> None:
        driver = self.driver

        driver.find_elements_by_xpath("//*[@id='account_pulldown']").submit()
        #driver.implicitly_wait(5)

        driver.find_element_by_xpath(
            "//*[@id='account_dropdown']/div/a[1]"
        ).click()
        sleep(3)

    def set_active_game(self) -> None:
        self.driver.find_element_by_xpath(f'//*[text()="{game}"]').click()
        sleep(1)
        self.driver.refresh()
        sleep(1)

    def get_number_of_items(self) -> int:
        number_of_items = self.driver.find_element_by_xpath(
            f'//span[text()="{game}"]/following-sibling::span').text.strip('()')

        return int(number_of_items)

    def set_checkbox_marketable_items(self) -> None:
        self.driver.find_element_by_id('filter_tag_show').click()
        self.driver.implicitly_wait(5)

        self.driver.find_element_by_css_selector("input[tag_name=marketable]").click()
        sleep(1)

    def get_number_of_marketable_items(self) -> int:
        number_of_marketable_items = self.driver.find_element_by_xpath(
            "//label[text()='Можно продать']/child::span"
        ).text.strip('()')

        return int(number_of_marketable_items)

    def select_item(self, number_of_item: int) -> None:
        items_list = self.driver.find_elements_by_class_name('inventory_item_link')
        items_list[number_of_item].click()
        sleep(5)

    def get_item_name(self) -> str:
        name_list = self.driver.find_elements_by_class_name('hover_item_name')

        if name_list[0].is_displayed():
            name = name_list[0].text
        else:
            name = name_list[1].text
        self.driver.implicitly_wait(5)

        return name

    def get_item_price(self) -> float:
        price_list = self.driver.find_elements_by_xpath("//div[@style='min-height: 3em; margin-left: 1em;']")

        if price_list[0].is_displayed():
            price = price_list[0].text.replace(',', '.').split()[1]
        else:
            price = price_list[1].text.replace(',', '.').split()[1]
        self.driver.implicitly_wait(5)

        return float(price)

    def sell_all_items(self):
        count = 0
        number_of_items = self.get_number_of_items()
        number_of_marketable_items = self.get_number_of_marketable_items()
        print(f'{number_of_items} items in {game}\n{number_of_marketable_items} items to sell\n')
        for item in range(number_of_items):
            try:
                self.select_item(item)
                count += 1

                if self.xpath_exists("//*[contains(text(),'Сейчас этот предмет никто не продаёт.')]"):
                    continue

                name = self.get_item_name()
                price = self.get_item_price()
                print(f'{count} - {name}: {price}\n')

                if ((count + 1) % 25 == 0) and (count != 0):
                    self.driver.find_element_by_id('pagebtn_next').click()
                    sleep(1)
            except ElementNotInteractableException:
                continue


bot = SteamBot()

if __name__ == "__main__":
    bot.log_into_steam()
    bot.enter_inventory()
    bot.set_active_game()
    bot.set_checkbox_marketable_items()
    bot.sell_all_items()