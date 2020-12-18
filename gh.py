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
root_dir = 'C:\\Users\\drx\\Desktop\\dwn\\'
if not os.path.exists(root_dir):
    os.mkdir(root_dir)
os.system(os.path.realpath(sys.argv[0]).replace(os.path.realpath(sys.argv[0]).split('\\')[-1], 'shutd.bat'))


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
    shenqingh = 2016104879553
    # shenqingh = 2019300339762

    print('程序已启动')
    try:
        driver.get('http://cpquery.cnipa.gov.cn/')

        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'selectyzm_text')))
        yzm_text_element = driver.find_element_by_id("selectyzm_text")
        ActionChains(driver).move_to_element(yzm_text_element).perform()

        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'username1')))
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'password1')))
        print('账号密码输入中...')
        driver.execute_script("document.getElementById('username1').value = '15524847907'")
        driver.execute_script("document.getElementById('password1').type = 'Text'")
        driver.execute_script("document.getElementById('password1').value = 'P@ssw0rd'")
        print('账号密码输入完成')
        print('验证码下载中...')
        for i in range(0, 3):
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, 'jcaptchaimage')))
            yzm_pic_element = driver.find_element_by_id("jcaptchaimage")
            time.sleep(3)

            driver.save_screenshot('login/login.png')
            imgSize = yzm_pic_element.size
            imgLocation = yzm_pic_element.location
            rangle = (int(imgLocation['x']), int(imgLocation['y']), int(imgLocation['x'] + imgSize['width']),
                      int(imgLocation['y'] + imgSize['height'] + 20))  # 计算验证码整体坐标
            login = Image.open("login/login.png")
            frame4 = login.crop(rangle)
            frame4.save('login/authCode.png')
            print('验证码下载完成')
            print('尝试打码中...')
            yzm_location = Chaojiying_Client.cjy_do(9103)
            # 查看打码是否成功
            if yzm_location['err_no'] == -1005:
                print('打码平台余额不足,程序结束')
                driver.quit()
                exit()
            elif yzm_location['err_no'] == -3002:
                print('打码平台无响应,正在第' + str(i + 1) + '次重试')
                continue

            click1_location_x = int(yzm_location['pic_str'].split('|')[0].split(',')[0])
            click1_location_y = int(yzm_location['pic_str'].split('|')[0].split(',')[1])
            click2_location_x = int(yzm_location['pic_str'].split('|')[1].split(',')[0])
            click2_location_y = int(yzm_location['pic_str'].split('|')[1].split(',')[1])
            click3_location_x = int(yzm_location['pic_str'].split('|')[2].split(',')[0])
            click3_location_y = int(yzm_location['pic_str'].split('|')[2].split(',')[1])

            ActionChains(driver).move_to_element_with_offset(yzm_pic_element, click1_location_x,
                                                             click1_location_y).click().perform()

            ActionChains(driver).move_to_element_with_offset(yzm_pic_element, click2_location_x,
                                                             click2_location_y).click().perform()
            time.sleep(1)
            ActionChains(driver).move_to_element_with_offset(yzm_pic_element, click3_location_x,
                                                             click3_location_y).click().perform()
            time.sleep(1)
            print('打码完成')
            print('尝试登陆中...')
            if yzm_text_element.text == '验证成功':
                time.sleep(2)
                ActionChains(driver).move_to_element(driver.find_element_by_id("publiclogin")).click().perform()
                print('登录成功')
                print('尝试跳过协议页...')

                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.ID, 'goBtn')))

                time.sleep(2)
                driver.execute_script("document.getElementById('goBtn').disabled = ''")
                driver.execute_script(
                    "document.evaluate('/html/body/div[2]/div/div[2]/div[2]', document).iterateNext().style = 'display:none'")
                ActionChains(driver).move_to_element(driver.find_element_by_id("goBtn")).click().perform()
                print('跳过成功')

                print('尝试下载查询验证码中...')
                for j in range(0, 3):
                    try:
                        WebDriverWait(driver, 30).until(
                            EC.visibility_of_element_located((By.ID, 'select-key:shenqingh')))
                        time.sleep(2)
                        driver.execute_script(
                            "document.getElementById('select-key:shenqingh').value = " + str(shenqingh))
                        yzm_pic_element = driver.find_element_by_id("authImg")
                        time.sleep(1)
                        driver.save_screenshot('login/search.png')
                        imgSize = yzm_pic_element.size
                        imgLocation = yzm_pic_element.location
                        rangle = (
                            int(imgLocation['x']), int(imgLocation['y']), int(imgLocation['x'] + imgSize['width']),
                            int(imgLocation['y'] + imgSize['height']))  # 计算验证码整体坐标
                        login = Image.open("login/search.png")
                        frame4 = login.crop(rangle)
                        frame4.save('login/authSearchCode.png')
                        print('查询验证码下载完成')
                        print('尝试打码中...')
                        yzm_location = Chaojiying_Client.cjy_do(6001)
                        if yzm_location['err_no'] == -1005:
                            print('打码平台余额不足,程序结束')
                            driver.quit()
                            exit()
                        elif yzm_location['err_no'] == -3002:
                            print('打码平台无响应,正在第' + str(i + 1) + '次重试')
                            continue
                        driver.execute_script("document.getElementById('very-code').value = " + yzm_location['pic_str'])
                        time.sleep(1)
                        print('打码完成')
                        print('尝试查询中...')
                        ActionChains(driver).move_to_element(driver.find_element_by_id("query")).click().perform()
                        for k in range(0, 10):
                            try:
                                time.sleep(3)
                                rowslen = len(driver.find_element_by_xpath(
                                    '/html/body/div[2]/div[1]/div[2]/div[2]/div/table').find_elements_by_tag_name('tr'))
                                break
                            except Exception as e:
                                # print('查询失败,正在第' + str(k + 1) + '次重试')
                                pass
                        if not int(rowslen) == 1:
                            driver.execute_script('location.reload()')
                            print('验证码识别错误或者查询结果为空,正在第' + str(j + 1) + '次重试')
                            continue
                        else:
                            inventName = driver.find_element_by_xpath(
                                '/html/body/div[2]/div[1]/div[2]/div[2]/div/table/tbody/tr/td[3]').text
                            print('查询成功,发明名称为:', inventName)
                        ActionChains(driver).move_to_element(driver.find_element_by_xpath(
                            "/html/body/div[2]/div[1]/div[2]/div[2]/div/ul/li[2]/a")).click().perform()
                        WebDriverWait(driver, 30).until(lambda diver: driver.find_element_by_xpath("//*[@id='treeDemo_2']"))

                        # 清空url.txt
                        cls_url_txt()
                        print('清空url.txt成功')
                        # 创建下载根目录
                        create_root_folder(inventName)
                        # 申请文件
                        FileUtils.nginx_proxy(False)
                        print('\r尝试保存申请文件的地址(0%)', end='')
                        ul = driver.find_element_by_xpath('//*[@id="treeDemo_1_ul"]')
                        lis = ul.find_elements_by_xpath("li")
                        last_li_id = lis[-1].get_attribute('id')
                        rand = int(last_li_id.split('_')[1])
                        for k in range(1, rand):
                            time.sleep(2)
                            if driver.execute_script('return document.getElementById("treeDemo_' + str(k + 1) + '_a").style.color') == 'gray':
                                continue
                            ActionChains(driver).move_to_element(
                                driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + 1) + "']")).click().perform()
                            WebDriverWait(driver, 60).until_not(lambda diver: driver.find_element_by_xpath('/html/body/div[6]'))
                            time.sleep(2)
                            folderName = driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + 1) + "_a']").text
                            # 获取页数
                            page = int(driver.find_element_by_xpath('//*[@id="total"]').text)
                            for pIdx in range(0, page):
                                img_src = str(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/ul/li[' + str(pIdx + 1) + ']/div/img').get_property("src"))
                                save_url(img_src, folderName)
                            if not k == rand - 1:
                                print('\r尝试保存申请文件的地址(' + str(math.trunc(((k + 1) / rand) * 100)) + '%)', end='')
                            else:
                                print('\r尝试保存申请文件的地址(' + str(math.trunc(((k + 1) / rand) * 100)) + '%)')

                        print('申请文件的地址保存成功')
                        notice_num = driver.find_element_by_xpath("//*[text()='通知书']").get_attribute('id').split('_')[1]
                        notice_start_num = int(notice_num) + 1
                        ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@id="treeDemo_' + notice_num + '_a"]')).click().perform()
                        WebDriverWait(driver, 30).until(lambda diver: driver.find_element_by_xpath("//*[@id='treeDemo_" + notice_num + "']"))

                        # 通知书
                        print('\r尝试保存通知书的地址(0%)', end='')
                        ul = driver.find_element_by_xpath('//*[@id="treeDemo_' + notice_num + '_ul"]')
                        lis = ul.find_elements_by_xpath("li")
                        last_li_id = lis[-1].get_attribute('id')
                        rand = int(last_li_id.split('_')[1])
                        for k in range(0, rand - int(notice_num)):
                            time.sleep(2)
                            if driver.execute_script('return document.getElementById("treeDemo_' + str(k + notice_start_num) + '_a").style.color') == 'gray':
                                continue

                            # 判断检索
                            if driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + notice_start_num) + "']").text.endswith('检索'):
                                ActionChains(driver).move_to_element(
                                    driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + notice_start_num) + "']")).click().perform()
                                time.sleep(2)
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
                            WebDriverWait(driver, 60).until_not(lambda diver: driver.find_element_by_xpath('/html/body/div[6]'))
                            time.sleep(2)
                            folderName = driver.find_element_by_xpath("//*[@id='treeDemo_" + str(k + notice_start_num) + "_a']").text
                            # 获取页数
                            page = int(driver.find_element_by_xpath('//*[@id="total"]').text)
                            for pIdx in range(0, page):
                                img_src = str(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/ul/li[' + str(pIdx + 1) + ']/div/img').get_property("src"))
                                save_url(img_src, folderName)
                            if not k == rand - int(notice_num) - 1:
                                print('\r尝试保存通知书的地址(' + str(math.trunc(((k + 1) / (rand - int(notice_num))) * 100)) + '%)', end='')
                            else:
                                print('\r尝试保存通知书的地址(' + str(math.trunc(((k + 1) / (rand - int(notice_num))) * 100)) + '%)')
                        print('通知书的地址保存成功')

                        # 下载图片
                        FileUtils.nginx_proxy(True)
                        dwn_img(inventName)

                        driver.quit()
                        # 关闭firefox进程
                        print('正在关闭firefox进程...')
                        os.system(os.path.realpath(sys.argv[0]).replace(os.path.realpath(sys.argv[0]).split('\\')[-1], 'shutd.bat'))
                        print('关闭完成')

                        print('任务已完成')
                        exit()
                    except Exception as e:
                        print('拉闸,错误信息:', e)
                        print(traceback.format_exc())
                    print('查询失败,请重新运行程序')
                    driver.quit()
                    exit()
            else:
                print('登录失败,正在第' + str(i + 1) + '次重试')
        print('登录失败,请重新运行程序')
    except Exception as e:
        print('拉闸,错误信息:', e)
        print(traceback.format_exc())
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
        print('根目录创建成功')
    else:
        print('根目录已存在')
        shutil.rmtree(root_dir + root_name)


def dwn_img(root_name: str):
    delete_all_png(root_name)
    fd = open(root_dir + 'url.txt', encoding='utf-8')
    print('\r开始下载图片(0%)', end='')
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
        time.sleep(5)
        for filename in os.listdir(root_dir):
            if filename.endswith(".png"):
                # 移动文件
                shutil.move(root_dir + filename, dwn_file_dir + '\\' + filename)
                break
        if not fd_idx == fd_len:
            print('\r开始下载图片(' + str(math.trunc((fd_idx / fd_len) * 100)) + '%)', end='')
        else:
            print('\r开始下载图片(' + str(math.trunc((fd_idx / fd_len) * 100)) + '%)')
    print('图片下载完成')


def delete_all_png(root_name: str):
    path = root_dir + root_name + '\\'
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".png"):
                os.remove(os.path.join(root, name))


if __name__ == "__main__":
    spider_gh()