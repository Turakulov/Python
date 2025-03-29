import argparse
import json
import os
import time

import pandas as pd
import selenium.webdriver as webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

parser = argparse.ArgumentParser(description='Federal statistics website parsing')
parser.add_argument('-j', type=str, help='Json categories file')
parser.add_argument('-u', type=str, help='Federal statistics website URL')
parser.add_argument('-t', type=int, help='''Type of webpage structure. # There are only three types:
# 1 - example "https://fedstat.ru/indicator/57890"
# 2 - example "https://fedstat.ru/indicator/57891"  -- in general almost all webpages look like this
# 3 - example "https://fedstat.ru/indicator/44176"
''')
parser.add_argument('-o', type=str, help='Output file name. Must include .xlsx format')


def get_json_categories(json_file_name: str) -> list:
    """
    Function for json file with oparsing categories upload
    :param json_file_name: Json file with categories
    :return: list with categories
    """
    file_object = open(json_file_name, "r")
    return json.loads(file_object.read())


def parse_website(type_page: int, query_link: str, category_list: list, years_dict: dict):
    """
    Function for Federal Statistics webpage parsing
    :param type_page: Type of webpage. See -h for desctiption
    :param query_link: URL of webpage
    :param category_list: list with categories
    :param years_dict: Years of analyze
    :return: list with content, list with content headers
    """
    heads = ['Год', 'OKATO']
    content = []
    errors = []
    counter = 0
    flag_head = False
    for cats in category_list:
        print(f"Обработка ОКАТО {str(cats)}")
        driver = webdriver.Chrome(executable_path=webdriver_path, chrome_options=chrome_options)
        driver.get(query_link)
        action = ActionChains(driver)
        time.sleep(1)
        years_element = driver.find_elements(By.XPATH, "//span[@class='k-icon k-filter']")
        time.sleep(2)
        if type_page == 1:
            years_element[0].click()
        elif type_page == 2:
            years_element[2].click()
        elif type_page == 3:
            years_element[0].click()

        try:
            driver.find_element(By.XPATH, ".//*[contains(text(), 'Выбрать все')]").click()
            time.sleep(1)
            driver.find_element(By.XPATH, ".//button[contains(text(), 'Фильтровать')]").click()
            time.sleep(1)
            driver.find_element(By.XPATH, ".//span[@class='icon-filters']").click()
            dropdown_menu = driver.find_elements(By.XPATH, ".//div[@class='dropdown_wrap']")[1]
            action.move_to_element(dropdown_menu).perform()
            time.sleep(1)
            region_dropdown = driver.find_element(By.XPATH,
                                                  ".//span[contains(text(), 'Классификатор объектов административно-территориального деления (ОКАТО)')]")
            action.move_to_element(region_dropdown).click(region_dropdown).perform()
            region = driver.find_elements(By.XPATH, f".//label[@class='lbl_checbox'][contains(text(), '{str(cats)}')]")
            time.sleep(1)
            for curr_reg in region:
                try:
                    action.move_to_element(curr_reg).click(curr_reg).perform()
                    time.sleep(2)
                    if type_page == 1:
                        tables = driver.find_elements(By.XPATH, ".//div[@class='k-grid-group-block']")
                        for i in range(len(tables)):
                            text_array = tables[i].text.split('\n')
                            for j in range(1, len(text_array)):
                                if 'ВСЕГО' in text_array[j]:
                                    content.append([int(text_array[0]), str(cats), 'ВСЕГО',
                                                    float(text_array[j + int(len(text_array[j:]) / 2)])])
                                    break
                                else:
                                    if i == 0 and counter == 0:
                                        heads.append(text_array[j])
                    elif type_page == 2:
                        years_value__dict = {
                            2015: None
                            , 2016: None
                            , 2017: None
                            , 2018: None
                            , 2019: None
                            , 2020: None
                            , 2021: None
                        }

                        html_current = driver.page_source
                        soup = BeautifulSoup(html_current, 'html5lib')
                        thead = soup.find('div', attrs={'class': 'k-grid-header-wrap'})
                        if not flag_head:
                            tr_tags = thead.find_all('tr')
                            for tr in tr_tags:
                                td_tags = tr.find_all('th')
                                heads = heads + [t.text for t in td_tags]
                            if heads != ['Год', 'OKATO', '2015', '2016', '2017', '2018', '2019', '2020', '2021']:
                                flag_head = False
                                heads = ['Год', 'OKATO']
                            else:
                                flag_head = True

                        tbody_content = soup.find_all('tbody')
                        for tr_content_i in range(len(tbody_content)):
                            tr_array = tbody_content[tr_content_i].find_all('tr')
                            for tr_array_i in range(len(tr_array)):
                                td_tags = tr_array[tr_array_i].find_all('td')
                                td_tags_array = [t.text for t in td_tags]
                                if 'ВСЕГО' in td_tags_array:
                                    data_raw = tbody_content[tr_content_i + 1].find_all('tr')[0]
                                    data_array = list(map(float, [t.text for t in data_raw.find_all('td')]))
                                    data_indexes = list(
                                        map(int, [item['data-col'][-1] for item in data_raw.find_all('td')]))
                                    for v_i in range(len(data_indexes)):
                                        years_value__dict[years_dict[data_indexes[v_i]]] = data_array[v_i]

                                    data_array = [y for _, y in years_value__dict.items()]
                                    data_array.insert(0, cats)
                                    data_array.insert(0, '')
                                    content.append(data_array)
                                    break
                    elif type_page == 3:
                        tables = driver.find_elements(By.XPATH, ".//div[@class='k-grid-group-block']")
                        for i in range(len(tables)):
                            text_array = tables[i].text.split('\n')
                            for j in range(1, len(text_array)):
                                if 'значение показателя за год' in text_array[j]:
                                    content.append([int(text_array[0]), str(cats), float(text_array[-1].split(' ')[0])])
                                    break

                    print("Выполнена обработка ОКАТО: ", cats)
                except Exception:
                    er = f"Возможно при загрузке ОКАТО {str(cats)} возникла ошибка. Проверьте данные!"
                    errors.append(er)
                    pass
        except Exception as external_error:
            er2 = f"Критическая ошибка! При загрузке ОКАТО {str(cats)} возникла ошибка:" + str(external_error)
            errors.append(er2)
            print(er2)
            time.sleep(1)
        driver.quit()
        counter += 1
        time.sleep(1)
    print(errors)
    return content, heads


def save_file(output_filename: str, type_page: int, content: list, heads: list) -> None:
    if type_page == 1:
        df = pd.DataFrame(content, columns=heads)
        df = df.pivot_table('значение показателя за год', ['OKATO'], 'Год')
        with pd.ExcelWriter(output_filename, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name="Sheet", index=True)
    elif type_page == 2:
        df = pd.DataFrame(content, columns=heads)
        with pd.ExcelWriter(output_filename, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name="Sheet", index=True)
    elif type_page == 3:
        heads = ['Год', 'OKATO', 'значение показателя за год']
        df = pd.DataFrame(content, columns=heads)
        df = df.pivot_table('значение показателя за год', ['OKATO'], 'Год')
        with pd.ExcelWriter(output_filename, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name="Sheet", index=True)
    print("Файл сохранен!")


if __name__ == "__main__":
    # How to run:
    # python Fedstat_parsing.py -j 'category_list.json' -u 'https://fedstat.ru/indicator/57891' -t 2 -o 'output_file.xlsx'
    args = parser.parse_args()
    CONST_type = args.t
    CONST_query_link = args.u
    CONST_json_file_name = args.j
    CONST_output_filename = args.o

    # working paths
    working_dir = os.getcwd()
    webdriver_path = os.path.join(working_dir, "chromedriver")  # proper version https://chromedriver.chromium.org/

    ua = UserAgent()  # Create a fake header to make requests look human
    # webdriver
    chrome_options = Options()
    chrome_options.add_argument(str(ua.chrome))
    # 'webdriver' executable needs to be in PATH. Please see
    # https://sites.google.com/a/chromium.org/chromedriver/home
    os.environ["webdriver.chrome.driver"] = webdriver_path

    _years_dict = {
        0: 2015
        , 1: 2016
        , 2: 2017
        , 3: 2018
        , 4: 2019
        , 5: 2020
        , 6: 2021
    }
    _category_list = get_json_categories(CONST_json_file_name)
    _content, _heads = parse_website(CONST_type, CONST_query_link, _category_list, _years_dict)
    save_file(CONST_output_filename, CONST_type, _content, _heads)
    print('Shutting down!')
