# 使用说明

1. 建议使用PyCharm Professional版本，使用虚拟环境功能，安装必要的库`selenium`
2. 运行前请确保安装了`chromedriver`，官网下载地址为[https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)(需要科学上网)，将其加入环境变量或直接将该程序复制到该工作目录下
3. 本程序使用的python版本为2.7.14
4. 首次使用请运行`init_directory.py`，以请确保成功创建如下目录：
    - 在工作目录下创建`data`文件夹
    - 在`data`文件夹中创建`coat`,`shoes`,`skirt`,`trousers`四个子文件夹
    - 在这四个子文件夹中分别创建两个文件夹：`label`和`picture`
    - 在每个`label`文件夹中创建两个文件夹：`raw`和`output`

5. 使用时需要运行两个文件`main.py`和`translate_label.py`
    - `main.py`中调用的`Urls`类初始化接受两个参数，第一个是爬取类型，可选值为`['coat', 'skirt', 'shoes', 'trousers']`，第二个参数为爬取的页数，每一页大概64件商品，此值是非必需的，默认值为20(即爬取数约为1200)。`Labels`类只接受一个参数，其情况与上述第一个参数类似。
    - 运行`translate_label.py`需要修改`main`函数。一般情况下，`main`函数中只包含一条语句，如：
        ```python
        def main():
            run(coat)  # coat可更改为 shoes | skirt | trousers
        ```