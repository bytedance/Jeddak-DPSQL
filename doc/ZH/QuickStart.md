- 导入公开的数据集
  - 下载公开的数据集, 数据集地址：[US Accidents](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents?resource=download)
  - 建立表结构
  ```mysql
    create table if not exists us_accidents_dec21_updated
      (
          id                    string,
          severity              int,
          start_time            string,
          end_time              string,
          start_lat             double,
          start_lng             double,
          end_lat               double,
          end_lng               double,
          distance              double comment 'mi',
          description           string,
          number                double,
          street                string,
          side                  string,
          city                  string,
          county                string,
          state                 string,
          zipcode               string,
          country               string,
          timezone              string,
          airport_code          string,
          weather_timestamp     string,
          temperature           double comment 'f',
          wind_chill            double comment 'f',
          humidity              double comment '%',
          pressure              double comment 'in',
          visibility            double comment 'mi',
          wind_direction        string,
          wind_speed            double comment 'mph',
          precipitation         double comment 'in',
          weather_condition     string,
          amenity               string,
          bump                  string,
          crossing              string,
          give_way              string,
          junction              string,
          no_exit               string,
          railway               string,
          roundabout            string,
          station               string,
          stop                  string,
          traffic_calming       string,
          traffic_signal        string,
          turning_loop          string,
          sunrise_sunset        string,
          civil_twilight        string,
          nautical_twilight     string,
          astronomical_twilight string
      )
          row format serde 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
          stored as
              inputformat 'org.apache.hadoop.mapred.TextInputFormat'
              outputformat 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
          location 'hdfs://namenode:8020/user/hive/warehouse/us_accidents_dec21_updated';
  ```
  - 导入数据集
  ```shell
    ##<csv_path> is the hdfs path of dataset us_accidents_dec21_updated.csv
    load data local inpath <csv_path> into table us_accidents_dec21_updated;
    ```
- 初始化metadata和隐私预算
      
  - 生成 metadata
      
      启动dpsql服务后， 调用接口 `/api/v1/metadata/generate`，生成metadata，可参考下面的python脚本：
         
    ```python
    def meta_generate():
      args = {
          "db_config": {
              "host": <hive_host>,
              "database": <hive_dbname>,
              "username": <hive_username>,
              "password": <hive_password>
          },
          "table_name": "us_accidents_dec21_updated",
          "db_type": db_type
      }
      route_path = "/api/v1/metadata/generate"
      # local service,  host:127.0.0.1, port:5000
      url = "http://%s:%s/%s" % (host, port, route_path)
      headers = {"content-type": "application/json"}
      r = requests.post(url, json=args, headers=headers)
    
    if __name__ == '__main__':
       meta_generate()```
        
  - 确认metadata 生成完成
        
       调用 `/api/v1/metadata/get` 接口，确认 metadata 生成完成
    ```python
    def meta_get():
        args = {
            "prefix": <hive_host>,
            "db_name": <hive_dbname>,
            "table_name": "us_accidents_dec21_updated"
        }
        route_path = "/api/v1/metadata/get"
        # local service,  host:127.0.0.1, port:5000
        url = "http://%s:%s/%s" % (host, port, route_path)
        headers = {"content-type": "application/json"}
        r =  requests.get(url, json=args, headers=headers)
        print(r.text)```
    
- Dpsql查询
  ```python
    def query_sql_noise(sql, data_source):
        key = {
            "sql": sql,
            "dbconfig": {
                "reader": data_source,
                "host": <hive_host>,
                "database": <hive_dbname>,
                "port": <hive_port>
            },
            "queryconfig": {
               "traceid": "traceid",
            }
        }
        route_path = "/api/v1/query"
        url = "http://%s:%s/%s" % (host, port, route_path)
        headers = {"content-type": "application/json"}
        r = requests.post(url, json=key, headers=headers)
        return res
    
    
    if __name__ == "__main__":
        sql = "select count(severityc) from menu_page group by severity"
        section = "hivereader"
        res = query_sql_noise(sql, section)
        print(res)```