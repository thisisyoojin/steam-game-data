import time
from selenium import webdriver
from utils import read_config

def get_current_urls(driver:webdriver, last_id:int) -> int:
    """
    The function to read urls in
    """
    if last_id:
        xpath = f"//a[@data-ds-appid='{last_id}']//following-sibling::a[contains(@class, 'search_result_row')]"
    else:
        xpath = "//a[contains(@class, 'search_result_row')]"
  
    item_id = None
    items = driver.find_elements_by_xpath(xpath)

    for item in items:
        item_id = item.get_attribute('data-ds-appid')
        with open(f'data/{item}.txt', 'a') as f:
            f.write(f"{item_id}\n")
    time.sleep(2)

    return item_id


def get_all_urls(driver):

    last_height = driver.execute_script("return document.body.scrollHeight")
    last_id = None
    while True:
        # Scroll down to bottom
        last_id = get_current_urls(driver, last_id)
        print(last_id)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def crawl_steam_page():

    ROOT_PAGE, tags = read_config('config.yaml', ['ROOT_PAGE', 'TAGS'])
    driver = webdriver.Firefox()

    for tag, codes in tags.items():
        # Launch the webpage and wait for 4 seconds
        last_id = None
        for code in codes:
            driver.get(f"{ROOT_PAGE}/?category1=998&tags={code}")
            time.sleep(4)
            get_all_urls(driver)

    driver.close()



def combine_tags_by_game_id(fpath, crawl=False):
    # combine all tags with same
    if crawl:
        crawl_steam_page()

    data = {}

    for area in read_config(['LABELS'])[0]:
        for feature in read_config(['LABELS'])[0][area]:
            with open(f"data/{feature}.txt", 'r') as f:
                ids = list(set([line.split(',')[0] if len(line.split(',')) > 1 else line.replace('\n', '') for line in f.readlines()]))
            for id in ids:
                if id in data.keys():
                    data[id].append(feature)
                else:
                    data[id] = [feature]

    with open(fpath, 'a') as f:
        for _id, _tags in data.items():
            f.writelines(f"{_id}, {'|'.join(_tags)}\n")
