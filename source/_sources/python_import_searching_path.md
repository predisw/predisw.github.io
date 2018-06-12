### python import searching path

1. 程序运行的当前目录
2. PYTHONPATH 环境变量的目录
3. 标准链接库的目录
4. 任何.pth 中的文件内容

import 搜索路径默认按照上面的顺序

import 只会选择在搜索时遇到第一个匹配的文件导入

对于.pth 文件只能放在标准库所在位置sitepackages 子目录中，这个目录可以通过如下命令获取:
```
>>> import site;
>>> site.getsitepackages()
['/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages']
```


可以使用 **import sys;sys.path**   来查看当前 import 时搜索的路径
```
# env setting
export PROJ_HOME=/home/predisw/proj
export PYTHON_LEARNING_HOME=/home/predisw/proj/predisw-baseline/practice-test/python-learning/src/main/python
export PYTHONPATH=$PROJ_HOME/forOne/extractData:$PYTHON_LEARNING_HOME

# .pth setting
cat /usr/local/lib/python2.7/dist-packages/practice.pth 
/home/predisw/proj/predisw-baseline/practice-test/python-learning/src/main/python/predisw/moduleT

# check import searching path
>>> import sys
>>> sys.path
['', '/home/predisw/proj/forOne/extractData', '/home/predisw/proj/predisw-baseline/practice-test/python-learning/src/main/python', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-x86_64-linux-gnu', '/usr/lib/python2.7/lib-tk', '/usr/lib/python2.7/lib-old', '/usr/lib/python2.7/lib-dynload', '/usr/local/lib/python2.7/dist-packages', '/usr/local/lib/python2.7/dist-packages/setuptools-28.8.0-py2.7.egg', '/home/predisw/proj/predisw-baseline/practice-test/python-learning/src/main/python/predisw/moduleT', '/usr/lib/python2.7/dist-packages']
```

其中'' 空字符串表示当前工作目录