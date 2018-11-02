# 图文社交平台后端: MoreMom-Moretime 后端原型系统 （(English Versio)[www.baidu.com]）
该原型系统为App的摩尔时光模块服务，其中所有配置信息均已清除，仅作为参考学习使用。

MoreMom App: http://www.moremom.com/

## 基础
#### 1. 配置
```Bash
git clone https://github.com/SixingYan/MoreTime-Backend.git
cd moretime
virtualenv --no-site-packages venv    	# 创建虚拟环境
source venv/bin/activate              	# 激活虚拟环境
mkdir logs								# 创建log文件夹
pip3 install -r requirements.txt		# 安装flask依赖包
```


#### 2. 写入具体参数
```Bash
# /moretime/ 下
vim .env

PYTHONPATH={0}/moretime 					# {0}这里改成当前位置 e.g. /var/web/moretime 测试服
FLASK_APP=api/cli.py  					# fkask run 命令
SERVER_MODE=PRODUCTION 					# 选择当前运行环境 production-生产 development-开发 

[esc]:wq
```

#### 3. 启动
```Bash
# /moretime 下
source venv/bin/activate    			# 激活虚拟环境
source .env                       		# 激活环境变量
flask run -p 8998      					# 测试上线
nohup flask run -p 8998 &   			# 永久上线 测试

deactivate    							# 退出虚拟环境
```

#### 4. 更新
```Bash
git pull                              	# 更新代码

# kill 旧的进程
# 启动
```


## 结构&功能目录

### 主要代码
- api.moretime: api转发
- usecase: 业务处理
- orm: 数据库操作
- task.qiniu_multi: 七牛批量操作 
- util.qiniu: 根据key & bucket生成可用的url

### usecase
- poster
  - \_\_init\_\_.py 里转发各种具体操作
  - 对【摩尔时光】的所有直接操作
- reply
  - \_\_init\_\_.py 里转发各种具体操作
  - 对【回复】的所有直接操作
- visible.py
  - 判断当前应使用 私有/公开/无 的多媒体
  - 更新 公开/私有
- authority.py
  - 所有权限验证操作(包含逻辑)
  - 使用关键字转发具体操作
- user.py
  - 获取头像图片等用户信息
- rate.py
  - 对评分相关的操作
- picture/video.py
  - 对多媒体文件的具体操作
  - 两者的函数内容一致，函数名称/函数排列顺序不相同
- order.py
  - 对订单信息的查询
- common.py
  - 一些通用的函数
- notif.py
  - 【预留】消息/提醒 相关的



#### 更改【摩尔时光】可见性：公开
usecase.poster.visible()
1. 更新【摩尔时光】资料  
->usecase.picture.update_to_public()  
->->usecase.visible.copy_to_public()  
->->->task.qiniu_multi.multi_copy()  
2. 更新所属【评论】资料  
->usecase.reply.visible()  
->->usecase.picture.update_to_public()  
->->->usecase.visible.copy_to_public()  
->->->->task.qiniu_multi.multi_copy()  

## 日志系统
- 配置文件：/api/logger
- 日志文件：/logs
