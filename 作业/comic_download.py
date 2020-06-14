# import gevent
# from gevent.queue import Queue
# from gevent import monkey
# monkey.patch_all()
# 教学系统的浏览器设置方法
import time
# 本地Chrome浏览器的静默默模式设置：
from selenium import  webdriver #从selenium库中调用webdriver模块
from selenium.webdriver.chrome.options import Options # 从options模块中调用Options类
import urllib.request,csv,os
import ssl


# chrome_options = Options() # 实例化Option对象
# chrome_options.add_argument('--headless') # 把Chrome浏览器设置为静默模式
driver = webdriver.Chrome() # 设置引擎为Chrome，在后台默默运行options = chrome_options
ssl._create_default_https_context = ssl._create_unverified_context

driver.get('https://www.manhuabei.com/')
time.sleep(3)
comic_text = input('请输入需要下载的漫画关键字：')
comic_find = driver.find_element_by_id("keywords")
comic_find.send_keys(comic_text)
search_button = driver.find_element_by_id("btnSearch")
search_button.click()
time.sleep(3)
c_url = driver.current_url

driver.get(c_url)
time.sleep(3)
num = 0
choice_dit = {}
for comic_search in driver.find_elements_by_xpath("//li[@class='list-comic']/p/a"):
    num = num+1
    choice = str(num) + '、'+ comic_search.text
    choice_dit[str(num)] = [comic_search.text,comic_search]
    print(choice)
if choice_dit:
    url_file = open('url.csv','w',newline='',encoding='gbk',errors='ignore')
    url_write = csv.writer(url_file)
    url_write .writerow(['漫画名称','章节','页数','图片链接'])
    cont = 1
    while cont:
        choice_num = input('以上为本站的搜索结果，请选择您需要下载的漫画的数字编号：')
        if choice_dit[choice_num][0]:
            if not os.path.exists(r"F:\comic\%s"%(choice_dit[choice_num][0])):
                os.mkdir(r"F:\comic\%s"%(choice_dit[choice_num][0]))           
            continue_link = choice_dit[choice_num][1].get_attribute("href")

            start_url_list = []
            driver.get(continue_link)
            time.sleep(2)
            for li_url in driver.find_elements_by_xpath("//ul[@id='chapter-list-1']/li/a"):
                start_url = li_url.get_attribute("href")
                start_url_list.append(start_url)

            for url in start_url_list:
                driver.get(url)
                time.sleep(2)
                comic_name = driver.find_element_by_xpath("//div[@class='head_title']/h1").text
                chapter = driver.find_element_by_xpath("//div[@class='head_title']/h2").text
                page_num = driver.find_element_by_xpath("//option[@selected='selected']").text
                link = driver.find_element_by_xpath("//div[@id='images']/img").get_attribute("src")
                print(link)
                url_write.writerow([comic_name,chapter,page_num,link])
                f = urllib.request.urlopen(link) 
                data = f.read() 
                name = comic_name+'-'+chapter+'-'+page_num
                os.mkdir(r"F:\comic\%s\%s"%(comic_name,chapter))
                with open(r"F:\comic\%s\%s\%s.jpg"%(comic_name,chapter,name), "wb") as code:     
                    code.write(data)
                num_str = driver.find_element_by_xpath("//div[@id='images']/p").text
                num = int(num_str[-3:-1])
                for i in range(1,num):
                    next_url = url+'?p=%d'%(i+1)
                    driver.get(next_url)
                    time.sleep(2)

                    page_num = '第%d页'%(i+1)
                    link = driver.find_element_by_xpath("//div[@id='images']/img").get_attribute("src")
                    url_write .writerow([comic_name,chapter,page_num,link])
                    name = comic_name+'-'+chapter+'-'+page_num 
                    f = urllib.request.urlopen(link) 
                    data = f.read() 
                    with open(r"F:\comic\%s\%s\%s.jpg"%(comic_name,chapter,name), "wb") as code:     
                        code.write(data)
            url_file.close()  
            driver.close()    
            cont = 0   
        else:
            print('输入有误，请重新输入')
else:
    print('本站无此漫画，byebye！')
    url_file.close()
    driver.close() 

# task_list = []
# for i in range(5):
#     task = gevent.spawn(comic_spider)
#     task_list.append(task)
# gevent.joinall(task_list)