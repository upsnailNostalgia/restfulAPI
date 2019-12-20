#encoding:utf-8

from flask import jsonify, request

from db.model import CommitModel
from forms.commit_form import CommitForm, CheckoutForm, CheckoutMasterForm, CommitIdForm, DiffForm
from libs.error import OperationError
from config import config
from libs.tool import db_connect
from web.error_views import not_found
from . import web

DB = config.ISSUE_TRACKER_MYSQL_DB
TIME_FIELD_LIST = ('commit_time',)

def send_msg(host, recv, msg):
    from kafka import KafkaProducer
    import json
    producer = KafkaProducer(bootstrap_servers=host, api_version=(0, 9))
    producer.send(recv, json.dumps(msg).encode())
    producer.close()


@web.route('/commit', methods=['GET'])
def get_commit():

    form = CommitForm(request.args)
    if form.validate():
        repo_id = form.repo_id.data
        page = form.page.data
        per_page = form.per_page.data
        is_whole = form.is_whole.data
        developer = form.developer.data
        try:
            session = db_connect(DB)
            if developer is '':
                if is_whole is True:
                    query_ret = session.query(CommitModel).filter(CommitModel.repo_id == repo_id).\
                        order_by(CommitModel.commit_time.desc()).all()
                else:
                    query_ret = session.query(CommitModel).filter(CommitModel.repo_id == repo_id).\
                        order_by(CommitModel.commit_time.desc()).limit(per_page).offset((page - 1) * per_page)
            else:
                if repo_id is '':
                    query_ret = session.query(CommitModel).filter(CommitModel.developer == developer).\
                        order_by(CommitModel.commit_time.desc()).all()
                else:
                    query_ret = session.query(CommitModel).filter(CommitModel.developer == developer, CommitModel.repo_id == repo_id).\
                        order_by(CommitModel.commit_time.desc()).all()

            data = []
            field_list = ('uuid', 'commit_id', 'message', 'developer', 'commit_time', 'repo_id', 'developer_email')
            for item in query_ret:
                dic = dict()
                for field in field_list:
                    if field in TIME_FIELD_LIST:
                        dic[field] = str(item.__getattribute__(field))
                    else:
                        dic[field] = item.__getattribute__(field)
                data.append(dic)
                del dic
            session.close()
        except:
            return not_found()
        else:
            return jsonify(data=data)

    else:
        raise OperationError('Invalid parameters')

@web.route('/commit/one-day', methods=['GET'])
def get_commit_one_day():
    try:
        repo_id = request.args['repo_id']
        commit_time = request.args['commit_time'].replace('.', '-')
        session = db_connect(DB)
        query_ret = session.query(CommitModel).filter(CommitModel.repo_id == repo_id, CommitModel.commit_time.like(commit_time + "%")).all()
        data = []
        field_list = ('uuid', 'commit_id', 'message', 'developer', 'commit_time', 'repo_id', 'developer_email')
        for item in query_ret:
            dic = dict()
            for field in field_list:
                if field in TIME_FIELD_LIST:
                    dic[field] = str(item.__getattribute__(field))
                else:
                    dic[field] = item.__getattribute__(field)
            data.append(dic)
            del dic
        session.close()
    except Exception as e:
        raise OperationError(e.__str__())
    else:
        if query_ret is None:
            raise OperationError('Invalid parameters')

        else:
            return jsonify(data=data)

@web.route('/commit/<commit_id>', methods=['GET'])
def get_one_commit(commit_id):
    form = CommitIdForm(data={'commit_id':commit_id})
    if form.validate():
        try:
            session = db_connect(DB)
            query_ret = session.query(CommitModel).filter(CommitModel.commit_id == commit_id).first()
            data = dict()
            field_list = ('uuid', 'commit_id', 'message', 'developer', 'commit_time', 'repo_id', 'developer_email')
            for field in field_list:
                if field in TIME_FIELD_LIST:
                    data[field] = str(query_ret.__getattribute__(field))
                else:
                    data[field] = query_ret.__getattribute__(field)
            session.close()
        except:
            return not_found()
        else:
            return jsonify(data=data)

    else:
        raise OperationError('Invalid parameters')


@web.route('/commit/developer-lists-by-commits', methods=['POST'])
def get_developer_email_by_commit():
    try:
        key_set = request.form.get('key_set').split(',')
        session = db_connect(DB)
        query_ret = session.query(CommitModel).filter(CommitModel.commit_id.in_(key_set)).all()
        dev_info = dict()
        data = dict()
        for ret, key in zip(query_ret, key_set):
            dev_info[key] = str(ret.__getattribute__('developer_email'))
        session.close()
    except Exception as e:
        raise OperationError(e.__str__())
    else:
        if query_ret is None:
            raise OperationError('Invalid parameters')

        else:
            data['status'] = 'Successful'
            data['data'] = dev_info
    return jsonify(data)


@web.route('/commit/commit-time', methods=['GET'])
def commit_time():
    try:
        commit_id = request.args['commit_id']
        session = db_connect(DB)
        query_ret = session.query(CommitModel).filter(CommitModel.commit_id == commit_id).first()
        field_list = ('commit_time',)
        data = dict()
        for field in field_list:
            if field in TIME_FIELD_LIST:
                data[field] = str(query_ret.__getattribute__(field))
            else:
                data[field] = query_ret.__getattribute__(field)
        session.close()
    except Exception as e:
        raise OperationError(e.__str__())
    else:
        if query_ret is None:
            raise OperationError('Invalid parameters')

        else:
            data['status'] = 'Successful'
            return jsonify(data=data)






# @web.route('/commit/checkout', methods=['GET'])
# def checkout():
#     form = CheckoutForm(request.args)
#     if form.validate():
#         repo_id = form.repo_id.data
#         commit_id = form.commit_id.data
#         try:
#             repo_info = mysqlOperation.get_data_from_mysql(
#                 tablename = 'repository',
#                 params = {'uuid':repo_id},
#                 fields = ['local_addr']
#             )
#             local_addr = repo_info[0][0]
#             project_path = config.REPO_PATH + '/' +  local_addr
#             os.chdir(project_path)
#
#             os.system('git checkout ' + commit_id)
#         except:
#             raise OperationError('Internal error')
#         else:
#             message = {
#                 'status': 'Successful'
#             }
#             return jsonify(data=message)
#     else:
#         raise OperationError('Invalid parameters')


# @web.route('/commit/checkout-master/<repo_id>', methods=['GET'])
# def checkout_master(repo_id):
#     form = CheckoutMasterForm(data={'repo_id':repo_id})     #检查一下服务器上的代码是否一致
#     if form.validate():
#         repo_id = form.repo_id.data
#         try:
#             repo_info = mysqlOperation.get_data_from_mysql(
#                 tablename = 'repository',
#                 params = {'uuid':repo_id},
#                 fields = ['local_addr']
#             )
#             local_addr = repo_info[0][0]
#             project_path = config.REPO_PATH + '/' +  local_addr
#             os.chdir(project_path)
#
#             os.system('git checkout master')
#         except:
#             raise OperationError('Internal error')
#         else:
#             message = {
#                 'status': 'Successful'
#             }
#             return jsonify(data=message)
#     else:
#         raise OperationError(form.errors)

#
#
# @web.route('/commit/update/<repo_id>', methods=['GET'])      #暂时改成project_id
# def update_commit(repo_id):
#     try:
#         local_addr = mysqlOperation.get_data_from_mysql(
#             tablename='repository',
#             params={'uuid':repo_id},
#             fields=['local_addr']
#         )[0][0]
#         if len(local_addr) == 0:
#             raise OperationError('Invalid parameters')
#     except:
#         raise OperationError('Internal error')
#     else:
#         os.chdir(config.REPO_PATH + '/' + local_addr)
#         os.system('git checkout master')
#         os.system('git pull')
#         mysqlOperation.delete_from_mysql(
#             tablename='commit',
#             field='repo_id',
#             value=repo_id
#         )
#         msg = {'repoId':repo_id, 'projectId':'unknown', 'local_addr':local_addr}
#         send_msg(host=config.KAFKA_HOST['host-1'], recv=config.KAFKA_TOPIC['topic-3'], msg=msg)
#         message = {
#             'status': 'Successful'
#         }
#         return jsonify(data=message)
#
#
# @web.route('/commit/diff', methods=['GET'])
# def get_diff():
#     form = DiffForm(request.args)
#     if form.validate():
#         repo_id = form.repo_id.data
#         start = form.start.data
#         end = form.end.data
#         try:
#             local_addr = mysqlOperation.get_data_from_mysql(
#                 tablename='repository',
#                 params={'uuid': repo_id},
#                 fields=['local_addr']
#             )[0][0]
#             if len(local_addr) == 0:
#                 raise OperationError('Invalid parameters')
#         except:
#             raise OperationError('Internal error')
#         else:
#             os.chdir(config.REPO_PATH + '/' + local_addr)
#             os.system('git diff %s %s > diff.log' % (start, end))
#             with open(config.REPO_PATH + '/' + local_addr + '/diff.log', 'r') as f:
#                 data = f.read()
#             message = {
#                 'status': 'Successful',
#                 'diff':data
#             }
#             return jsonify(data=message)
