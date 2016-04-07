## 淘宝宝贝评论抓取

本系统提供抓取淘宝商品下方的宝贝相关评论，输出格式为旺旺名，评论内容，链接，宝贝名。

控制台输出结果并写入到文件。

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

* 安装

  ```
  pip install pyquery
  ```

#### Selenium

* 安装

  ```
  pip install selenium
  ```

#### xlutils

* 安装

  ```
  pip install xlrd
  pip install xlwt
  pip install xlutils
  ```

## 运行测试

进入项目

* 从命令中运行

  ```
  python from_input.py
  ```

* 从文件读取

  ```
  python from_file.py
  ```

  文件路径配置

  ```
  config.py FROM_FILE
  ```

  ​