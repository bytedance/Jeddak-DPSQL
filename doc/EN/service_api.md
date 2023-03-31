### DPSQL API Documentation

#### 一、Interface List

##### 1.1 DPSQL privacy query interface

**1.1.1 Privacy sql query**

**Basic Information**

**interface path:** POST/api/v1/query

**interface description:** The core noise addition interface supports different access data sources; input the original query sql, and output the query results after differential privacy noise addition.

**protocol format：**
```json
{
        "sql": sql,
        "dbconfig": {
            "host": "xxx",
     (Optional)"port": 9000
            "database": "default",
            "reader": "clickhouse",
     (Optional)"username": xxx,
     (Optional)"password": xxx,
        },
        "queryconfig": {
            (Optional)"traceid": "query_id",
            // Only need to be set when the data source is hive, set according to the authentication method allowed by deploying hive
            (Optional)"auth": xxx
        },
        （Optional）"dpconfig": {
            （Optional）"dp_method": "Gauss" or "Laplace",
            （Optional）"budget_setting": {
                （Optional）"epsilon": 2.0,
                （Optional）"delt": 1e-5,
            }
        },
 (Optional)"extra": {
            "debug": True
        }
}
```
**Parameter meaning：**

- sql
  - required
  - string
  - Raw query statement

- dbconfig
    - required
    - dict
    - Data source access path configuration
    
      a. Host
        - required
        - string

        b. port
        - optional
        - string
        
        c. database
        - required
        - string
        - specify access database

        d. reader
        - required
        - String
        - Specify the access data source type, such as: clickhouse type and hive type (clickhouse, hivereader)

        e. username
        - string
        - optional

        f. password
        - string
        - optional

    - queryconfig
    - required
    - dict
    - Query configuration items, support additional functions

        a. traceid
        - string
        - optional
        - Easy to track the complete execution link

        b. auth
        - string
        - optional
        - Specify the connection authentication method when the connection data source is hive
    - dpconfig
        - optional
        - dict
        - set the dp mechanism and the privacy budget for each answer
    
        a. dp\_method
        - optional
        - string（default = "Laplace"）
        - set the dp mechanism(Laplace or Gauss)
        
        b. budget\_setting
        - optional
        - set the privacy budget for each answer 
            
            i. epsilon
            - optional
            - float（default = 0.9）
            - set the privacy budget for each answer 
            
            ii. delt
            - optional
            - float（always 0 for Laplace; default = 1e-8 for Gauss）
            - the second parameter for (epsilon, delt)-DP 
    - Extra
      - optional
      - dict
      -   - Support additional parameter configuration

        a. debug
        - bool
        - optional
        - Whether to enable debug, display debug information

**response**

**Body:**

1.success
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
2.fail

```json
{
    "status": {
        "code": 1,
        "Message": xxx
    }
}
```
**Example**

1.Cliskhouse data source access
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

2.Hive data source access
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
##### 1.2 MetaData related interface

**1.2.1 Update metadata**

**Basic Information**

**interface path:** PUT /api/v1/metadata/update

**interface description:** Re-extract metadata and update metadata

**request parameters**

protocol format：
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
Parameter meaning：

- table\_name
    - required
    - string
    - table name
- db\_type
    - required
    - string
    - Database type: clickhouse/hive
- db\_config
    - required
    - dict
    - Data source access path configuration

    a. host
    - required
    - string
    - Data source host
    
    b. database
    - required
    - string
    - specify access database
    
    c. username
    - string
    - optional

    d. password
    - string
    - optional

**response**

**Body:**

1.success

```json
{
  "return_msg": "Updated successfully",
  "status_code": 0
}
```

2.fail
```json
{
  "return_msg": "XXX",
  "status_code": -1
}
```
Example
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

**1.2.2 Query metadata**

**Basic Information**

**interface path:** GET  /api/v1/metadata/get

**interface description:** query metadata information

**request parameters**

protocol format：
```json
{
    "prefix": prefix,
    "db_name": db_name,
    "table_name": table_name
}
```
Parameter meaning：

- prefix
    - required
    - string
    - Prefix information：the host of database
- db\_name
    - required
    - string
    - database name
- table\_name
    - required
    - string
    - table name

**Response**

**Body:**

1.success

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
2.fail

```json
{
  "return_msg": "XXX",
  "status_code": -1
}
```
Example
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

**1.2.3 Extract metadata**

**Basic Information**

**interface path:** POST /api/v1/metadata/extract

**interface description:** metadata extraction function

**request parameters**

protocol format：
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
Parameter meaning：

- table\_name
    - required
    - string
    - table name
- db\_type
    - required
    - string
    - Database type: clickhouse/hive
- db\_config
    - required
    - dict
    - Data source access path configuration
    
    a. host
    - required
    - string
    - data source host

    b. database
    - required
    - string
    - specify access database

    c. username
    - string
    - optional
    
    d. password
    - string
    - optional

response

**Body:**

1.success
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
2.fail
```json
{
  "return_msg": "XXX",
  "status_code": -1
}
```
Example
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

**1.2.4 Generate metadata**

**Basic Information**

**interface path:** POST /api/v1/metadata/generate

**interface description:** used to generate metadata , including extracting the metadata of the original table and storing it in the MYSQL;

**request parameters**

protocol format：
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
Parameter meaning：

- table\_name
    - required
    - string
    - table name
- db\_type
    - required
    - string
    - Database type: clickhouse/hive
- db\_config
    - required
    - dict
    - Data source access path configuration
    
    a. host
    - required
    - string
    - data source host

    b. database
    - required
    - string
    - specify access database

    c. username
    - string
    - optional

    d. password
    - string
    - optional

response

**Body:**

1.success
```json
{
  "return_msg": "Generated successfully",
  "status_code": 0
}
```
2.fail
```json
{
  "return_msg": "XXX",
  "status_code": -1
}
```
Example
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

**1.2.5 Delete metadata**

**Basic Information**

**interface path:** DELETE /api/v1/metadata/delete

**interface description:**  delete metadata

**request parameters**

protocol format：
```json
{
    "prefix": prefix,
    "db_name": db_name,
    "table_name": table_name
}
```
Parameter meaning：

- prefix
    - required
    - string
    - Prefix information：db\_host information
- db\_name
    - required
    - string
    - database name
- table\_name
    - required
    - string
    - table name

**Response**

**Body:**

1.success
```json
{
    "status_code": 0, 
    "return_msg": "Deleted successfully"
}
```
2.fail
```json
{
    "status_code": -1, 
    "return_msg": "XXX"
}
```
Example
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

**1.2.6 Setting Clipping**

**Basic Information**

**interface path:** PUT  /api/v1/metadata/get

**interface description:  Set Clipping information for a single column**

**request parameters**

protocol format：

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
Parameter meaning：

- prefix
    - required
    - string
    - Prefix information：db\_host information
- db\_name
    - required
    - string
    - database name
- table\_name
    - required
    - string
    - table name
- column\_name
    - required
    - string
    - field name
- clipping\_info
    - required
    - dict
    - clipping information
        - clipping\_flag： whether the field Clipping, 1: open; 0: disabled
        - clipping\_upper：Clipping upper bound
        - clipping\_lower：Clipping lower bound

**Response**

**Body:**

1.success
```json
{
    "status_code": 0, 
    "return_msg": "set successfully"
}
```
2.fail
```json
{
    "status_code": -1, 
    "return_msg": "xxx"
}
```
Example
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
**1.3 Interfaces about Budget**

**1.3.1 Query budget**

**Basic Information**

**interface path:** GET  /api/v1/budget/get

**interface description:** query budget information

**request parameters**

protocol format：
```json
{
    "prefix": prefix,
    "db_name": db_name,
    "table_name": table_name
}
```
Parameter meaning：

- prefix
    - required
    - string
    - Prefix information：db\_host information
- db\_name
    - required
    - string
    - database name
- table\_name
    - required
    - string
    - table name

**Response**

**Body:**

1.success
```json

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
2.fail
```json
{
  status:{
        "code": 1,
        "Message": xxxx
    }
}
```
Example
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
**1.3.2 Set/Update budget information**

**Basic Information**

**interface path: POST** /api/v1/budget/set

**interface description: set or update budget information**

**request parameters**

protocol format：
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
Parameter meaning：

- prefix
    - required
    - string
    - Prefix information：db\_host information
- db\_name
    - required
    - string
    - database name
- table\_name
    - required
    - string
    - table name
- total\_budget
    - Optimal, default=10000.0
    - float
    - total privacy budget
- recover\_cycle
    - Optimal, default=30
    - int
    - The interval days between two adjacent budget recovery
- exhausted\_strategy
    - Optimal, default="reject"
    - string，“reject”  or “allow”
    - Policies when privacy budgets run out

**response**

**Body:**

1.success
```json

{
    status:{
        "code": 200,
        "Message": "succeed"
    }
}
```
2.fail
```json
{
  status:{
        "code": 1,
        "Message": xxx
    }
}
```
Example
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