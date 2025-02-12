# <div align="center">本地deepseek模型实现微信自动回复</div>

**持续更新中————**

## 1.下载[ollama](https://ollama.com/)
下载完成之后在命令行里输入`ollama -v`有结果即为下载成功
  
## 2.本地部署[deepseek](https://ollama.com/search)
```
模型名称            参数数量    内存占用        运行代码                    最低配置
deepseek-r1:1.5b    1.5B        1.1Gb   ollama run deepseek-r1:1.5b     8GB RAM，无显卡加速；适合老旧设备
deepseek-r1:7b      7B          4.7Gb   ollama run deepseek-r1:7b       16GB RAM，6GB显存
deepseek-r1:8b      8B          4.9Gb   ollama run deepseek-r1:8b       16GB RAM，8GB显存
deepseek-r1:14b     14B         9.0Gb   ollama run deepseek-r1:14b      ？
deepseek-r1:32b     32B         20Gb    ollama run deepseek-r1:32b      ？
deepseek-r1:70b     70B         43Gb    ollama run deepseek-r1:70b      ？
deepseek-r1:671b    671B        404Gb   ollama run deepseek-r1:671b     ？
```
我的电脑是3060 6G显存  32GB RAM 实测7B流畅，8B能用，14B卡顿但能用

如需要下载deepseek-r1:7b，使用命令行输入`ollama run deepseek-r1:7b`即可

## 3.采用python3.9
所需依赖均在`requirements.txt`中，使用`pip install -r requirements.txt`即可

## 4.替换文件
将所有图片替换为自己的微信图片，`./image/friend`目录存放需要自动回复目标的头像图片