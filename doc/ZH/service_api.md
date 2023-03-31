### DPSQL API文档

#### 一、接口列表

##### 1.1 DPSQL隐私查询接口

**1.1.1 隐私sql查询**

**基本信息**

**接口路径:** POST/api/v1/query

**接口描述:** 核心的加噪接口，支持不同接入数据源；输入原始查询sql，输出经过差分隐私加噪的查询结果

**协议格式：**
```json
{
        "sql": sql,
        "dbconfig": {
            "host": "xxx",
     (非必选)"port": 9000
            "database": "default",
            "reader": "clickhouse",
     (非必选)"username": xxx,
     (非必选)"password": xxx,
        },
        "queryconfig": {
            (非必选)"traceid": "query_id",
            // 仅在数据源为hive时需要设置，根据部署hive允许的认证方式设置
            (非必选)"auth": xxx
        },
        （非必选）"dpconfig": {
            （非必选）"dp_method": "Gauss" or "Laplace",
            （非必选）"budget_setting": {
                （非必选）"epsilon": 2.0,
                （非必选）"delt": 1e-5,
            }
        },
 (非必选)"extra": {
            "debug": True
        }
}
```
**参数含义：**

- sql
  - 必填
  - string
  - 原始查询语句

- dbconfig
    - 必填
    - dict
    - 数据源访问路径配置
    
      a. Host
        - 必填
        - string

        b. port
        - 选填
        - string
        
        c. database
        - 必填
        - string
        - 指定访问数据库

        d. reader
        - 必填
        - String
        - 指定访问数据源类型，如：clickhouse类型和hive类型(clickhouse、hivereader)

        e. username
        - string
        - 选填

        f. password
        - string
        - 选填

    - queryconfig
    - 必填
    - dict
    - 查询配置项，支持附加功能

        a. traceid
        - string
        - 选填
        - 方便追踪完整执行链路

        b. auth
        - string
        - 选填
        - 连接数据源为hive时指定连接认证方式
    - dpconfig
        - 选填
        - dict
        - 设置加噪机制和为每个结果添加的隐私预算
    
        a. dp\_method
        - 选填
        - string（默认值为拉普拉斯机制）
        - 设置加噪机制(拉普拉斯机制，高斯机制)
        
        b. budget\_setting
        - 选填
        - 为每个结果添加的隐私预算
            
            i. epsilon
            - 选填
            - float（默认值为0.9）
            - 为每个结果添加的隐私预算
            
            ii. delt
            - 选填
            - float（对于拉普拉斯机制，始终为0；对于高斯机制，默认值为1e-8）
            - (epsilon,delt)-DP的第二个参数
    - Extra
      - 选填
      - dict
      - 支持额外参数配置

        a. debug
        - bool
        - 选填
        - 是否开启debug，展示debug信息

**响应**

**Body:**

1.成功
```json
{
    'status': {
        'code': 0,
        'Message': 'ok'
    },
    'ServerInfo': {
        'TimeZone': 'CST'
    },
    'Meta': [
        {
            'Name': ,
            'Type': 
        }
    ],
    'Data': {
        'col_name': [
            x,x,x,x,
        ]
    },
    'dp_info': {
        'privacy': ,
        'utility': [
            
        ]
    }
}
```
2.失败

```json
{
    "status": {
        "code": 1,
        "Message": xxx
    }
}
```
**使用示例**

1.Cliskhouse数据源访问
```python
def test_http_query():
    url = 'http://127.0.0.1:5000/api/v1/query'
    sql = 'select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20'
    key = {
        "sql": sql,
        "dbconfig": {
            "host": "",
            "database": "",
            "reader": "clickhouse",
        },
        "queryconfig": {
            "traceid": "query_id",
        },
        "dpconfig": {
            "dp_method": "Gauss",
            "budget_setting": {
                "epsilon": 2.0,
                "delt": 1e-5,
             }
        },
        "extra": {
            "debug": True        }
    }
    headers = {"content-type": "application/json"}
    r = requests.post(url, json=key, headers=headers)
    return r
```

2.hive数据源访问
```python
def test_http_query():
    url = 'http://127.0.0.1:5000/api/v1/query'
    sql = 'select gender, sum(age) as total_age from user_info group by gender'
    key = {
        "sql": sql,
        "dbconfig": {
            "host": "",
            "database": "",
            "reader": "hivereader",
        },
        "queryconfig": {
            "traceid": "query_id",
        },
        "dpconfig": {
            "dp_method": "Gauss",
            "budget_setting": {
                "epsilon": 2.0,
                "delt": 1e-5,
             }
        },
        "extra": {
            "debug": True        }
    }
    headers = {"content-type": "application/json"}
    r = requests.post(url, json=key, headers=headers)
    return r
```
#####1.2 MetaData相关接口

**1.2.1 更新metadata**

**基本信息**

**接口路径:** PUT /api/v1/metadata/update

**接口描述:** 重新提取metadata并更新metadata信息

**请求参数**

协议格式：
```json
{
    "table_name": table_name,
    "db_type": db_type,
    "db_config": {
        "host": xxx,
        "database": xxx,
        "username": xxx,
        "password": xxx
    }
}
```
参数含义：

- table\_name
    - 必填
    - string
    - 表名
- db\_type
    - 必填
    - string
    - 数据库类型: clickhouse/hive
- db\_config
    - 必填
    - dict
    - 数据源访问路径配置

    a. host
    - 必填
    - string
    - 数据源host
    
    b. database
    - 必填
    - string
    - 指定访问数据库
    
    c. username
    - string
    - 选填

    d. password
    - string
    - 选填

**响应**

**Body:**

1.成功

```json
{
  "return_msg": "Updated successfully",
  "status_code": 0
}
```

2.失败
```json
{
  "return_msg": "XXX",
  "status_code": -1
}
```
使用示例
```python
def test_http_query():
    url = 'http://127.0.0.1:5000/api/v1/query'
    sql = 'select count(menu_id), sum(page_number) as sum_val from menu_page group by menu_id limit 20'
    key = {
        "sql": sql,
        "dbconfig": {
            "host": "",
            "database": "",
            "reader": "clickhouse",
        },
        "queryconfig": {
            "traceid": "query_id",
        },
        "dpconfig": {
            "dp_method": "Gauss",
            "budget_setting": {
                "epsilon": 2.0,
                "delt": 1e-5,
             }
        },
        "extra": {
            "debug": True        }
    }
    headers = {"content-type": "application/json"}
    r = requests.post(url, json=key, headers=headers)
    return r
```

**1.2.2 查询metadata**

**基本信息**

**接口路径:** GET  /api/v1/metadata/get

**接口描述:** 查询metadata信息

**请求参数**

协议格式：
```json
{
    "prefix": prefix,
    "db_name": db_name,
    "table_name": table_name
}
```
参数含义：

- prefix
    - 必填
    - string
    - 前缀信息：db\_host信息
- db\_name
    - 必填
    - string
    - 数据库名
- table\_name
    - 必填
    - string
    - 表名

**返回数据**

**Body:**

1.成功

```json
{
  "data": {
    "database": "default",
    "engine": "clickhouse",
    "tables": [
      {
        "columns": {
          "highest_price": {
            "clipping_flag": 1,
            "clipping_lower": "65.000",
            "clipping_upper": "15.000",
            "lower": "0",
            "type": "Decimal(18, 3)",
            "upper": "3050"
          },
          "id": {
            "clipping_flag": 1,
            "clipping_lower": "65.000",
            "clipping_upper": "15.000",
            "lower": "1",
            "max_fre": "1",
            "type": "UInt32",
            "upper": "520799"
          },
          ......
        },
        "tablename": "dish"
      }
    ]
  },
  "return_msg": "Query succeeded",
  "status_code": 0
}
```
2.失败

```json
{
  "return_msg": "XXX",
  "status_code": -1
}
```
使用示例
```python
def test_meta_query():
    url = 'http://127.0.0.1:5000/api/v1/metadata/get'
    key = {
        "prefix": "",
        "db_name": "",
        "table_name": ""
    }
    headers = {"content-type": "application/json"}
    r = requests.get(url, json=key, headers=headers)
    print(r.text)
```

**1.2.3 提取metadata**

**基本信息**

**接口路径:** POST /api/v1/metadata/extract

**接口描述:** metadata 提取功能

**请求参数**

协议格式：
```json
{
    "table_name": table_name,
    "db_type": db_type,
    "db_config": {
        "host": xxx,
        "database": xxx,
        "username": xxx,
        "password": xxx
    }
}
```
参数含义：

- table\_name
    - 必填
    - string
    - 表名
- db\_type
    - 必填
    - string
    - 数据库类型: clickhouse/hive
- db\_config
    - 必填
    - dict
    - 数据源访问路径配置
    
    a. host
    - 必填
    - string
    - 数据源host

    b. database
    - 必填
    - string
    - 指定访问数据库

    c. username
    - string
    - 选填
    
    d. password
    - string
    - 选填

响应

**Body:**

1.成功
```json
{
  "data": {
    "database": "default",
    "engine": "hive",
    "tables": [
      {
        "columns": {
          "age": {
            "lower": 1,
            "max_fre": 16,
            "type": "INT",
            "upper": 120
          },
          "country_code": {
            "type": "STRING"
          },
          "email": {
            "type": "STRING"
          },
          "first_name": {
            "type": "STRING"
          },
          "gender": {
            "lower": 1,
            "max_fre": 514,
            "type": "INT",
            "upper": 2
          },
          "id": {
            "lower": 1,
            "max_fre": 1,
            "type": "BIGINT",
            "upper": 1000
          },
          "last_name": {
            "type": "STRING"
          },
          "mobile": {
            "type": "STRING"
          },
          "non_pii_value": {
            "type": "STRING"
          }
        },
        "tablename": "user_info"
      }
    ]
  },
  "return_msg": "extracted successfully",
  "status_code": 0
}
```
2.失败
```json
{
  "return_msg": "XXX",
  "status_code": -1
}
```
使用示例
```python
def test_metadata_extract():
     url = 'http://127.0.0.1:5000/api/v1/metadata/extract'
     table_name = "dish"
     db_type = "clickhouse"
     db_config = {
         "host": "",
         "database": "",
         "username": "",
         "password": ""
    }
    db_type = "clickhouse"
    headers = {"content-type": "application/json"}
    r = requests.post(url, json=key, headers=headers)
    print(r.text)
```

**1.2.4 生成metadata**

**基本信息**

**接口路径:** POST /api/v1/metadata/generate

**接口描述:** 用于生成metadata，包括提取原始表的metadata，并将其存储到MYSQL中；

**请求参数**

协议格式：
```json
{
    "table_name": table_name,
    "db_type": db_type,
    "db_config": {
        "host": xxx,
        "database": xxx,
        "username": xxx,
        "password": xxx
    }
}
```
参数含义：

- table\_name
    - 必填
    - string
    - 表名
- db\_type
    - 必填
    - string
    - 数据库类型: clickhouse/hive
- db\_config
    - 必填
    - dict
    - 数据源访问路径配置
    
    a. host
    - 必填
    - string
    - 数据源host

    b. database
    - 必填
    - string
    - 指定访问数据库

    c. username
    - string
    - 选填

    d. password
    - string
    - 选填

响应

**Body:**

1.成功
```json
{
  "return_msg": "Generated successfully",
  "status_code": 0
}
```
2.失败
```json
{
  "return_msg": "XXX",
  "status_code": -1
}
```
使用示例
```python
def test_metadata_generate():
     url = 'http://127.0.0.1:5000/api/v1/metadata/generate'
     table_name = "dish"
     db_type = "clickhouse"
     db_config = {
         "host": "",
         "database": "",
         "username": "",
         "password": ""
    }
    db_type = "clickhouse"
    headers = {"content-type": "application/json"}
    r = requests.post(url, json=key, headers=headers)
    print(r.text)
```

**1.2.5 删除metadata**

**基本信息**

**接口路径:** DELETE /api/v1/metadata/delete

**接口描述:** 删除metadata

**请求参数**

协议格式：
```json
{
    "prefix": prefix,
    "db_name": db_name,
    "table_name": table_name
}
```
参数含义：

- prefix
    - 必填
    - string
    - 前缀信息：db\_host信息
- db\_name
    - 必填
    - string
    - 数据库名
- table\_name
    - 必填
    - string
    - 表名

**返回数据**

**Body:**

1.成功
```json
{
    "status_code": 0, 
    "return_msg": "Deleted successfully"
}
```
2.失败
```json
{
    "status_code": -1, 
    "return_msg": "XXX"
}
```
使用示例
```python
def test_meta_delete():
    url = 'http://127.0.0.1:5000/api/v1/metadata/delete'
    key = {
        "prefix": "",
        "db_name": "",
        "table_name": ""
    }
    headers = {"content-type": "application/json"}
    r = requests.delete(url, json=key, headers=headers)
    print(r.text)
```

**1.2.6 设置Clipping**

**基本信息**

**接口路径:** PUT  /api/v1/metadata/get

**接口描述:  为单个column设置Clipping信息**

**请求参数**

协议格式：

```json
{
    "prefix": prefix,
    "db_name": db_name,
    "table_name": table_name,
    "column_name": column_name,
    "clipping_info": {
        "clipping_flag": x,
        "clipping_upper": xxx,
        "clipping_lower": xxx
    }
}
```
参数含义：

- prefix
    - 必填
    - string
    - 前缀信息：db\_host信息
- db\_name
    - 必填
    - string
    - 数据库名
- table\_name
    - 必填
    - string
    - 表名
- column\_name
    - 必填
    - string
    - 字段名
- clipping\_info
    - 必填
    - dict
    - clipping信息
        - clipping\_flag： 该字段是否开启Clipping， 1：开启； 0: 禁用
        - clipping\_upper：Clipping 取值上界
        - clipping\_lower：Clipping 取值下界

**返回数据**

**Body:**

1.成功
```json
{
    "status_code": 0, 
    "return_msg": "set successfully"
}
```
2.失败
```json
{
    "status_code": -1, 
    "return_msg": "xxx"
}
```
使用示例
```python
def set_clipping():
    url = 'http://127.0.0.1:5000/api/v1/metadata/set_clipping'
    key = {
        "prefix": "",
        "db_name": "",
        "table_name": "",
        "column_name": "",
        "clipping_info": {
            "clipping_flag": 1,
            "clipping_upper": 15,
            "clipping_lower": 65
        }
    }
    headers = {"content-type": "application/json"}
    r = requests.get(url, json=key, headers=headers)
    print(r.text)
```
**1.3 Budget相关接口**

**1.3.1 查询budget信息**

**基本信息**

**接口路径:** GET  /api/v1/budget/get

**接口描述:** 查询budget信息

**请求参数**

协议格式：
```json
{
    "prefix": prefix,
    "db_name": db_name,
    "table_name": table_name
}
```
参数含义：

- prefix
    - 必填
    - string
    - 前缀信息：db\_host信息
- db\_name
    - 必填
    - string
    - 数据库名
- table\_name
    - 必填
    - string
    - 表名

**返回数据**

**Body:**

1.成功
```json
// 查询成功
{
     status:{
            "code": 200,
            "Message": "succeed",
            "data": {
                "prefix"：string，
                "db_name"：string，
                "table_name": string,
                "total_budget": float,
                "residual_budget": float,
                ...
            }
     }
}
```
2.失败
```json
{
  status:{
        "code": 1,
        "Message": xxxx
    }
}
```
使用示例
```python
def test_budget_get():
    url = 'http://127.0.0.1:5000/api/v1/budget/get'
    key = {
        "prefix": "",
        "db_name": "",
        "table_name": ""
    }
    headers = {"content-type": "application/json"}
    r = requests.get(url, json=key, headers=headers)
    print(r.text)
```
**1.3.2 设置/更新budget信息**

**基本信息**

**接口路径: POST** /api/v1/budget/set

**接口描述: 设置或更新budget信息**

**请求参数**

协议格式：
```json
{
    "prefix": xxx,
    "db_name": xxx,
    "table_name": xxx,
    "total_budget": xxx,
    "recover_cycle": xx,
    "exhausted_strategy": xxxx,
}
```
参数含义：

- prefix
    - 必填
    - string
    - 前缀信息：db\_host信息
- db\_name
    - 必填
    - string
    - 数据库名
- table\_name
    - 必填
    - string
    - 表名
- total\_budget
    - 可选，默认值为10000.0
    - float
    - 总体的隐私预算
- recover\_cycle
    - 可选，默认值为30
    - int
    - 隐私预算恢复策略
- exhausted\_strategy
    - 可选，默认值为“reject”
    - string，“reject”  or “allow”
    - 隐私预算耗尽时策略

**响应**

**Body:**

1.成功
```json
// 查询成功
{
    status:{
        "code": 200,
        "Message": "succeed"
    }
}
```
2.失败
```json
{
  status:{
        "code": 1,
        "Message": xxx
    }
}
```
使用示例
```python
def test_budget_set():
    url = 'http://127.0.0.1:5000/api/v1/budget/set'
    key = {
    "prefix": "1.1.1.3",
    "db_name": "test_db_1",
    "table_name": "test_table_2",
    "total_budget": 77777.0,
    "recover_cycle": 88,
    "exhausted_strategy": "reject",
    }
    headers = {"content-type": "application/json"}
    r = requests.post(url, json=key, headers=headers)
    print(r.text)
```