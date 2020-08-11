import pack.pyChrome as chrome
import auto_test
from auto_test import ini_data, do_action


# 命令对应函数
@auto_test.reg_fun
async def login(web: chrome.WebBrowser, account):
    n = 0
    while n < 5:
        try:
            web.Chrome.get('http://app.hzsgz.com:9009/views/App/CourseSelection/StuElectiveCourse.html')
            (await web.asyncFindElement_by_css_selector(
                '''#demo-tabs-box-2 > form > div:nth-child(2) > input''')).send_keys(account[0])
            web.Chrome.find_elements_by_css_selector('''#demo-tabs-box-2 > form > div:nth-child(3) > input''')[
                1].send_keys(
                account[1])
            web.Chrome.find_element_by_css_selector('''#demo-tabs-box-2 > form > button''').click()
            button = await web.asyncFindElement_by_css_selector('''#btnConsent''')
            if button is not None:
                button.click()
            if await web.asyncCheckUrl('http://app.hzsgz.com:9009/views/App/CourseSelection/StuElectiveCourse.html'):
                return True
        except Exception as e:
            print(e)
            n = n + 1
    return False


@auto_test.reg_fun
async def xk(web: chrome.WebBrowser, account):
    try:
        web.Chrome.find_element_by_css_selector('''#refreshContainer > li:nth-child(1) > div.content > div > 
        div.ctrl_btn.active''').click()
        (await web.asyncFindElement_by_css_selector(
            '''body > div.mui-popup.mui-popup-in > div.mui-popup-buttons''')).click()
        return True
    except Exception as e:
        print(e)
        return False


@auto_test.reg_fun
async def tx(web: chrome.WebBrowser, account):
    (await web.asyncFindElement_by_css_selector(
        '''#refreshContainer > li:nth-child(1) > div.content > div > div:nth-child(1)''')).click()
    (await web.asyncFindElement_by_css_selector(
        '''body > div.mui-popup.mui-popup-in > div.mui-popup-buttons > span.mui-popup-button.mui-popup-button-bold''')).click()
    (await web.asyncFindElement_by_css_selector(
        '''body > div.mui-popup.mui-popup-in > div.mui-popup-buttons''')).click()
    return True


if __name__ == '__main__':
    auto_test.test_id = 't3'
    auto_test.count = 6
    auto_test.test_account_name = 'xk'
    ini_data()
    do_action()
