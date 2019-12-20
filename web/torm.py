
# mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, text
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import and_, or_
from datetime import datetime
engine = create_engine("mysql+mysqlconnector://root:root@10.141.221.85:3306/github?charset=utf8mb4", max_overflow=5, encoding='utf-8')

# class Base (Base):
#     __abstract__ = True
#     __table_args__ = { # 可以省掉子类的 __table_args__ 了
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8mb4'
# }
Base = declarative_base()

class RepositoryTable(Base):
    __tablename__ = 'repository_java'
    id = Column(Integer, primary_key=True, autoincrement=True)
    repository_id = Column(Integer)
    uuid = Column(String(36))
    crawl_time = Column(DateTime)
    git_address = Column(String(512))
    has_issues = Column(Boolean)
    releases_count = Column(Integer)
    stars_count = Column(Integer)
    repos_name = Column(String(255))
    owner_id = Column(Integer)
    owner_name = Column(String(255))
    updated_at = Column(DateTime)
    created_at = Column(DateTime)
    license_key = Column(String(512))
    license_name = Column(String(512))
    license_spdxld = Column(String(512))
    # description = Column(MEDIUMTEXT)
    has_wiki = Column(Boolean)
    forks_count = Column(Integer)
    is_archived = Column(Boolean)
    watchers_count = Column(Integer)
    issues_count = Column(Integer)
    primaryLanguage = Column(String(64))
    is_del = Column(Boolean)
    repos_type = Column(String(32))
    is_downloaded = Column(Boolean)
    is_issue_crawled = Column(Boolean)
    is_commit_crawled = Column(Boolean)
    is_valid = Column(Boolean)
    scan_time = Column(DateTime)
    local_addr = Column(String(512))


# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#添加角色数据
# session.add(Role(role_name='dba'))
# session.add(Role(role_name='sa'))
# session.add(Role(role_name='net'))
#
# #添加用户数据
# session.add_all([
#     User(name='fuzj',role=1),
#     User(name='jie',role=2),
#     User(name='张三',role=3),
#     User(name='李四',role=1),
#     User(name='王五',role=3),
# ])
# session.commit()
# session.close()

# ret = session.query(RepositoryTable).filter(RepositoryTable.id < 100, RepositoryTable.updated_at < "2015-01-01 00:00:00").all()

query = 'stars_count>=100 and id<=10000 or updated_at>"2019-04-01 10:00:00"' # 转换成 'stars_count>=:value1 and id<=:value2 or updated_at>:value3'
split = query.split()
per_page = 1000
page = 1
count = session.query(RepositoryTable).filter(text(query)).count()
print(count)
ret = session.query(RepositoryTable).filter(text('id <:id and updated_at <:updated_at')).params({'id':1000,'updated_at':'2015-01-01 00:00:00'}).limit(per_page).offset((page - 1) * per_page)
# query = '<var1> <sign>:<value1> <logic_sign> <var2> <sign>:<value2> ...'


# ret = session.execute('select * from repository_java where id < 100 and updated_at < "2015-01-01 00:00:00"').query(RepositoryTable)
# print(ret)
for item in ret:
    print(item.id, item.stars_count, item.repos_name, item.updated_at, type(item.updated_at))

# print(ret[0].updated_at > ret[3].updated_at)