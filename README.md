自动化业务：用户输入文字后交给AI模型识别后调用selenium技术搜索并解析联系信息，然后自动化发送邮件
\n一，项目只上传了代码，需要自行下载并放到项目根目录的如下：
（1）下载chrome和chromedriver：
https://googlechromelabs.github.io/chrome-for-testing/
（2）下载开源模型，可以在HuggingFace网站找符合自己设备配置的语言模型，例如：
https://huggingface.co/Qwen/Qwen2-1.5B-Instruct-GGUF/tree/main
二，自行准备搜索API的key：
本项目用到的搜索API地址：https://google.serper.dev/search
申请成功后，替换search_engine.py中的代码：
headers = {
        "X-API-KEY": "复制黏贴在这里",  # 👈 用你自己的 API Key 替换
        "Content-Type": "application/json"
    }
三，在qwen_model.py中替换你的AI模型路径：
MODEL_PATH = r"D:\ai_analysis_model\model\Qwen1.5-0.5B-Chat"# 👈 用你自己的AI模型路径替换
四，自行在项目中创建data目录。
注意：本项目目前未商业实战能力，如需用于商业请自行斟酌！
代码是死的，但人的创意是无限的！
