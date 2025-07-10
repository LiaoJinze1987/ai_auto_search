#https://googlechromelabs.github.io/chrome-for-testing/

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#手动指定路径
chrome_binary_path = r"D:\ai_analysis_model\chrome-win64\chrome.exe"
chromedriver_path = r"D:\ai_analysis_model\chromedriver-win64\chromedriver.exe"

#配置启动参数
chrome_options = Options()
chrome_options.binary_location = chrome_binary_path
chrome_options.add_argument("--headless")  # 如需可视化可注释掉此行
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")

#设置服务对象
service =   Service(executable_path=chromedriver_path)

#启动解析器
driver = webdriver.Chrome(service=service, options=chrome_options)

#测试
driver.get("https://www.baidu.com")
print(driver.title)

# 关闭浏览器
driver.quit()