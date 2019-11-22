from splinter import Browser
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
import configparser
import schedule


class C:
    W, G, R, P, Y, C = '\033[0m', '\033[92m', '\033[91m', '\033[95m', '\033[93m', '\033[36m'


def intro(test_mode):
    if test_mode:
        t = f'{C.R}TEST MODE{C.Y}'
    else:
        t = ''

    print(f"""{C.Y}
╦  ╦╔╗╔╦╔═╔═╗╔╦╗╦╔╗╔╔═╗╦  ╔═╗╔╦╗
║  ║║║║╠╩╗║╣  ║║║║║║╠═╣║  ║ ║ ║   {t}
╩═╝╩╝╚╝╩ ╩╚═╝═╩╝╩╝╚╝╩ ╩╩═╝╚═╝ ╩   {C.C}v1.0{C.W}
    """)


def runner(email, password, max_scroll, max_follow, min_sleep, max_sleep, test_mode):
    chrome_options = Options()
    chrome_options.add_extension('ublock_origin.crx')

    with Browser('chrome', chrome_options=chrome_options) as browser:
        # LOGIN
        browser.visit('https://www.linkedin.com/login')
        browser.fill('session_key', email)
        browser.fill('session_password', password)
        browser.find_by_css('.from__button--floating').click()

        # NETWORK
        browser.visit('https://www.linkedin.com/mynetwork')
        sleep(5)

        # REMOVE ELEMENTS
        browser.execute_script(
            "document.querySelector('#extended-nav').remove();")
        browser.execute_script(
            "document.querySelector('.mn-cohorts-list').remove();")
        browser.execute_script(
            "document.querySelector('#a11y-menu').remove();")
        for i in range(2):
            browser.execute_script("document.querySelector('aside').remove();")
        for i in range(max_scroll):
            browser.execute_script(
                "window.scrollTo(0,document.body.scrollHeight);")
            sleep(2)

        # FOLLOW
        buttons = browser.find_by_css('.artdeco-button--full')
        c = 0
        for button in buttons:
            button.mouse_over()
            if not test_mode:
                button.click()
            c += 1
            print(f'Following {c}/{max_follow}')
            sleep(randint(min_sleep, max_sleep))
            if not max_follow:
                break


def main():
    config = configparser.ConfigParser(interpolation=None)
    config.read('conf.ini')
    email = config['LINKEDIN']['email']
    password = config['LINKEDIN']['password']
    run_schedule = int(config['OPTIONS']['run_schedule'])
    run_time = config['OPTIONS']['run_time']
    max_scroll = int(config['OPTIONS']['max_scroll'])
    max_follow = int(config['OPTIONS']['max_follow'])
    min_sleep = int(config['OPTIONS']['min_sleep'])
    max_sleep = int(config['OPTIONS']['max_sleep'])
    test_mode = int(config['OPTIONS']['test_mode'])

    intro(test_mode)

    if run_schedule:
        print(f'Sleeping until {run_time}\n')
        schedule.every().day.at(run_time).do(runner, email, password,
                                             max_scroll, max_follow, min_sleep, max_sleep, test_mode)
        while True:
            schedule.run_pending()
            sleep(1)
    else:
        runner(email, password, max_scroll, max_follow,
               min_sleep, max_sleep, test_mode)


if __name__ == '__main__':
    main()
