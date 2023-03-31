A SQL Proxy that supports differential privacy and de-identification
=====================

General introduction
=====================
DPSQL (Privacy Protection SQL Query Service) - This project is a microservice Middleware located between the database engine ( Hive , Clickhouse , etc.) and the application system. It provides transparent SQL query result desensitization capabilities. The core problem solved is the leakage of individual user privacy caused by statistical queries due to differential attacks . It is also planned to support de-identification in the future. It can be used to build privacy-by-design applications to protect personal privacy in a variety of database environments.

Architecture Overview
=====================
![arch overview](doc/img/arch_overview.png)

Main Features
==============
- Supports automated analysis of SQL queries and applies differential privacy algorithms without additional SQL transformation costs
- Compatible with multiple data sources and SQL dialects, currently supports ClickHouse and Hive , seamless and transparent access to existing systems
- For the production environment, it provides complete metadata management and privacy budget management capabilities, and optimizes query performance overhead to milliseconds
- Support for state-of-the-art differential privacy mechanisms: including Laplace, Gaussian noise, advanced composition, and noised result usability calculations（Confidence interval）
- Easy to develop and extend: Quickly extend new data source types, SQL dialects, and differential privacy algorithms

Limitation
===========
The project was spun off from an internal project and is still in its early stages. At present, there are mainly the following problems:
- The project has not been strictly tested,  has no guarantee of stability
- Limited support for database engine and SQL dialects, only Hive, Clickhouse, may not meet the needs of most people
- Limited support for SQL complexity, the part that has been open source only supports noise on query results, which is not well supported for nested queries

To Use
=======
- [Deployment Guide](doc/EN/Deployment.md)
- [Quick Start](doc/EN/QuickStart.md)
- [API Documentation](doc/EN/service_api.md)

To Develop
===========
- [Overall Design](doc/EN/Architecture.md) 
- [Metadata Management Design](doc/EN/Metadata.md)
- [Budget Management Design](doc/EN/budget_management_en.md) 
- [Differentially Private Algorithms](doc/EN/dp_algorithm_en.pdf)


Thanks
=======
This project is inspired by OpenDP, Google/Differential-Privacy, Chorus and other projects, and there are many references in implementation, these are very great projects, we have learned a lot from them, thanks to the developers of these projects.
Thanks to the members of this project, without the joint efforts of everyone, there will be no open source release of this project, and I hope to make a certain contribution to the application and promotion of privacy technology.

License
========
Apache 2.0
