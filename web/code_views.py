import json
import os
from redis import Redis

from flask import jsonify, request
from . import web
from libs.error import OperationError
from libs import mysqlOperation
from config.config import REPO_PATH
from kafka import KafkaProducer
from config import config
from libs.tool import from_path_get_branch, from_path_get_host, db_connect
from db.model import RepositoryModel

KAFKA_TOPIC_COMPLETE_DOWNLOAD = 'UpdateCommit'
KAFKA_HOST = config.KAFKA_HOST
LOCALHOST = config.LOCALHOST
DB = config.ISSUE_TRACKER_MYSQL_DB

# @web.route('/code-service', methods=['GET'])
# def get_root_path():
#     repo_id = request.args['repo_id']
#     commit_id = request.args['commit_id']
#     try:
#         session = db_connect(DB)
#         query_ret = session.query(RepositoryModel.local_addr).filter(RepositoryModel.uuid == repo_id).first()
#         if query_ret is None:
#             message = {
#                 'status': 'Failed',
#                 'content': 'This repository is not existed'
#             }
#             return jsonify(data=message)
#
#         r = Redis(host=config.REDIS['host'], password=config.REDIS['host'], db=config.REDIS['db'])
#         r.rpush(repo_id, 'none')
#         pop = r.lpop(repo_id).decode()
#         if pop == 'none':
#             message = {
#                 'status': 'Failed',
#                 'content': 'This repository is not free'
#             }
#             return jsonify(data=message)
#         else:
#             try:
#                 split = query_ret.local_addr.split('/')
#                 # pop = host-branch-index
#                 pop_split = pop.split('-')
#                 host = pop_split[0]
#                 branch = pop_split[1]
#                 index = pop_split[2]
#                 # 中汇
#                 if host == LOCALHOST: # localhost
#                     root_path = REPO_PATH + '/' + query_ret.local_addr.replace(split[-1], split[-1] + '_duplicate_fdse-') + index
#                 # 应该写个小函数转换 这样可读性更好
#                 else:
#                     root_path = REPO_PATH + '/' + host + '/' + query_ret.local_addr.replace(split[-1], split[-1] + '_duplicate_fdse-') + index
#                 os.chdir(root_path)
#                 ret = os.system('git checkout %s' % commit_id)
#                 if ret != 0:
#                     message = {
#                         'status': 'Failed',
#                         'content': 'This commit is not existed'
#                     }
#                     r.lpush(repo_id, pop)
#                     r.rpop(repo_id)
#                     return jsonify(data=message)
#             except Exception as e:
#                 r.lpush(repo_id, pop)
#                 r.rpop(repo_id)
#                 raise e
#         # 访问控制
#         session.close()
#
#     except Exception as e:
#         raise OperationError(e.__str__())
#     else:
#         message = {
#             'status': 'Successful',
#             'content': root_path
#         }
#         return jsonify(data=message)

# @web.route('/code-service/free', methods=['GET'])
# def free_resource():
#
#     try:
#         repo_id = request.args['repo_id']
#         path = request.args['path']
#         session = db_connect(DB)
#         query_ret = session.query(RepositoryModel.url).filter(RepositoryModel.uuid == repo_id).first()
#         r = Redis(host=config.REDIS['host'], password=config.REDIS['host'], db=config.REDIS['db'])
#         # path合法性判断
#         split = path.split('/')
#         host = from_path_get_host(path)
#         branch = from_path_get_branch(path, query_ret.url.split('/')[-1])
#         index = split[-1][-1]
#         item = '%s-%s-%s' % (host, branch, index)
#         key = repo_id
#         r.lpush(key, item)
#         r.rpop(key)
#         # 访问控制
#
#     except Exception as e:
#         raise OperationError(e.__str__())
#     else:
#         message = {
#             'status': 'Successful',
#         }
#         return jsonify(data=message)

# @web.route('/code-service/ls', methods=['GET'])
# def get_file_list():
#     try:
#         path = request.args['path']
#         os.chdir(path)
#
#         # 访问控制
#         data = os.listdir(os.getcwd())
#
#     except Exception as e:
#         raise OperationError(e.__str__())
#     else:
#         message = {
#             'status':'Successful',
#             'content':data
#         }
#         return jsonify(data=message)

# @web.route('/code-service/refresh', methods=['PUT'])
# def refresh():
#     repo_id = request.args['repo_id']
#     try:
#         local_addr = mysqlOperation.get_data_from_mysql(
#             tablename='repository',
#             params={'repo_id': repo_id},
#             fields=['local_addr'],
#         )[0][0]
#
#         os.chdir(REPO_PATH + '/' + local_addr)
#         os.system('git pull')
#         os.system('git log --pretty=format:"%H" > check.log')
#
#         with open(REPO_PATH + '/' + local_addr + '/check.log', 'r', encoding='UTF-8') as f:
#             length = f.readlines().__len__()
#
#         max_index = mysqlOperation.get_data_from_mysql(
#             sql='select max(self_index) from commit where repo_id = "%s"' % repo_id
#         )[0][0]
#
#         if length > max_index:
#             producer = KafkaProducer(bootstrap_servers=KAFKA_HOST, api_version=(0, 9))
#             msg = {
#                 'repoId': repo_id,
#                 'local_addr': local_addr,
#                 'max_index': max_index,
#                 'flag': 'not first added and existed'
#             }
#             producer.send(KAFKA_TOPIC_COMPLETE_DOWNLOAD, json.dumps(msg).encode())
#             producer.close()
#
#     except Exception as e:
#         raise OperationError(e.__str__())
#
#     else:
#         message = {
#             'status':'Successful'
#         }
#         return jsonify(data=message)



@web.route('/code-service', methods=['GET'])
def get_root_path():
    repo_id = request.args['repo_id']
    commit_id = request.args['commit_id']
    try:
        session = db_connect(DB)
        query_ret = session.query(RepositoryModel.local_addr).filter(RepositoryModel.uuid == repo_id).first()
        if query_ret is None:
            message = {
                'status': 'Failed',
                'content': 'This repository is not existed'
            }
            return jsonify(data=message)
        root_path = REPO_PATH + '/' + query_ret.local_addr + '_duplicate_fdse-0'
        os.chdir(root_path)
        os.system('git reset --hard')
        ret = os.system('git checkout %s' % commit_id)
        if ret != 0:
            message = {
                'status': 'Failed',
                'content': 'This commit is not existed'
            }
            return jsonify(data=message)

    except Exception as e:
        raise OperationError(e.__str__())
    else:
        message = {
            'status': 'Successful',
            'content': root_path
        }
        return jsonify(data=message)


@web.route('/code-service/free', methods=['GET'])
def free_resource():
    message = {
        'status': 'Successful',
    }
    return jsonify(data=message)







# @web.route('/code-service', methods=['GET'])
# def get_file_content():
#     file_path = request.args['file_path']
#     try:
#         with open(file_path, 'r', encoding='UTF-8') as f:
#             data = f.read()
#     except Exception as e:
#         raise OperationError(e.__str__())
#     else:
#         message = {
#             'status':'Successful',
#             'content':data
#         }
#         return jsonify(data=message)


# @web.route('/code-service/authorization', methods=['GET'])
# def get_authorization():
#     repo_id = request.args['repo_id']
#     try:
#         local_addr = mysqlOperation.get_data_from_mysql(
#             tablename = 'repository',
#             params={'uuid': repo_id},
#             fields=['local_addr']
#         )
#         if len(local_addr) == 0:
#             message = {
#                 'status': 'Failed',
#                 'content': 'This repository is not existed'
#             }
#             return jsonify(data=message)
#
#     except Exception as e:
#         raise OperationError(e.__str__())
#     else:
#         r = Redis(host='10.141.221.85', password='85redis', db=5)
#         if r.llen(local_addr[0][0]) == 0:
#             message = {
#                 'status': 'Failed',
#                 'content': 'This repository is not free'
#             }
#             return jsonify(data=message)
#         else:
#             message = {
#                 'status': 'Successful'
#             }
#             return jsonify(data=message)


# @web.route('/code-service/ls', methods=['GET'])
# def get_file_list():
#     repo_id = request.args['repo_id']
#     commit_id = request.args['commit_id']
#     try:
#         local_addr = mysqlOperation.get_data_from_mysql(
#             tablename = 'repository',
#             params={'uuid': repo_id},
#             fields=['local_addr']
#         )
#         if len(local_addr) == 0:
#             message = {
#                 'status': 'Failed',
#                 'content': 'This repository is not existed'
#             }
#             return jsonify(data=message)
#
#         os.chdir(REPO_PATH + '/' + local_addr[0][0])
#         ret = os.system('git checkout %s' % commit_id)
#         if ret != 0:
#             message = {
#                 'status': 'Failed',
#                 'content': 'This commit is not existed'
#             }
#             return jsonify(data=message)
#         # 访问控制
#         data = os.listdir(os.getcwd())
#
#     except Exception as e:
#         raise OperationError(e.__str__())
#     else:
#         message = {
#             'status':'Successful',
#             'content':data
#         }
#         return jsonify(data=message)