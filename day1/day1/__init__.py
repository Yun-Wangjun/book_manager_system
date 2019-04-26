# 告诉Django用pymysql模块代替MySQLdb来连接MySQL数据库
import pymysql

pymysql.install_as_MySQLdb()