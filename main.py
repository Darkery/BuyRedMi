from selenium import webdriver
import time

RETRY_TIMES = 2000
USER_NAME = ""
PASSWORD = ""

def snap(sleep_time=0.1):
    time.sleep(sleep_time)
    print("browser.title = " + browser.title)


def login():
    # login
    browser.get('https://account.xiaomi.com/pass/serviceLogin/')
    user_name = browser.find_element_by_name("user")
    password = browser.find_element_by_name("password")
    user_name.send_keys(USER_NAME)
    password.send_keys(PASSWORD)
    browser.find_element_by_id("login-button").click()

    snap()


def refresh_item_page(item_url, window_num):
    # goto item page
    command = "window.open('" + item_url + "')"
    browser.execute_script(command)
    browser.switch_to.window(browser.window_handles[window_num])
    snap()

    # refresh until it could buy
    while 1:
        try:
            # red airdots
            # browser.find_element_by_xpath('//*[@id="J_headNav"]/div/div/div/a[5]').click()
            # shouhuan4
            # browser.find_element_by_xpath('//*[@id="J_headNav"]/div/div/div[2]/a[6]').click()
            browser.find_element_by_css_selector("#J_headNav > div > div > div.right > a.btn.btn-small.btn-primary")
        except:
            snap()
            continue
        break


    snap()

    i = 0
    while i < RETRY_TIMES:
        try:
            buy_btn = browser.find_element_by_css_selector('#J_buyBtnBox > li:nth-child(1) > a')
            status = buy_btn.get_attribute("data-name")
        except:
            snap()
            continue

        if status == "加入购物车":
            break

        try:
            browser.refresh()
        except:
            snap()
            continue

        snap()
        i += 1
        print("第{}次重试，共{}次！！！".format(i, RETRY_TIMES))

    if i == RETRY_TIMES:
        print("Timeout !!!!!")
        return

    while 1:
        try:
            buy_btn.click()
            break
        except:
            snap()
            continue
    snap()

def check_out_bill(window_num, item_num):
    browser.execute_script("window.open('https://static.mi.com/cart/')")
    browser.switch_to.window(browser.window_handles[window_num])

    j = 1
    while j < item_num:
        snap(0.3)
        browser.find_element_by_xpath('//*[@id="J_cartListBody"]/div/div[1]/div/div[5]/div/a[2]').click()
        j += 1

    snap()

    while 1:
        try:
            go_checkout_btn = browser.find_element_by_id('J_goCheckout')
            browser.execute_script("arguments[0].click();", go_checkout_btn)
            break
        except:
            snap()
            continue
    snap()

    while 1:
        try:
            address_item = browser.find_element_by_xpath('//*[@id="J_addressList"]/div[1]')
            browser.execute_script("arguments[0].click();", address_item)
            browser.find_element_by_id('J_checkoutToPay').click()
            break
        except:
            snap()
            continue
    snap()


if __name__ == '__main__':

    # item_url = "https://www.mi.com/redmiairdots/?cfrom=search"
    item_url = "https://www.mi.com/shouhuan4/?cfrom=search"
    # item_url = "https://www.mi.com/camera-360/?cfrom=search"

    browser = webdriver.Chrome()
    login()
    refresh_item_page(item_url, 1)
    check_out_bill(2, 1)
    while 1:
        try:
            browser.find_element_by_xpath('//*[@id="J_weixin"]/img').click()
            break
        except:
            snap()
            continue
