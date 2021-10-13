import os
import pandas as pd
from selenium.webdriver.chrome.options import Options
import selenium.webdriver as webdriver
import time

from email.message import EmailMessage
import smtplib
from conf import query, num_page, sender, password, receiver

query_link = f"https://www.researchgate.net/search/publication?q={query}&page="

# working paths
working_dir = os.getcwd()
folder_for_pdf = os.path.join(working_dir, "articles")
webdriver_path = os.path.join(working_dir, "chromedriver")   # proper version https://chromedriver.chromium.org/

# check if articles directory is exist and create if not
if not os.path.isdir(folder_for_pdf):
    os.mkdir(folder_for_pdf)

# webdriver
chrome_options = Options()
prefs = {"download.default_directory": folder_for_pdf, "download.prompt_for_download": False}
chrome_options.add_experimental_option('prefs', prefs)
os.environ["webdriver.chrome.driver"] = webdriver_path   # 'webdriver' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home

links_list = [query_link + str(page) for page in range(1, num_page)]   # create links to follow

driver = webdriver.Chrome(executable_path=webdriver_path, chrome_options=chrome_options)

final_info = []   # empty dictionary for articles info

for search_link in links_list:
    # get all links to articles from the page
    driver.get(search_link)
    time.sleep(5)
    articles = driver.find_elements_by_class_name("nova-legacy-o-stack__item")
    
    articles_links = []
    for article in articles:
        try:
            link = article.find_element_by_css_selector("a.nova-legacy-e-link.nova-legacy-e-link--color-inherit.nova-legacy-e-link--theme-bare").get_attribute("href")
            articles_links.append(link)
        except:
            pass
        
    for link in articles_links:
        # get info of each article 
        driver.get(link)
        text = driver.find_element_by_class_name("research-detail-header-section__ie11").text
        
        try:
            desc = driver.find_element_by_xpath("//div[@class='nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-800 research-detail-middle-section__abstract']").text
        except:
            desc = ''
            
        try:
            citations = driver.find_element_by_xpath("//h2[@class='nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit']").text
        except:
            citations = ''   

        # trying to download the article's doc
        try:
            initial_dir = os.listdir(folder_for_pdf)
            driver.find_element_by_xpath("//*[@class='nova-legacy-c-button nova-legacy-c-button--align-center nova-legacy-c-button--radius-m nova-legacy-c-button--size-m nova-legacy-c-button--color-blue nova-legacy-c-button--theme-solid nova-legacy-c-button--width-full js-target-download-btn-5c4ac089a6fdccd6b5c6f690 js-lite-click']").click()
            time.sleep(5)
            current_dir = os.listdir(folder_for_pdf)
            filename = list(set(current_dir) - set(initial_dir))[0]
            full_path = os.path.join(folder_for_pdf, filename)
        except Exception as e:
            full_path = None
        
        tmp_info = {}
        tmp_info.update({
                        'title': text.split("\n")[0],
                        'source' : link,
                        'authors': text.split("Authors:")[-1].replace("\n","; "),
                        'description': desc,
                        'citations': citations.split("Citations (")[-1].replace(")",""),
                        'path_to_file': full_path
                        })

        final_info.append(tmp_info.copy())
        time.sleep(2)

driver.quit()

# write all info to excel
df = pd.DataFrame(final_info)
excel_path = os.path.join(working_dir, "data.xlsx")
df.to_excel(excel_path, index=False)


# create email

mail = EmailMessage()
mail['From'] = sender
mail['To'] = receiver
mail['Subject'] = "Results of query: " + query
mail.set_content("Hello!\n\nI've found some information for you")

# add article attachment
with open(excel_path, 'rb') as f:
    file_data = f.read()
    file_name = f'data.xlsx'
mail.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

# send email
server = smtplib.SMTP('smtp.office365.com')  
server.starttls()  
server.login(sender, password)    
server.send_message(mail)      
server.quit()    
