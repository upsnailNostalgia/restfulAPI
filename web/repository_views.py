from flask import jsonify
from flask import request
from sqlalchemy import text

from . import web
from libs.error import OperationError
from config import config
from libs.tool import db_connect
from db.model import RepositoryModel

DB = config.ISSUE_TRACKER_MYSQL_DB #########################这里配置需要改
DEFAULT_FIELD_LIST = ('uuid', 'local_addr', 'is_private', 'description')
REPO_PREFIX = config.REPO_PATH

@web.route('/repository', methods=['POST'])
def query_repo_info():
    query = request.form.get('query')
    field_list = DEFAULT_FIELD_LIST if request.form.get('field_list') is None else request.form.get('field_list').split(',') # 默认参数
    page = 1 if request.form.get('page') is None else int(request.form.get('page')) # 默认参数
    per_page = 1000 if request.form.get('per_page') is None else int(request.form.get('per_page')) # 默认参数,
    try:
        session = db_connect(DB)
        count = session.query(RepositoryModel).filter(text(query)).count()
        ret = session.query(RepositoryModel).filter(text(query)).limit(per_page).offset((page - 1) * per_page)
    except Exception as e:
        # raise OperationError('Invalid query')
        raise OperationError(e.__str__()) # 调试模式
    else:
        session.close()
        data = []
        for item in ret:
            dic = dict()
            for field in field_list:
                try:
                    if field == 'local_addr':
                        dic[field] = REPO_PREFIX + '/' + item.__getattribute__(field)
                    else:
                        dic[field] = item.__getattribute__(field)
                except:
                    raise OperationError('Invalid field list')
            data.append(dic)
        return_data = {
            'count':count,
            'data':data
        }
        return jsonify(return_data)


@web.route('/repository/<repo_id>', methods=['GET'])
def get_repo_info(repo_id):
    try:
        session = db_connect(DB)
        ret = session.query(RepositoryModel).filter(RepositoryModel.uuid == repo_id).first()
    except Exception as e:
        raise OperationError('Invalid query')
        # raise OperationError(e.__str__()) # 调试模式
    else:
        session.close()
        data = []
        field_list = ('uuid', 'repository_id', 'language', 'description', 'url', 'local_addr', 'is_private')
        data = dict()
        for field in field_list:
            try:
                if field == 'local_addr':
                    data[field] = REPO_PREFIX + '/' + ret.__getattribute__(field)
                else:
                    data[field] = ret.__getattribute__(field)
            except:
                raise OperationError('Invalid field list')

        return jsonify(data=data)
