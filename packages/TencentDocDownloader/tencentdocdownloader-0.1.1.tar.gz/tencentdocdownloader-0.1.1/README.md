# TencentDocDownload
腾讯文档下载 目前只支持excel文档

# How To Use
```py
from TencentDocDownloader.excel_downloader import download
url = "your-url-goes-here"
download(url)

from TencentDocDownloader.excel_downloader import download
url = "your-url-goes-here"
download(url, to_path)
```

## 获取cookies
1.针对chrome系列浏览器，安装插件Get cookies.txt，链接 https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid
> (可能需要翻墙)
2.打开chromedevtools(右击->检查)，application，storage，cookies
将对应的值全部复制出来，放到download文件头部`cookie_string = "" #可以手动写死cookies内容`内，并解除（以及user_data后面）相关注释
