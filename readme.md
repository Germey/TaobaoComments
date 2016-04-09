## 项目简介

本系统用来抓取淘宝商品下方为我推荐板块宝贝相关评论和旺旺名。

输出格式为旺旺名，评论内容，链接，宝贝名。

控制台输出结果并写入到文件。

写入文件包括 excel，txt 格式。

## 平台兼容

* Windows
* Mac OS X
* Linux

## 环境配置

#### Python2.7

* 下载

   https://www.python.org/ 



* 测试

  命令行输入 `python` 提示版本信息，则安装成功。

#### PhantomJS

* 下载

   http://phantomjs.org/download.html



* 测试

  命令行输入 `phantomjs`  提示版本信息，则安装成功。

#### PyQuery

* 说明

  本库用来解析 HTML 代码。


* 安装

  ```
  pip install pyquery
  ```

#### Selenium

* 说明

  本库和 phantomjs 配合，驱动之运行。


* 安装

  ```
  pip install selenium
  ```

#### xlutils

* 说明

  本库用来处理 excel 相关内容。


* 安装

  ```
  pip install xlrd
  pip install xlwt
  pip install xlutils
  ```

#### twisted

* 安装

  ```
  pip install twisted
  ```

#### requests

* 安装

  ```
  pip install requests
  ```

## 运行测试

进入项目

* 从命令中运行，输入某宝贝的名称，即可完成抓取。

  ```
  python from_input.py
  ```

* 从文件读取，在 config.py 中配置好 FROM_FILE，即可自动提取链接抓取。

  ```
  python from_file.py
  ```


## 配置项目

在 config.py 中，有相应配置项。

* SERVICE_ARGS 

  模拟浏览器的配置，可以在此配置是否加载图片，是否缓存，是否使用代理等等。

* DRIVER

  全局会话，即相当于一个浏览器窗口。

* TIMEOUT

  请求超时时间。

* MAX_TRY

  最多尝试请求的次数。

* FROM_FILE

  淘宝的链接存放位置，在 file 文件夹，会正则匹配获取出所有的淘宝链接，然后逐个请求之。

* TO_TXT_FILE

  写入的目标文本文件，如果文件不存在，则会自动创建。

* TO_EXCEL_FILE

  写入的目标EXCEL文件，如果文件不存在，则会自动创建。

* TO_WANG_FILE

  单独抓取的非匿名旺旺名，保存到此文件中。

* CONSOLE_OUTPUT

  是否输出额外的提示信息，False 则不会提示额外信息。