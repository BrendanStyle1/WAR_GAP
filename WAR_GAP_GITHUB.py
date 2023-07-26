
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 02:58:14 2023

@author: brendan
"""
#%% Get every retired player who has had a 6-win season
import datetime as dt
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Firefox, FirefoxOptions
#driver.close()
#options = Options()
opts = FirefoxOptions()
opts.add_argument("--width=950")
opts.add_argument("--height=1025")
driver_path = "path_to_geckodriver"
driver = Firefox(options=opts)
#driver = webdriver.Chrome(chrome_options = options, executable_path = driver_path)
url = "https://stathead.com/baseball/player-batting-season-finder.cgi?request=1&order_by=b_war&ccomp%5B1%5D=gt&cval%5B1%5D=6.0&cstat%5B1%5D=b_war&is_active=N"
driver.get(url)
# driver.find_element(By.XPATH, '')
menu = driver.find_element(By.XPATH, '//*[@id="nav_trigger"]/a') #log in to stathead acccount
menu.click()
login = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/ul[2]/li[3]/a')
login.click()
username = "username"
password = 'password'
uname = driver.find_element(By.XPATH,'//*[@id="username"]')
uname.send_keys(username)
pword = driver.find_element(By.XPATH,'//*[@id="password"]')
pword.send_keys(password)
nex = driver.find_element(By.XPATH, '//*[@id="sh-login-button"]')
nex.click()
df = pd.DataFrame()
for f in range(1,8):
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,5050)")#scrolls to click "next page" button at bottom of screen
    time.sleep(1)
    if f == 7: #7 pages worth of players, the first 6 have 200 each but the 7th has only 4 names
        for i in range(1,5):
            war = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/form/div[2]/div[2]/div[4]/div[3]/table/tbody/tr['+str(i)+']/td[2]').text
            war = pd.DataFrame([war])
            name = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/form/div[2]/div[2]/div[4]/div[3]/table/tbody/tr['+str(i)+']/td[1]/a').text
            name = pd.DataFrame([name])
            data = pd.concat([name, war], axis=1)
            df = df.append(data)
    else:
        for i in range(1, 206):
            if i in [36, 72, 108, 144, 180]: #these are empty rows, row numbers can vary based on size of window
                continue
            else:
                war = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/form/div[2]/div[2]/div[4]/div[3]/table/tbody/tr['+str(i)+']/td[2]').text
                war = pd.DataFrame([war])
                name = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/form/div[2]/div[2]/div[4]/div[3]/table/tbody/tr['+str(i)+']/td[1]/a').text
                name = pd.DataFrame([name])
                data = pd.concat([name, war], axis=1)
                df = df.append(data)
    if f == 7:
        break
    else: #scrolls to bottom of page again(sometimes the scroll wouldn't work properly) and clicks next page button
        driver.execute_script("window.scrollTo(0,5051)")
        time.sleep(2)    
        nextpage = driver.find_element(By.CLASS_NAME,'button2.next')
        nextpage.click()
df.columns = ['name','war']
df['war'] = df['war'].astype(float)
df = df.sort_values(by=['name','war'],ascending = False)
df = df.drop_duplicates(subset=['name'], keep='first') #since the list was sorted by WAR, keeping first insures only highest war season remains
df =df.sort_values(by=['war'],ascending = False)
df = df.reset_index()
df = df.drop(['index'], axis =1) #creates index based on the highest WAR

# GETTING WAR AND TAKING TOTAL PERCENTAGE
driver.execute_script("window.scrollTo(0,0)") #scrolls back up to bring search bar into view
df2 = pd.DataFrame()
search = driver.find_element(By.CSS_SELECTOR, '.ac-input')
search.send_keys('Babe Ruth')                         
search.send_keys(Keys.DOWN)
search.send_keys(Keys.ENTER)
time.sleep(3)
war = driver.find_element(By.CSS_SELECTOR, ".p1 > div:nth-child(1) > p:nth-child(2)").text #takes career war from page
name = driver.find_element(By.CSS_SELECTOR, '#meta > div:nth-child(2) > h1:nth-child(1) > span:nth-child(1)').text #takes name so dataframes can merge later on
war = pd.DataFrame([war])
name = pd.DataFrame([name])
data = pd.concat([name, war], axis=1)
df2 = df2.append(data)
more_stats_dropdown = driver.find_element(By.CSS_SELECTOR, "#meta_more_button") #clicks the "more stats" button, which somehow helps the computer find the career war, only needs to be clicked once per browswer
more_stats_dropdown.click()
for i in range(1,464):
    search = driver.find_element(By.CSS_SELECTOR, 'div.ac-outline:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
    names = df.iloc[i,0]
    if names in ['Billy Hamilton', 'Stan Spence', 'Art Wilson', 'Ken Williams', 'John Mayberry', 'George Stone']: #these names have another player with an identical/very similar name to theirs that shows up first on the search, so there must be 2 down presses
        search = driver.find_element(By.CSS_SELECTOR, 'div.ac-outline:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
        search.click()
        search.send_keys(names)
        search.send_keys(Keys.DOWN)
        time.sleep(1)
        search.send_keys(Keys.DOWN)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        war = driver.find_element(By.CSS_SELECTOR, ".p1 > div:nth-child(1) > p:nth-child(2)").text
        name = driver.find_element(By.CSS_SELECTOR, '#meta > div:nth-child(2) > h1:nth-child(1) > span:nth-child(1)').text
        war = pd.DataFrame([war])
        name = pd.DataFrame([name])
    else:
        search = driver.find_element(By.CSS_SELECTOR, 'div.ac-outline:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
        search.click()
        search.send_keys(names)
        time.sleep(1)
        search.send_keys(Keys.DOWN)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        war = driver.find_element(By.CSS_SELECTOR, ".p1 > div:nth-child(1) > p:nth-child(2)").text
        name = driver.find_element(By.CSS_SELECTOR, '#meta > div:nth-child(2) > h1:nth-child(1) > span:nth-child(1)').text
        war = pd.DataFrame([war])
        name = pd.DataFrame([name])
    data = pd.concat([name, war], axis=1)
    df2 = df2.append(data)
driver.close
df2.columns = ['name','c_war']
df2['c_war'] = df2['c_war'].astype(float).sort_values(by=['c_war'],ascending = False).reset_index().drop(['index'], axis =1)
df3 = pd.merge(df,df2,on='name',how='outer')
df3['percent'] = df3['war']/df3['c_war']
df3 = df3.sort_values(by=['c_war'], ascending = False).reset_index().drop(['index'], axis =1)
df3['percent'] = round(df3['percent'],3) #creating a row that shows what percentage of the player's career war came from best season
df3.to_csv('default.csv', index=False) #saving progress so code above doesn't have to be run again in case of future error
driver.cose()
#%% Opening new driver
import datetime as dt
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
opts = FirefoxOptions()
opts.add_argument("--width=950")
opts.add_argument("--height=1025")
driver_path = "path_to_geckodriver"
driver = Firefox(options=opts)
url = "https://www.baseball-reference.com/players/r/ruthba01.shtml"
driver.get(url)
#logging in
menu = driver.find_element(By.XPATH, '//*[@id="nav_trigger"]/a')
menu.click()
login = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/ul[2]/li[3]/a')
login.click()
username = "username"
password = 'password'
uname = driver.find_element(By.XPATH,'//*[@id="username"]')
uname.send_keys(username)
pword = driver.find_element(By.XPATH,'//*[@id="password"]')
pword.send_keys(password)
nex = driver.find_element(By.XPATH, '//*[@id="sh-login-button"]')
nex.click()
#%% getting total number of seasons played to later iterate through
df3.read_csv('default.csv')
import re
fd = pd.DataFrame()
for i in range(0,464):
    names = df3.iloc[i,0]
    if names in ['Billy Hamilton', 'Stan Spence', 'Art Wilson', 'Ken Williams', 'John Mayberry', 'George Stone']:
        search = driver.find_element(By.CSS_SELECTOR, 'div.ac-outline:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
        search.click()
        search.send_keys(names)
        search.send_keys(Keys.DOWN)
        time.sleep(1)
        search.send_keys(Keys.DOWN)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
    else:
        search = driver.find_element(By.CSS_SELECTOR, 'div.ac-outline:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
        search.click()
        search.send_keys(names)
        time.sleep(1)
        search.send_keys(Keys.DOWN)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
    szn = driver.find_element(By.CSS_SELECTOR, '#batting_standard > tfoot:nth-child(5) > tr:nth-child(1) > th:nth-child(1)').text #the text is however many years the player played along with the string 'yrs' after it
    ctl = re.findall(r'\d+',szn) #removes the 'yrs' from the text and leaves just the number of seasons played
    r_szn = float(ctl) #turns the string of years into a float
    name = driver.find_element(By.CSS_SELECTOR, '#meta > div:nth-child(2) > h1:nth-child(1) > span:nth-child(1)').text #name taken for merging purposes
    name = pd.DataFrame([name])
    r_szn = pd.DataFrame([r_szn])
    data = pd.concat([name, r_szn], axis=1)
    fd = fd.append(data)
fd.columns = ['name','seasons']
df4 = pd.merge(df3,fd, on='name',how='outer')
df4.to_csv('default_2.csv',index=False) #saving progress again
#%% Obtaining 2nd highest war
df5 = pd.read_csv('default_2.csv')
df5['w/s'] = df5['c_war']/df5['seasons'] #creating a row for war per season
df6 = pd.DataFrame()
for i in range(0,464):
    df7 = pd.DataFrame()
    szns = df5.iloc[i,4]
    names = df5.iloc[i,0]
    if names in ['Billy Hamilton', 'Stan Spence', 'Art Wilson', 'Ken Williams', 'John Mayberry', 'George Stone']:
        search = driver.find_element(By.CSS_SELECTOR, 'div.ac-outline:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
        search.click()
        search.send_keys(names)
        search.send_keys(Keys.DOWN)
        time.sleep(1)
        search.send_keys(Keys.DOWN)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
    else:
        search = driver.find_element(By.CSS_SELECTOR, 'div.ac-outline:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
        search.click()
        search.send_keys(names)
        time.sleep(1)
        search.send_keys(Keys.DOWN)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
    while True:  #most bref pages had the same XPATH for the WAR and years columns, but for those who didn't, a try-except block has been created to accomodate them
        try:
            for p in range(1,(szns+1)):
                 szn_w = driver.find_element(By.XPATH, '/html/body/div[2]/div[6]/div[3]/div[4]/table/tbody/tr['+str(p)+']/td[15]').text #takes war from each season and appends, if error is encouterd here just copy and past xpath again
                 szn_w = pd.DataFrame([szn_w])
                 szn_y = driver.find_element(By.XPATH, '/html/body/div[2]/div[6]/div[3]/div[4]/table/tbody/tr['+str(p)+']/th').text #takes the year they accumulates said war and appends
                 szn_y = pd.DataFrame([szn_y])
                 data = pd.concat([szn_y,szn_w], axis=1)
                 df7 = df7.append(data)
        except NoSuchElementException:
            for p in range(1,(szns+1)):
                 szn_w = driver.find_element(By.XPATH, '/html/body/div[2]/div[7]/div[3]/div[4]/table/tbody/tr['+str(p)+']/td[15]').text
                 szn_w = pd.DataFrame([szn_w])
                 szn_y = driver.find_element(By.XPATH, '/html/body/div[2]/div[7]/div[3]/div[4]/table/tbody/tr['+str(p)+']/th').text
                 szn_y = pd.DataFrame([szn_y])
                 data = pd.concat([szn_y,szn_w], axis=1)
                 df7 = df7.append(data)
            break
        else:
            break
    df7.columns = ['year','season_war']
    df7 = df7.sort_values(by=['season_war'],ascending = False)
    df7 = df7.reset_index().drop(['index'],axis=1)
    df8 = df7 #I can't quite remember why I switched to a new df for this part but it worked so I'll roll with it
    """some players had gaps in their resumes which would go into the df as blank cells. 
    Since dropna() decided it wasn't going to work, I had to add another try-except block
    to check. By sorting by war without changing the type to float first(since converting to float results in a ValueError), 
    it pushes the blank cells to the bottom of the df, which it why I am indexing backwards in the for loop"""
    
    for r in range((len(df8)-1),-1,-1):
        try:
            df8['season_war'] = df8['season_war'].astype(float)
        except ValueError:
            df8 = df8.drop(r)
        else:
            break
    df8 = df8.groupby(df8['year']).agg({'year':'first','season_war':'sum'}) #combines based on year for players who got traded mid season
    df8 = df8.sort_values(by=['season_war'],ascending = False)
    df8 = df8.reset_index().drop(['index'],axis=1)
    for c in range(0,len(df8)):
        if c == 1:
            continue
        else:
            df8 = df8.drop(c)
    df8['season_war'] = df8['season_war'].astype(float)
    df6 = df7.append(df8)
df6 = df6.reset_index().drop(['index'],axis=1)
df_final = pd.concat([df5,df6], axis=1)
df_final['diff'] = df_final['war']-df_final['season_war']
df_final = df_final.drop('year',axis=1)
df_final = (df_final.rename(columns={'war': 'best_war'}).rename(columns={'season_war': '2nd_best_war'}) #renaming the columns
            .rename(columns={'percent': 'percent_of_career_from_best'}))
df_final = df_final[['name','best_war','2nd_best_war','diff','c_war','seasons','w/s','percent_of_career_from_best']] #reorganizing the columns
df_final['w/s'] = round(df_final['w/s'],1)
df_final.to_csv('default_final.csv',index=False)

"""
this code still isn't perfect. the main problem left to fix is that, for players who did get traded in-season, I won't be able to get
all their years, since their performance with both teams shows up as different rows, and they will have more rows than seasons played
"""