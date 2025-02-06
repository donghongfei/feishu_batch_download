# -*- coding: utf-8 -*-
# 批量下载飞书文档为 Markdown 文件的 Python 脚本
# 最终版本：自动加载 .crx 插件，配置 Chrome 自动下载，无需手动登录，无需模拟回车键

import json
import logging
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()  # 加载 .env 文件

# 配置日志输出
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# ChromeDriver 路径
chromedriver_path = os.getenv("CHROME_DRIVER_PATH", "./extensions/chromedriver")


# 插件 .crx 文件路径
crx_path = os.getenv(
    "CRX_PATH", "./extensions/cloud_document_converter-1.9.2-chrome.crx"
)


# 插件导出按钮的元素选择器 (CSS 选择器，基于 data-cdc-button-type 属性)
export_button_selector = (By.CSS_SELECTOR, "button[data-cdc-button-type='download']")

# 配置 ChromeOptions
chrome_options = ChromeOptions()
chrome_options.add_extension(crx_path)  # 加载 .crx 插件

prefs = {
    "download.default_directory": os.path.join(
        os.getcwd(), "download_output"
    ),  # 设置默认下载目录为脚本所在目录下的 download_output 文件夹
    "download.prompt_for_download": False,  # 禁止弹出下载对话框 (对插件弹窗也有效)
    "plugins.always_open_pdf_externally": True,  # (可选) 如果需要下载 PDF 文件，可以设置这个选项
}
chrome_options.add_experimental_option("prefs", prefs)


# 初始化 Chrome 浏览器
service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
logging.info("Chrome 浏览器已启动")

# 确保 download_output 文件夹存在，如果不存在则创建
download_dir = os.getenv("DOWNLOAD_PATH", "./download_output")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
    logging.info(f"已创建下载目录: {download_dir}")
else:
    logging.info(f"下载目录已存在: {download_dir}")


def load_links_from_json(json_file):
    """从 JSON 文件加载链接，并扁平化为一个列表。"""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    links = []

    def extract_links(node):
        if "url" in node:
            links.append(node["url"])
        if "children" in node:
            for child in node["children"]:
                extract_links(child)

    extract_links(data)
    return links


# 从 JSON 文件加载链接
feishu_links = load_links_from_json("wiki_tree.json")
logging.info(f"从 JSON 文件加载了 {len(feishu_links)} 个链接")

for index, link in enumerate(feishu_links):
    try:
        logging.info(f"开始处理第 {index + 1}/{len(feishu_links)} 个链接: {link}")
        driver.get(link)
        logging.info("已打开链接")

        # 等待页面加载，并确保飞书文档内容加载出来 (根据网络情况调整)
        time.sleep(5)  # 基本等待时间

        # 定位插件导出按钮并点击
        logging.info("尝试定位插件导出按钮...")
        export_button = WebDriverWait(driver, 20).until(  # 增加等待时间到20秒
            EC.element_to_be_clickable(export_button_selector)
        )
        export_button.click()
        logging.info("插件导出按钮已点击")

        #  等待下载完成 (根据文档大小和网络情况调整)
        time.sleep(10)
        logging.info("等待下载完成... (假设等待 10 秒)")
        logging.info(f"第 {index + 1}/{len(feishu_links)} 个链接处理完成")

    except Exception as e:
        logging.error(f"处理链接 {link} 时出错: {e}")
        logging.error("请检查错误信息，并尝试手动打开该链接，确认是否可以正常下载")
        logging.error("脚本将继续处理下一个链接...")
        # 可以选择截图保存当前页面，方便调试
        # driver.save_screenshot(f"error_screenshot_{index}.png")

driver.quit()
logging.info("所有链接处理完成！")
logging.info("Chrome 浏览器已关闭")
