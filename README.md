# 飞书文档批量下载工具

一个帮你轻松下载飞书文档的 Python 工具集,包含两个主要功能:

1. 获取完整的知识库文档树
2. 批量下载文档为 Markdown 格式

## ✨ 特性

- 🚀 自动获取完整文档结构
- 📥 批量下载为 Markdown 格式
- 🔌 自动加载导出插件,无需手动安装
- 🎯 支持自定义下载目录
- 🔒 通过环境变量管理敏感信息

## 🛠 准备工作

1. **安装 Python**: 需要 Python 3.7 或更高版本

2. **安装依赖**:

```bash
pip install -r requirements.txt
```

3. **准备必要文件**:

   - 下载[ChromeDriver](https://chromedriver.chromium.org/downloads),放到 extensions 目录
   - 下载[Cloud Document Converter](https://github.com/whale4113/cloud-document-converter)插件,放到 extensions 目录

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

   - 打开飞书知识库
   - 按 F12 打开开发者工具
   - 找到任意请求,复制完整 Cookie

2. **获取 Space ID**

   - 从飞书知识库 URL 中找到形如`space/123456`的部分
   - 或在首页 URL 参数中找`space_id=xxxxx`

3. **获取文档 Token**
   - 从要下载的文档 URL 中复制 token 部分
   - 形如`RXdbwRyASiShtDky381ciwFEnpe`

## ❗️ 常见问题

1. **下载失败**

   - 检查 Cookie 是否过期
   - 确认 Chrome 版本与 ChromeDriver 版本匹配
   - 查看控制台报错信息

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
