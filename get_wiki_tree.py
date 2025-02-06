import json
import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

# 配置日志输出格式 - 这样可以在日志里看到具体的时间,方便排查问题
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为INFO,这样可以看到程序的主要运行状态
    format="%(asctime)s [%(levelname)s] %(message)s",  # 设置日志格式:时间 [日志级别] 日志内容
    datefmt="%Y-%m-%d %H:%M:%S",  # 设置日期时间格式
)

# 从环境变量获取飞书空间ID - 环境变量可以保护敏感信息不被泄露
BASE_SPACE_ID = os.environ.get("FEISHU_SPACE_ID")

# 飞书API接口地址 - 这是飞书官方提供的接口
WIKI_API_BASE_URL = "https://langgptai.feishu.cn/space/api/wiki/v2"
NODE_INFO_API_BASE_URL = "https://langgptai.feishu.cn/space/api/wiki/v2/tree"


def get_node_children(wiki_token, cookies, delay=0.5):
    """
    获取一个知识库节点下的所有子节点信息

    参数说明:
    wiki_token: 知识库节点的唯一标识符,可以在飞书文档URL中找到
    cookies: 用户登录信息,从浏览器中复制
    delay: 每次请求后等待的时间(秒),防止请求太快被限制

    返回值:
    list: 所有子节点的信息列表,如果没有子节点或出错则返回空列表
    """
    # 检查是否设置了空间ID
    if not BASE_SPACE_ID:
        logging.error("错误:请设置FEISHU_SPACE_ID环境变量")
        return []

    # 构建请求URL
    url = f"{WIKI_API_BASE_URL}/tree/get_node_child/?space_id={BASE_SPACE_ID}&wiki_token={wiki_token}"

    # 设置请求头,模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }

    logging.info(f"正在获取节点的子节点列表: {url}")

    try:
        # 发送GET请求获取子节点数据
        response = requests.get(url, headers=headers, cookies=cookies)
        response.raise_for_status()  # 如果请求失败会抛出异常
        data = response.json()

        # 检查返回数据是否正确
        if data["code"] == 0 and data["data"] and wiki_token in data["data"]:
            logging.debug(f"成功获取到{len(data['data'][wiki_token])}个子节点")
            time.sleep(delay)  # 等待一段时间,避免请求过快
            return data["data"][wiki_token]
        else:
            logging.warning(f"获取子节点失败,API返回: {data}")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"请求出错: {e}")
        return []


def build_tree_recursive(wiki_token, cookies, delay=0.5):
    """
    递归构建知识库的树状结构

    这个函数会:
    1. 获取当前节点的详细信息
    2. 获取当前节点的所有子节点
    3. 对每个子节点重复这个过程
    4. 最终生成一个完整的树状结构

    参数说明:
    wiki_token: 当前节点的唯一标识符
    cookies: 用户登录信息
    delay: 每次请求后等待的时间(秒)

    返回值:
    dict: 包含当前节点及其所有子节点信息的字典
    """
    # 检查是否设置了空间ID
    if not BASE_SPACE_ID:
        logging.error("错误:请设置FEISHU_SPACE_ID环境变量")
        return None

    # 构建获取节点信息的URL
    node_info_url = f"{NODE_INFO_API_BASE_URL}/get_info/?space_id={BASE_SPACE_ID}&with_space=true&with_perm=true&expand_shortcut=true&need_shared=true&exclude_fields=5&with_deleted=true&wiki_token={wiki_token}&synced_block_host_token=CKzqdVFFTooOsbxttXmcGebInOb&synced_block_host_type=22"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }

    logging.info(f"正在获取节点详细信息: {node_info_url}")

    try:
        # 获取节点详细信息
        response = requests.get(node_info_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        node_data_response = response.json()

        # 检查返回数据的结构是否正确
        if (
            node_data_response["code"] == 0
            and node_data_response["data"]
            and "tree" in node_data_response["data"]
            and "nodes" in node_data_response["data"]["tree"]
            and wiki_token in node_data_response["data"]["tree"]["nodes"]
        ):

            logging.debug(f"成功获取节点信息")
            time.sleep(delay)

            # 提取节点信息
            node_data = node_data_response["data"]["tree"]["nodes"][wiki_token]
            tree_node = {
                "title": node_data["title"],  # 节点标题
                "url": node_data["url"],  # 节点URL
                "wiki_token": wiki_token,  # 节点唯一标识符
                "children": [],  # 子节点列表
            }
        else:
            logging.warning(f"获取节点信息失败,API返回: {node_data_response}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"请求出错: {e}")
        return None

    # 获取并处理子节点
    logging.debug(f"开始获取子节点信息...")
    children_nodes = get_node_children(wiki_token, cookies, delay)

    if children_nodes:
        logging.debug(f"找到{len(children_nodes)}个子节点")
        for child_node in children_nodes:
            # 如果子节点还有下一级,继续递归处理
            if child_node["has_child"]:
                logging.debug(f"节点 [{child_node['title']}] 还有子节点,继续处理...")
                child_tree = build_tree_recursive(
                    child_node["wiki_token"], cookies, delay
                )
                if child_tree:
                    tree_node["children"].append(child_tree)
            else:
                # 如果是叶子节点,直接添加到children列表
                tree_node["children"].append(
                    {
                        "title": child_node["title"],
                        "url": child_node["url"],
                        "wiki_token": child_node["wiki_token"],
                        "children": [],
                    }
                )
    else:
        logging.debug(f"该节点没有子节点")

    return tree_node


if __name__ == "__main__":
    logging.info("程序开始运行")

    # 从环境变量获取Cookie
    cookie_string = os.environ.get("FEISHU_COOKIE")
    if not cookie_string:
        logging.error("请设置FEISHU_COOKIE环境变量")
        print(
            "\n错误:缺少FEISHU_COOKIE环境变量\n"
            "请按以下步骤操作:\n"
            "1. 用浏览器打开飞书知识库\n"
            "2. 按F12打开开发者工具\n"
            "3. 在Network标签页刷新页面\n"
            "4. 找到任意请求,复制Cookie值\n"
            "5. 设置为FEISHU_COOKIE环境变量\n"
        )
        exit(1)

    # 将Cookie字符串转换为字典格式
    cookies_dict = {}
    for item in cookie_string.split(";"):
        item = item.strip()
        if "=" in item:
            key, value = item.split("=", 1)
            cookies_dict[key] = value
    logging.info("Cookie加载完成")

    # 获取根节点token
    root_wiki_token = os.environ.get("ROOT_WIKI_TOKEN", "RXdbwRyASiShtDky381ciwFEnpe")
    if root_wiki_token == "RXdbwRyASiShtDky381ciwFEnpe":
        logging.warning(
            f"当前使用的是示例token: {root_wiki_token},请修改为你的文档token"
        )
        print(
            "\n警告:当前使用示例token\n"
            "请按以下步骤设置正确的token:\n"
            "1. 打开要抓取的飞书知识库文档\n"
            "2. 从URL中复制wiki_token参数值\n"
            "3. 设置为ROOT_WIKI_TOKEN环境变量\n"
        )

    logging.info(f"使用根节点token: {root_wiki_token}")

    # 设置请求间隔时间
    request_delay = 1
    logging.info(f"设置请求间隔: {request_delay}秒")

    logging.info("开始获取文档树...")
    root_tree = build_tree_recursive(root_wiki_token, cookies_dict, request_delay)

    if root_tree:
        logging.info("成功获取文档树结构")

        # 打印树状结构
        def print_tree(node, indent=0):
            """把文档树打印成层级结构"""
            print(
                "  " * indent
                + f"- {node['title']} ({node['url']}) - token: {node['wiki_token']}"
            )
            for child in node["children"]:
                print_tree(child, indent + 1)

        print("\n文档树结构:")
        print_tree(root_tree)

        # 保存为JSON文件
        output_file = "wiki_tree.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(root_tree, f, indent=4, ensure_ascii=False)
        logging.info(f"文档树已保存到: {output_file}")
        print(f"\n文档树已保存到文件: {os.path.abspath(output_file)}")
    else:
        logging.error("获取文档树失败")
        print(
            "\n错误:获取文档树失败\n"
            "可能的原因:\n"
            "1. 环境变量未正确设置\n"
            "2. Cookie已过期\n"
            "3. 文档token不正确\n"
            "4. 网络问题\n"
            "请检查以上问题并重试\n"
        )

    logging.info("程序运行结束")
