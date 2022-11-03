from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import re
import os


def welcome_page():
    print("#################################")
    print("##########   I-U-S-T   ##########")
    print("########## Reservation ##########")
    print("##########             ##########")
    print("##########  MAGESTEAM  ##########")
    print("#################################")
    print()

def login(driver):

    user_element = driver.find_element(By.NAME, "username")
    pass_element = driver.find_element(By.NAME, "password")
    pass_element.clear()
    user_element.clear()

    user_element.send_keys("97521432")
    pass_element.send_keys("2282927151")

    pass_element.send_keys(Keys.RETURN)
    print("[+]Login Successfully !!!")


def adjust_panel(driver):

    driver.get('http://stu.iust.ac.ir/nurture/user/multi/reserve/showPanel.rose')
    self_id = driver.find_element(By.ID, "selfId")
    for option in self_id.find_elements(By.TAG_NAME, 'option'):
        if option.get_attribute("value") == '1':
            option.click() # select() in earlier versions of webdriver
            break
    driver.execute_script("nextWeek();")
    time.sleep(1)
    print("[+] Panel Adjusted Successfully !!!")

def get_food(driver):

    whole_table_tags = driver.find_elements(By.TAG_NAME, "table")

    days = []
    foods = []
    food_dict = {}
    id_counter = 0


    file = open("food.txt", "a")

    for table in whole_table_tags:
        if table.get_attribute("cellspacing") == "2":
            days.append(table)
            cur_food = {}
            spans = table.find_elements(By.TAG_NAME, "span")
            for span in spans:
                if "foodNameSpan" in span.get_attribute("id"):
                    temp = span.get_attribute("innerHTML")
                    temp = temp.split(" | ")[1]
                    temp = temp.split("\n")[0]
                    temp = temp.replace(" ", "")
                    temp = temp.replace("*", "")
                    cur_food[temp] = "userWeekReserves.selected" + str(id_counter)
                    id_counter += 1
            foods.append(cur_food)

    return foods

def load_love_dict(filename):

    whole_qaza = open(filename, "r", encoding="utf-8")
    love_dict = {}
    for line in whole_qaza.readlines():
        food_love = line.split("-")
        food_love[0] = food_love[0].replace(" ","")
        food_love[1] = food_love[1].replace(" ","")
        food_love[1] = food_love[1].replace("\n","")
        love_dict[food_love[0]] = int(food_love[1])

    whole_qaza.close()

    return love_dict

def get_money(driver):

    current_money = int(driver.find_element(By.ID, "creditId").get_attribute("innerHTML"))/10000
    print("\n[$] Money : ", current_money, "\n")


def add_qaza(filname, qaza, score):
    file = open(filname, "a")
    file.write("\n" + qaza + "-" + str(score))
    file.close()
    print("[+] Food has been added to file !")


########### MAIN Code ##############
driver_path = "./chromedriver"
brave_path = "/usr/bin/brave-browser"

option = webdriver.ChromeOptions()
option.binary_location = brave_path
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
driver.get('http://stu.iust.ac.ir')

welcome_page()
login(driver)

try:
    adjust_panel(driver)
except:
    login(driver)
    adjust_panel(driver)

get_money(driver)

this_week_foods = get_food(driver)

try:
    love_dict = load_love_dict("data.txt")
except:
    print("[!] Error : data.txt doesn\'t Exists !")


###################
### Reservation ###
###################

reserve = {0:'', 1:'', 2:'', 3:'', 4:''}

day_counter = 0
for day in this_week_foods:
    maxim = -1
    for food in day.keys():
        food_likes = None
        for text in love_dict.keys():
            if food in text or text in food:
                food_likes = love_dict[text]
                break
        try:
            if maxim <= food_likes:
                maxim = food_likes
                reserve[day_counter] = day[food]
        except:
            pass

    maxim = -1
    food_likes = -2
    day_counter += 1



for i in range(5):
    try:
        if driver.find_element(By.ID, reserve[i]).get_attribute("checked") != "true":
            driver.execute_script("document.getElementById('" + reserve[i] + "').checked = true;")
            driver.execute_script("document.getElementById('" + reserve[i] + "').onclick();")
            print("[+] Reservation Number", str(i+1), "Is Compeleted !!")
        else:
            print("[!] It Had Been Reserved Before !")
    except:
        print("[!] Error in Reservation Number", str(i+1), "Is Compeleted !!")
        print("[!] Maybe it\'s Holiday ... or something else happened")

get_order = input("[?] Are You Sure ? (y,n) ")
if get_order == 'y':
    try:
        driver.execute_script("finalReserve();")
        print("[+] Reservation Compeleted !")
    except:
        print("[!] Error ..")
    driver.close()
else:
    get_order = input("[?] Are You Sure ? (y,n) ")
    if get_order == 'y':
        try:
            driver.execute_script("finalReserve();")
            print("[+] Reservation Compeleted !")
        except:
            print("[!] Error ..")
    else:
        driver.close()
        exit(0)
