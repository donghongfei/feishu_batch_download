# 飞书文档批量下载工具

⚠️ **重要免责声明**

1. 本工具仅用于学习研究使用。在使用本工具前，请确保您已经获得了相关文档的访问权限。
2. 使用本工具时请遵守飞书平台的使用条款和政策。请勿用于任何未授权、非法或者商业用途。
3. 请合理使用,不要进行高频率请求。建议保持默认的请求延迟,避免对飞书服务器造成压力。
4. 下载的文档请遵守知识产权相关法律法规,不得违规传播或用于商业用途。
5. 由于使用本工具导致的任何问题(包括但不限于账号封禁、数据丢失、法律风险等),均由使用者自行承担。
6. 作者不对使用本工具产生的任何后果负责。

使用本工具即表示您已阅读并同意上述免责声明。如不同意,请勿使用本工具。

---

一个帮你轻松下载飞书文档的 Python 工具集,包含两个主要功能:

1. 获取完整的知识库文档树
2. 批量下载文档为 Markdown 格式

> 📝 **特别说明**
>
> 1. 本项目使用了 Cloud Document Converter 插件。为实现静默下载,对原插件做了修改,修改版源码见: [donghongfei/cloud-document-converter](https://github.com/donghongfei/cloud-document-converter)
> 2. 默认提供的 ChromeDriver 适用于 Mac M 芯片。其他设备请参考[ChromeDriver 下载页面](https://developer.chrome.com/docs/chromedriver/downloads?hl=zh-cn)下载对应版本。

## ✨ 特性

- 🚀 自动获取完整文档结构
- 📥 批量下载为 Markdown 格式

## 🛠 准备工作

1. **安装 Python**: 需要 Python 3.7 或更高版本

2. **安装依赖**:

```bash
pip install -r requirements.txt
```

3. **准备必要文件**:

   > 💡 为了方便使用,项目已内置以下文件到 extensions 目录:
   >
   > - ChromeDriver (当前适配 Mac M 芯片)
   > - Cloud Document Converter 插件(已修改支持静默下载)

   如需自行准备:

   - 下载[ChromeDriver](https://chromedriver.chromium.org/downloads) 对应版本,放到 extensions 目录
   - 从[donghongfei/cloud-document-converter](https://github.com/donghongfei/cloud-document-converter) 下载源码，自行编译后，放到 extensions 目录。具体方法可以问chatGPT。

4. **配置环境变量**:
   - 复制`.env.example`为`.env`
   - 按文件中的说明填写配置

## 🚀 使用方法

### 第一步: 获取文档树

```bash
python get_wiki_tree.py
```

这会生成`wiki_tree.json`文件,包含完整的文档结构。

### 第二步: 下载文档

```bash
python export_markdown.py
```

文档会自动下载到`download_output`目录。

## 📝 使用提示

1. **获取 Cookie**

   - 登录飞书，打开飞书知识库
   - 按 F12 打开开发者工具
   - 找到任意请求,复制完整 Cookie

2. **获取 Space ID**

   - 从飞书知识库 URL 中找到形如`space/123456`的部分
   - 或在首页 URL 参数中找`space_id=xxxxx`

3. **获取文档 Token**
   - 通过 Chrome 浏览器控制台，查看要下载的 wiki 页面网络请求
   - 找到类似链接：`https://langgptai.feishu.cn/space/api/wiki/v2/tree/get_info/?space_id=7260334668648644609&with_space=true&with_perm=true&expand_shortcut=true&need_shared=true&exclude_fields=5&with_deleted=true&wiki_token=RXdbwRyASiShtDky381ciwFEnpe&synced_block_host_token=CKzqdVFFTooOsbxttXmcGebInOb&synced_block_host_type=22`
   - wiki_token 参数，形如`RXdbwRyASiShtDky381ciwFEnpe`

## ❗️ 常见问题

1. **下载失败**

   - 检查 Cookie 是否过期
   - 确认 Chrome 版本与 ChromeDriver 版本匹配

2. **获取文档树失败**
   - 验证环境变量是否正确设置
   - 确认 Space ID 格式是否正确
   - 检查网络连接

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📜 开源协议

MIT License

## 🙏 感谢

- [Cloud Document Converter](https://github.com/whale4113/cloud-document-converter): 提供 Markdown 导出功能
- [Selenium](https://www.selenium.dev/): 提供浏览器自动化支持
- [Gemini 2.0 Flash Thinking Experimental](https://gemini.google.com/app): 编码调试支持
- [Claude](https://claude.ai): 项目结构调整及文档编写