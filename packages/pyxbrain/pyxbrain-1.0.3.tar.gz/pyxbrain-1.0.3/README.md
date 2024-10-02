## 使用指南

使用 `pip install pyxbrain`安装，安装完成后可以在命令行使用 `xb`命令进行快捷操作。



## 打包指南

打包成 whl 文件：

```
py -m pip install --upgrade build
py -m build
```

在 `C:\Users\用户名`下的 `.pypirc`文件配置基本信息：

```
[distutils]
index-servers = pypi
[pypi]
#测试环境
repository = https://upload.pypi.org/legacy/
username = __token__
password = token
```

上传到官方：

`py -m twine upload dist/*`

## 异常处理

1. 如果输入 `xb` 时提示：“'xb' 不是内部或外部命令，也不是可运行的程序或批处理文件”。你需要把python的Scripts目录设置在环境变量下。
