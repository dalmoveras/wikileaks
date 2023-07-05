#!/usr/bin/env python

import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


file = open("wiki-torrents.txt","x")
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
# chrome_options.add_argument("--headless")


def split(elems):
    torrents = []
    folders = []
    for el in elems:
        if '.torrent' in el.get_attribute('href'):
            torrents.append(el)
        else:
            folders.append(el)
    return (torrents, folders)

def traverse(elems):
   
    tmp_elems = []
    time.sleep(2)
    if type(elems) == list:
        del elems[0]
        for el in elems:
            el.click()
            print(driver.title)
            tmp_elems = driver.find_elements(By.XPATH, "//a[@href]")
            driver.back()
    else:
        elems.click()
        print(driver.title)
        tmp_elems =  driver.find_elements(By.XPATH, "//a[@href]")
    
    torrents, folders = split(tmp_elems)

    if len(folders) > 1:
        traverse(folders)
    else:
        file.write('\n'.join(t.get_attribute('href') for t in torrents))
        file.write('\n')
        driver.back()
        return

def main():
    url = 'https://file.wikileaks.org/torrent/'
    #url = 'https://file.wikileaks.org/torrent/aryan-nation-2009/'
    driver.get(url)
    elems = driver.find_elements(By.XPATH,"//a[@href]")
    del elems[0]
    torrents, folders = split(elems)
    file.write('\n'.join(t.get_attribute('href') for t in torrents))
    file.write('\n') 
    
    for folder in folders:
        traverse(folder)
        if driver.current_url != url:
            driver.back()








if __name__ == "__main__":
    main()

