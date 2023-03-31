Overall architecture
====================
![arch overview](../img/arch_overview.png)

Module description
==================

Http_service
------------
- Provide HTTP  API，including: sql query API、metadata management API、privacy budget management API
Query Driver
- QueryDriver is responsible for driving other modules to complete SQL execution of the overall logic
- Create a separate QueryDriver object and QueryContext object for each query request, maintain the context independently, and maintain isolation

Parser
-------
- Define a unified AST structure designed for differential privacy 
- Mapping multiple input dialects into the unified AST
- Convert AST to SQL  string for each dialect
- Provides traversal, rewrite APIs for AST

Analysis
--------
- Basic information extraction, database name, table name, join information, etc
- Provide differential privacy policy, whether it can be supported, noise method (result based, rewrite based)

Metadata Management
-------------------
- Metadata  Storage and CRUD  API
- Metadata high-performance queries, multi-level caching
- Metadata Automated Extraction from the database

DP 
------
- Aggregate function noise processing logic
- Clipping logic, etc.
- Sensitivity calculation local/smooth/elastic
- Noise addition algorithm
-  Usability Calculation of Noised Results

Privacy Budget Management
-------------------------
- Storage and CRUD API
- Maintain privacy budget per data table
- Record privacy budget consumption per query

DBAccess
---------
- Support various types of data source access
- Provide a unified query interface
- Provides a unified abstraction of query results

SQL Process flow
================
![main process](../img/main_process.png)