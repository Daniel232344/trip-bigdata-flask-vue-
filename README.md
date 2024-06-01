# 配置流程

## 创建环境

打开项目目录

在anaconda-prompt终端输入

```
conda env create -f environment.yml
```

在pycharm中file->settings->project->interpreter将flask-env作为项目环境

## 启动vue

新建终端

```
cd trip-vue
set NODE_OPTIONS=--openssl-legacy-provider
npm run serve
```

## 启动flask

新建终端

```
cd trip-python
python app.py
```

## 打开网址

http://localhost:8080