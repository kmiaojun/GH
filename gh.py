# coding=utf-8
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image, ImageEnhance
from chaojiying import Chaojiying_Client
import FileUtils
import subprocess
import traceback
import os, shutil
import sys
import math
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser
import logging
import random
logging.basicConfig(level=logging.INFO,
                    filename='./log/log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
cf = configparser.ConfigParser()
cf.read("./conf/sys.conf", encoding='utf-8-sig')
root_dir = cf.get("sys", "dwn_root_dir")
wait_time = int(cf.get("sys", "global_wait_time_weight"))
web_wait_time = int(cf.get("sys", "web_driver_wait_time_weight"))
if not os.path.exists(root_dir):
    os.mkdir(root_dir)
os.system(os.path.realpath(sys.argv[0]).replace(os.path.realpath(sys.argv[0]).split('\\')[-1], 'shutd.bat'))
cfed = configparser.ConfigParser()
cfed.read("./conf/ed.conf", encoding='utf-8-sig')


def spider_gh():
    # todo 启动 nginx 并记录 pid, 用于程序结束关闭nginx
    # todo 可以自行获取 运行目录,
    FileUtils.nginx_proxy(True)

    options = webdriver.FirefoxOptions()
    # options.add_argument("--window-size=1280,720")
    options.add_argument('-headless')
    options.add_argument('--host-resolver-rules=MAP cpquery.cnipa.gov.cn 127.0.0.1')
    driver = webdriver.Firefox(options=options)
    # shenqingh = 2018214893335
    # shenqingh = 2016104879553
    # shenqingh = 2019300339762
    # 2019105148830
    # 2018214893335
    if cf.get("sys", "ed_state") == '1':
        ed_name = get_ed_name()
    else:
        ed_name = "normal"

    print(cfed.get(ed_name, "prt_sqh"))
    shenqingh = input()
    sys_step = 0
    sys_total_step = 6
    try:
        # print('程序已启动')
        print('\r' + cfed.get(ed_name, "prt_qzbz") + '(0%)', end='')
        sys_step += 1
        driver.get('http://cpquery.cnipa.gov.cn/')

        WebDriverWait(driver, web_wait_time).until(
            EC.visibility_of_element_located((By.ID, 'selectyzm_text')))
        yzm_text_element = driver.find_element_by_id("selectyzm_text")
        ActionChains(driver).move_to_element(yzm_text_element).perform()

        WebDriverWait(driver, web_wait_time).until(
            EC.visibility_of_element_located((By.ID, 'username1')))
        WebDriverWait(driver, web_wait_time).until(
            EC.visibility_of_element_located((By.ID, 'password1')))
        # print('账号密码输入中...')
        driver.execute_script("document.getElementById('username1').value = '15524847907'")
        driver.execute_script("document.getElementById('password1').type = 'Text'")
        driver.execute_script("document.getElementById('password1').value = 'P@ssw0rd'")
        # print('账号密码输入完成')
        print('\r' + cfed.get(ed_name, "prt_qzbz") + '(' + str(math.trunc((sys_step / sys_total_step) * 100)) + '%)', end='')
        sys_step += 1
        # print('验证码下载中...')
        login_flg = False
        for i in range(0, 5):
            WebDriverWait(driver, web_wait_time).until(
                EC.visibility_of_element_located((By.ID, 'jcaptchaimage')))
            yzm_pic_element = driver.find_element_by_id("jcaptchaimage")
            time.sleep(1 + wait_time)

            driver.save_screenshot('login/login.png')
            imgSize = yzm_pic_element.size
            imgLocation = yzm_pic_element.location
            rangle = (int(imgLocation['x']), int(imgLocation['y']), int(imgLocation['x'] + imgSize['width']),
                      int(imgLocation['y'] + imgSize['height'] + 20))  # 计算验证码整体坐标
            login = Image.open("login/login.png")
            frame4 = login.crop(rangle)
            frame4.save('login/authCode.png')
            # print('验证码下载完成')
            # print('尝试打码中...')
            yzm_location = Chaojiying_Client.cjy_do(9103)
            # 查看打码是否成功
            if yzm_location['err_no'] == -1005:
                print('\n' + cfed.get(ed_name, "prt_yebz"))
                driver.quit()
                exit()
            elif yzm_location['err_no'] == -3002:
                print('\r' + cfed.get(ed_name, "prt_ptwxy") + ',正在第' + str(i + 1) + '次重试', end='')
                continue

            click1_location_x = int(yzm_location['pic_str'].split('|')[0].split(',')[0])
            click1_location_y = int(yzm_location['pic_str'].split('|')[0].split(',')[1])
            click2_location_x = int(yzm_location['pic_str'].split('|')[1].split(',')[0])
            click2_location_y = int(yzm_location['pic_str'].split('|')[1].split(',')[1])
            click3_location_x = int(yzm_location['pic_str'].split('|')[2].split(',')[0])
            click3_location_y = int(yzm_location['pic_str'].split('|')[2].split(',')[1])

            ActionChains(driver).move_to_element_with_offset(yzm_pic_element, click1_location_x,
                                                             click1_location_y).click().perform()
            time.sleep(1)
            ActionChains(driver).move_to_element_with_offset(yzm_pic_element, click2_location_x,
                                                             click2_location_y).click().perform()
            time.sleep(1)
            ActionChains(driver).move_to_element_with_offset(yzm_pic_element, click3_location_x,
                                                             click3_location_y).click().perform()
            time.sleep(1)
            # print('打码完成')
            # print('尝试登陆中...')
            if yzm_text_element.text == '验证成功':
                print('\r' + cfed.get(ed_name, "prt_qzbz") + '(' + str(math.trunc((sys_step / sys_total_step) * 100)) + '%)', end='')
                sys_step += 1
                login_flg = True
                break
        if not login_flg:
            print('\r' + cfed.get(ed_name, "prt_dlsb"))
            driver.quit()
            exit()

        time.sleep(wait_time)
        ActionChains(driver).move_to_element(driver.find_element_by_id("publiclogin")).click().perform()
        # print('登录成功')
        print('\r' + cfed.get(ed_name, "prt_qzbz") + '(' + str(math.trunc((sys_step / sys_total_step) * 100)) + '%)', end='')
        sys_step += 1
        # print('尝试跳过协议页...')

        WebDriverWait(driver, web_wait_time).until(
            EC.visibility_of_element_located((By.ID, 'goBtn')))

        time.sleep(wait_time)
        driver.execute_script("document.getElementById('goBtn').disabled = ''")
        driver.execute_script(
            "document.evaluate('/html/body/div[2]/div/div[2]/div[2]', document).iterateNext().style = 'display:none'")
        ActionChains(driver).move_to_element(driver.find_element_by_id("goBtn")).click().perform()
        # print('跳过成功')
        print('\r' + cfed.get(ed_name, "prt_qzbz") + '(' + str(math.trunc((sys_step / sys_total_step) * 100)) + '%)', end='')
        sys_step += 1
        # print('尝试下载查询验证码中...')
        search_flg = False
        for j in range(0, 5):
            # try:
            WebDriverWait(driver, web_wait_time).until(
                EC.visibility_of_element_located((By.ID, 'select-key:shenqingh')))
            time.sleep(wait_time)
            driver.execute_script(
                "document.getElementById('select-key:shenqingh').value = " + str(shenqingh))
            yzm_pic_element = driver.find_element_by_id("authImg")
            time.sleep(wait_time)
            driver.save_screenshot('login/search.png')
            imgSize = yzm_pic_element.size
            imgLocation = yzm_pic_element.location
            rangle = (
                int(imgLocation['x']), int(imgLocation['y']), int(imgLocation['x'] + imgSize['width']),
                int(imgLocation['y'] + imgSize['height']))  # 计算验证码整体坐标
            login = Image.open("login/search.png")
            frame4 = login.crop(rangle)
            frame4.save('login/authSearchCode.png')
            # print('查询验证码下载完成')
            # print('\r正在执行前置步骤(' + str(math.trunc((sys_step / sys_total_step) * 100)) + '%)', end='')
            # sys_step += 1
            # print('尝试打码中...')
            yzm_location = Chaojiying_Client.cjy_do(6001)
            if yzm_location['err_no'] == -1005:
                print('\n' + cfed.get(ed_name, "prt_yebz"))
                driver.quit()
                exit()
            elif yzm_location['err_no'] == -3002:
                print('\r' + cfed.get(ed_name, "prt_ptwxy") + ',正在第' + str(i + 1) + '次重试', end='')
                continue
            driver.execute_script("document.getElementById('very-code').value = " + yzm_location['pic_str'])
            time.sleep(wait_time)
            # print('打码完成')
            # print('尝试查询中...')
            ActionChains(driver).move_to_element(driver.find_element_by_id("query")).click().perform()
            for k in range(0, 10):
                try:
                    time.sleep(1 + wait_time)
                    rowslen = len(driver.find_element_by_xpath(
                        '/html/body/div[2]/div[1]/div[2]/div[2]/div/table').find_elements_by_tag_name('tr'))
                    break
                except Exception as e:
                    # print('查询失败,正在第' + str(k + 1) + '次重试')
                    pass
            if not int(rowslen) == 1:
                driver.execute_script('location.reload()')
                print('\r' + cfed.get(ed_name, "prt_ptwxy") + ',正在第' + str(j + 1) + '次重试', end='')
                continue
            else:
                inventName = driver.find_element_by_xpath(
                    '/html/body/div[2]/div[1]/div[2]/div[2]/div/table/tbody/tr/td[3]').text
                print('\r'  + cfed.get(ed_name, "prt_qzbz") + '(100%)')
                print(cfed.get(ed_name, "prt_cxcg"), inventName)
                search_flg = True
                break
        if not search_flg:
            print('\r' + cfed.get(ed_name, "prt_cxsb"))
            driver.quit()
            exit()

        ActionChains(driver).move_to_element(driver.find_element_by_xpath(
            "/html/body/div[2]/div[1]/div[2]/div[2]/div/ul/li[2]/a")).click().perform()
        WebDriverWait(driver, web_wait_time).until(lambda diver: driver.find_element_by_xpath("//*[@id='treeDemo_2']"))

        # 清空url.txt
        cls_url_txt()
        # print('清空url.txt成功')
        # 申请文件
        FileUtils.nginx_proxy(False)
        print('\r' + cfed.get(ed_name, "prt_sqwj") + '(0%)', end='')
        ul = driver.find_element_by_xpath('//*[@id="treeDemo_1_ul"]')
        lis = ul.find_elements_by_xpath("li")
        last_li_id = lis[-1].get_attribute('id')
        rand = int(last_li_id.split('_')[1])
        for k in range(1, rand):
            time.sleep(wait_time)
            if driver.execute_script('return document.getElementById("treeDemo_' + str(k + 1) + '_a").style.color') == 'gray':
                continue
            ActionChains(driver).move_to_element(
                driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + 1) + "']")).click().perform()
            WebDriverWait(driver, web_wait_time).until_not(lambda diver: driver.find_element_by_xpath('/html/body/div[6]'))
            time.sleep(wait_time)
            folderName = driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + 1) + "_a']").text
            # 获取页数
            page = int(driver.find_element_by_xpath('//*[@id="total"]').text)
            for pIdx in range(0, page):
                img_src = str(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/ul/li[' + str(pIdx + 1) + ']/div/img').get_property("src"))
                save_url(img_src, folderName)
            if not k == rand - 1:
                print('\r' + cfed.get(ed_name, "prt_sqwj") + '(' + str(math.trunc(((k + 1) / rand) * 100)) + '%)', end='')

        print('\r' + cfed.get(ed_name, "prt_sqwj") + '(100%)')
        print(cfed.get(ed_name, "prt_sqwjcg"))
        notice_num = driver.find_element_by_xpath("//*[text()='通知书']").get_attribute('id').split('_')[1]
        notice_start_num = int(notice_num) + 1
        ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@id="treeDemo_' + notice_num + '_a"]')).click().perform()
        WebDriverWait(driver, web_wait_time).until(lambda diver: driver.find_element_by_xpath("//*[@id='treeDemo_" + notice_num + "']"))

        # 通知书
        print('\r' + cfed.get(ed_name, "prt_tzs") + '(0%)', end='')
        ul = driver.find_element_by_xpath('//*[@id="treeDemo_' + notice_num + '_ul"]')
        lis = ul.find_elements_by_xpath("li")
        last_li_id = lis[-1].get_attribute('id')
        rand = int(last_li_id.split('_')[1])
        for k in range(0, rand - int(notice_num)):
            time.sleep(wait_time)
            if driver.execute_script('return document.getElementById("treeDemo_' + str(k + notice_start_num) + '_a").style.color') == 'gray':
                continue

            # 判断检索
            if driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + notice_start_num) + "']").text.endswith('检索'):
                ActionChains(driver).move_to_element(
                    driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + notice_start_num) + "']")).click().perform()
                time.sleep(wait_time)
                folderName = driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + notice_start_num) + "_a']").text
                toHandle = driver.window_handles
                driver.switch_to.window(toHandle[1])
                driver.maximize_window()
                select_element = driver.find_element_by_xpath('/html/body/div/div[1]/div')
                driver.save_screenshot('login/select.png')
                imgSize = select_element.size
                imgLocation = select_element.location
                rangle = (
                    int(imgLocation['x']), int(imgLocation['y']),
                    int(imgLocation['x'] + imgSize['width']),
                    int(imgLocation['y'] + imgSize['height']))
                select = Image.open("login/select.png")
                frame4 = select.crop(rangle)
                frame4.save('login/selectPic' + str(k + notice_start_num) + '.png')
                driver.close()
                driver.switch_to.window(toHandle[0])
                save_url('selectPic' + str(k + notice_start_num), folderName)
                continue
            ActionChains(driver).move_to_element(
                driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + notice_start_num) + "']")).click().perform()
            WebDriverWait(driver, web_wait_time).until_not(lambda diver: driver.find_element_by_xpath('/html/body/div[6]'))
            time.sleep(wait_time)
            folderName = driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + notice_start_num) + "_a']").text
            # 获取页数
            page = int(driver.find_element_by_xpath('//*[@id="total"]').text)
            for pIdx in range(0, page):
                img_src = str(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/ul/li[' + str(pIdx + 1) + ']/div/img').get_property("src"))
                save_url(img_src, folderName)
            if not k == rand - int(notice_num) - 1:
                print('\r' + cfed.get(ed_name, "prt_tzs") + '(' + str(math.trunc(((k + 1) / (rand - int(notice_num))) * 100)) + '%)', end='')
        print('\r' + cfed.get(ed_name, "prt_tzs") + '(100%)')
        print(cfed.get(ed_name, "prt_tzscg"))

        # 下载图片
        FileUtils.nginx_proxy(True)
        dwn_img(inventName)

        driver.quit()
        # 关闭firefox进程
        # print('正在关闭firefox进程...')
        os.system(os.path.realpath(sys.argv[0]).replace(os.path.realpath(sys.argv[0]).split('\\')[-1], 'shutd.bat'))
        # print('关闭完成')

        print(cfed.get(ed_name, "prt_rwwc"))
        exit()
    except Exception as e:
        print(cfed.get(ed_name, "prt_lz"), e)
        print(traceback.format_exc())
        logging.error(traceback.format_exc())
    driver.quit()
    exit()


def dwn_browser(url: str):
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.dir', root_dir)
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/png;charset=UTF-8')
    driver = webdriver.Firefox(firefox_profile=profile, options=options)
    driver.get(url)


def save_url(url: str, file_name: str):
    fd = open(root_dir + 'url.txt', 'a+', encoding='utf-8')
    fd.write(file_name + '||' + url + '\n')


def cls_url_txt():
    open(root_dir + 'url.txt', 'w', encoding='utf-8').close()


def create_root_folder(root_name: str):
    if not os.path.exists(root_dir + root_name):
        os.mkdir(root_dir + root_name)
        # print('根目录创建成功')
    else:
        # print('根目录已存在')
        shutil.rmtree(root_dir + root_name)
        os.mkdir(root_dir + root_name)


def dwn_img(root_name: str):
    # 创建下载根目录
    create_root_folder(root_name)
    delete_all_png(root_name)
    fd = open(root_dir + 'url.txt', encoding='utf-8')
    print('\r' + cfed.get(ed_name, "prt_xztp") + '(0%)', end='')
    fd_len = len(fd.readlines())
    fd_idx = 0
    fd = open(root_dir + 'url.txt', encoding='utf-8')
    for line in fd:
        fd_idx += 1
        file_name = line.split('||')[0]
        file_url = line.split('||')[1]
        dwn_file_dir = root_dir + root_name + '\\' + file_name
        if not os.path.exists(dwn_file_dir):
            os.mkdir(dwn_file_dir)
        if file_url.startswith('select'):
            pic_location = os.path.realpath(sys.argv[0]).replace(os.path.realpath(sys.argv[0]).split('\\')[-1], 'login')
            shutil.move(pic_location + '\\' + file_url.split('\n')[0] + '.png', dwn_file_dir + '\\00001.png')
        else:
            # 下载
            dwn_browser(file_url)
        time.sleep(1 + wait_time)
        flg = False
        for sxh in range(0, 10):
            time.sleep(1)
            for filename in os.listdir(root_dir):
                if filename.endswith(".png"):
                    # 移动文件
                    shutil.move(root_dir + filename, dwn_file_dir + '\\' + filename)
                    flg = True
                    break
            if flg:
                break
        if not fd_idx == fd_len:
            print('\r' + cfed.get(ed_name, "prt_xztp") + '(' + str(math.trunc((fd_idx / fd_len) * 100)) + '%)', end='')
        else:
            print('\r' + cfed.get(ed_name, "prt_xztp") + '(' + str(math.trunc((fd_idx / fd_len) * 100)) + '%)')
    print(cfed.get(ed_name, "prt_xztpwc"))


def delete_all_png(root_name: str):
    path = root_dir + root_name + '\\'
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".png"):
                os.remove(os.path.join(root, name))


def get_ed_name():
    rad = random.randint(0, 50)
    if 0 < rad <= 10:
        return 'normal'
    elif 10 < rad <= 20:
        return 'english'
    elif 25 < rad <= 30:
        return 'mars'
    elif 37 < rad <= 40:
        return 'dog'
    elif 40 < rad <= 50:
        return 'japanese'
    else:
        return 'normal'


if __name__ == "__main__":
    spider_gh()