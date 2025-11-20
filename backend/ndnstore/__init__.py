# Поддержка pymysql для Windows (если mysqlclient не устанавливается)
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

