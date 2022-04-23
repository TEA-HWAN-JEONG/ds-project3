from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pickle

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}

def top_500_list():
    url = "https://www.op.gg/leaderboards/tier?page=1&region=kr"
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    p = soup.find_all('a', 'name')
    lst = []
    lst.append(str(p[0]).split('<')[1].split('>')[1])

    p = soup.find_all('span', 'name')
    for i in range(len(p)):
        lst.append(str(p[i]).split('<')[1].split('>')[1])

    p = soup.find_all('strong')
    for i in range(len(p)):
        lst.append(str(p[i]).split('<')[1].split('>')[1])

    for i in range(2, 6):
        url = f"https://www.op.gg/leaderboards/tier?page={i}&region=kr"
        page = requests.get(url, headers = headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        p = soup.find_all('strong')
        for i in range(len(p)):
            lst.append(str(p[i]).split('<')[1].split('>')[1])

    lst = [i for i in lst if i not in 'Privacy Policy']
    return lst

def opgg_control(name):
    url = f'https://www.op.gg/summoners/kr/{name}'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("no-sandbox")
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36')
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    driver.get(url)
    driver.implicitly_wait(1)
    driver.find_element_by_xpath('//*[@id="__next"]/div[6]/div[2]/div[1]/ul/li[2]/button').click()
    req = driver.page_source
    return req

def data():
    summoner = top_500_list()
    lst_sum = []
    lst_vic = []
    lst_time = []
    lst_name = []
    lst_d_spell = []
    lst_f_spell = []
    lst_k = []
    lst_d = []
    lst_a = []
    lst_level = []
    lst_party = []
    lst_party = []
    lst_cs = []
    lst_ward = []

    for i in summoner:
        lst_sum += [i]*20
        url = f'https://www.op.gg/summoners/kr/{i}'
        page = requests.get(url, headers = headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        p = soup.find_all('div', 'game-result')
        for j in range(len(p)):
            lst_vic.append(str(p[j]).split('<')[1].split('>')[1])

        p = soup.find_all('div', 'game-length')
        for j in range(len(p)):
            lst_time.append(str(p[j]).split('<')[1].split('>')[1])

        p = soup.find_all('div', 'champion')
        for j in range(len(p)):
            lst_name.append(p[j].img['alt'])

        p = soup.find_all('div', 'spell')
        for j in range(0, 40, 2):
            lst_d_spell.append(p[j].img['alt'])
            lst_f_spell.append(p[j+1].img['alt'])
        
        p = soup.find_all('div', 'k-d-a')
        for j in range(len(p)):
            lst_kda = str(p[j]).split('/')
            lst_k.append(int(lst_kda[0].split('>')[2].split('<')[0]))
            lst_d.append(int(lst_kda[2].split('<')[1].split('>')[1]))
            lst_a.append(int(lst_kda[4].split('>')[1].split('<')[0]))

        p = soup.find_all('div', 'level')
        for j in range(len(p)):
            lst_level.append(int(str(p[j]).split('<')[1].split('>')[1].split(' ')[1]))
        
        p = soup.find_all('div', 'kill-participantion')
        for j in range(len(p)):
            lst_party.append(int(str(p[j]).split('-->')[2].split('<')[0]))
        
        p = soup.find_all('div', 'stats')
        for j in range(len(p)):
            lst_cs.append(int(str(p[j]).split('relative">')[1].split('<')[0]))
        
        p = soup.find_all('div', 'control')
        for j in range(len(p)):
            lst_ward.append(int(str(p[j]).split('-->')[-1].split('<')[0].split(' ')[2]))

    df = pd.DataFrame({'summoners' : lst_sum, 'result' : lst_vic, 'time' : lst_time, 'champion' : lst_name, 'd_spell' : lst_d_spell, 'f_spell' : lst_f_spell, 'kill' : lst_k, 'deths' : lst_d, 'assist' : lst_a, 'level' : lst_level, 'kill_part' : lst_party, 'cs' : lst_cs, 'ward' : lst_ward})
    with open("data.pkl", "wb") as pickle_file:
        pickle.dump(df, pickle_file)
    return df