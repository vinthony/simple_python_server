# simple python server

a simple blog server base on python 

#### getting start:

	cd src && ./pymonitor.py wsgiapp.py

#### online demo

	xsjcxt.sinaapp.com


#### todos:

* 分页 
* 利用git同步

## reference :
 [awesome-python-webapp](https://github.com/michaelliao/awesome-python-webapp)


## 学籍管理系统

功能： 

1. 学生【登陆】
2. 学生基本信息 【改】
3. 管理员【登陆】
4. 管理员对于获奖信息增删改查
5. 管理员【增删改查】学生

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
| award_type| boolean 1为奖励|
| award_title |  varchar(255)|
|created_at |  varchar(50)  |

## 学院表：

|类别| 信息|
|----------------|------------|
|    id    |  primary key          |
|  college_name| varchar(50)   |
|   college_id|   int        |
|created_at |  varchar(50)  |

### todo

- [ ] 把学生都改成老师
- [ ] 把增加获奖记录放到老师里面
- [ ] 增加一个统计界面
- [ ] 加上传图片功能
