from utils.config.load_config import load_config
from utils.mysql_client import MysqlClient

# get mysql client
mysql_config = load_config("mysql.ini", "mysql_meta")
username = mysql_config.get("username")
password = mysql_config.get("password")
host = mysql_config.get("host")
port = mysql_config.get("port")
db_name = mysql_config.get("database")
mysql_client = MysqlClient(host=host, user=username, password=password, port=port, db_name=db_name)
