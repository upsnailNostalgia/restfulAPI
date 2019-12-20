from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine  # 导入engine


def connect(host, port, username, password):
    HOST = '10.141.221.85'  # IP地址
    PORT = '3306'  # 端口
    DATABASE = 'github'  # 要连接的数据库
    USERNAME = 'root'  # 数据库用户
    PASSWORD = 'root'  # 数据库密码

    # 构造一个url
    db_url = 'mysql+mysqlconnector://%s:%s@%s:%s/%s?charset=utf8mb4' % (
        USERNAME,
        PASSWORD,
        HOST,
        PORT,
        DATABASE
    )

    engine = create_engine(db_url)

    return engine