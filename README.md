# 教师奖励管理系统

a simple student manager server base on python 

#### getting start:

	cd src && ./pymonitor.py wsgiapp.py

#### online demo

[sae-xsjcxt.sinaapp.com](xsjcxt.sinaapp.com)
	
登录账号：000000
密码：000000

#### todos:

* 分页 
* 利用git同步

## reference :
 [awesome-python-webapp](https://github.com/michaelliao/awesome-python-webapp)


## USER表:

|类别| 信息|
|----------------|------------|
|      id(varchar(50))        |   primary key |
|      name       |   varchar(50)    |
|      sno			|  int(10)       |
|      password     |   varchar(50)  |
|      email        |   varchar(50)  |
|      identify        |   1/0 (boolean) |
|      year        |    int(4)      |
|      college      |    int(2)      |
|     created_at    |   varchar(50) |


## award表：

|类别| 信息|
|----------------|------------|
|    id    |  primary key          |
|   award_content|   text        |
|   award_user_id|    varchar(50)     |
| award_is_show|       boolean|
| award_year|       int(4)|
| award_type| boolean (级别，分为校级123，市级123，省级123) |
| award_title |  varchar(255)|
|created_at |  varchar(50)  |
| image| varchar(500) |
## 学院表：

|类别| 信息|
|----------------|------------|
|    id    |  primary key          |
|  college_name| varchar(50)   |
|   college_id|   int        |
|created_at |  varchar(50)  |

### todo

- [x] 把学生都改成老师
- [x] 把增加获奖记录放到老师里面
- [x] 增加一个统计界面[统计每年获奖情况]
- [x] 加上传图片功能



# 模块解析

采用MVC架构：

* Model ---- 定义数据模型,使得调用更加方便
* View ---- 定义前端模板,使用jinja2来进行注入
* Controller --- 逻辑控制和路由

### static 目录

* 为静态目录，保存前端静态资源，css，javascript
* 前端模块使用bootstrap,统计表格使用echarts

### templates 目录/View

* 为html模板目录，保存view中所有的模板

### transwarp 目录 -- 一个简洁的web框架

* `db.py` 数据库连接模块，封装数据库底层事务，向orm提供简洁的API
* `orm.py` ORM模块，定义数据库文件查询所需的字段，为Models层提供支持。
* `web.py` 服务器模块，封装了一个简单地HTTP服务器
* `colorlog.py` 为了更方便的调试

### upload 目录 
* 为上传的图片所存得目录

### apis.py 
* 定义@api装饰器,使返回值变成json格式

### config.py
* 保存服务器配置和数据库配置信息

### models.py/Model
* 定义`User`,`Awards`,`College`三个模型
* 模型内容与数据库表配置相同

### wsgiapp.py

* 初始化数据库
* 初始化前端模板
* 初始化服务器

## pymonitor.py 帮助类

* 自动监听代码改动，如有改动重新启动服务器。

## urls.py 主要的route入口/Controller

主要函数解析：

* `index()` 定义主页内容
* `user_interceptor()` 一个检测器，来判断用户是否登录
* `register_user()` 注册用户
* `authenticate()` 登陆函数
* `checkuser()` API,判断用户是否合法
* `getloginName()` 获得登录之后的名字
* `search()` 查询学生
* `search_student()` API，用来异步查询学生
* `awardlist()` 获奖情况列表
* `search_award()` API,异步查询奖励
* `addstudent()`增加学生页初始化数据
* `add_student()` API，异步提交增加学生数据
* `addaward()` 增加奖项页面初始化
* `add_award()` 增加奖项异步提交
* `myinfomation()` 个人页面初始化
* `award_id()` 奖励内容页面内容初始化
* `modifypassword()` 修改密码
* `summary()` 总结年度奖项页面
* `delete()` 删除用户
* `delete_award()` 删除奖项
* `modifyaward()` 更改奖项初始化
* `modifyawardecho()` 异步提交更改奖项
* `modifyuser()` 更改用户初始化
* `modifyuserecho()` 异步提交更改用户




