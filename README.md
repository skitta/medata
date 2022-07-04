# medata - 科研信息管理系统

## 后端

- django-rest-framework

## 数据库

sqlite3 微型数据库

## 前端

* vue (iview / view-design)

## 部署

### 下载

`git clone https://github.com/skitta/medata.git`

### 安装依赖

1. python 依赖
	`pip install -r requirements.txt`
2. node 依赖
	```
	cd frontend
	npm install
	```

### 前端编译

1. 进入 `frontend` 目录
2. 修改 `src/api/**.js` 文件中的请求地址，与服务器地址保持一致
3. `npm run build`

### 后端设置

1. 进入 `medata/medata` 目录
2. 修改 `settings.py` 文件中的 `DEBUG = True` 为 `DEBUG = False`
3. 取消 `settings.py` 文件末尾关于 HTTPS 的注释
4. 在 `metata` 目录下运行 `python manage.py collectstatic`

