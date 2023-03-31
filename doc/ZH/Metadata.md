元数据管理模块设计
=======

背景
-------------
在DPSQL系统中，需要提取 metadata 的信息进行 sql 的重写和敏感度的分析。


目标
-------------
- 持久化存储元数据
- 对常用表的元数据查询增加缓存，提升动态读取的性能开销
- 提供元信息的 CURD API
- 支持自动提取元数据信息


总体方案
-------------
![arch overview](../img/meta_overview.png)
- 整体架构说明
  - Metadata generator，元数据信息生成器，给定数据源配置信息和表名，自动提取该表的元数据信息，并存入metadata store;
  - Metadata store，中心化存储;
  - 设立 meta matcher 对象，每条查询独立创建，负责根据 prefix、db、table、column 等信息从Metadata store 中查询匹配对应的 meta 信息； 不同的数据源对应不同的metamatcher，处理差异性;
  - Metadata 信息主要包括：数据库名、表名、列名、列的数据类型、map 类型列的key、value 类型，数值类型的 最大值、最小值等信息
  - 在执行查询时性能非常敏感，通过 Mysql 查询和加载metadata 是非常大的一个瓶颈，因此在 Mysql 之前增加了两层缓存，内存缓存和基于 kv 存储的缓存。

- 关于数据库类型转换
  - DPSQL 使用 python 实现，对于基本数据类型只区分到 （int、float、string、datatime) ，但是数据库的基本数据类型是比较丰富的，比如 clickhouse，int 有 int32/int64/uint32/uin64 等；另外还有 内置函数返回值类型，算术运算类型推导问题。为了兼容多种数据库类型系统，以及能够得到准确的查询结果的类型，需要将 数据库类型 dbtype 转换为 DPSQL 内部类型 type。
  - DB type converter 模块，在从metadata store加载 metadata 信息时，协助其将数据库类型名转换为 DPSQL 内部处理的类型名（如 uint32 -> int)；AST 从 database metadata 对象获取 dbtype converter，在做类型推导时可以获得数据库相关的结果。

