from config import config
from db.model import RepositoryModel
from libs.git_operation import git_archive
from libs.tool import db_connect, redis_connect
import pexpect

DB = config.BIG_CODE_DB
REPO_PATH_PREFIX = config.TEST_REPO_PATH
def get_release(repo_id, commit_id='HEAD'):
    session = db_connect(DB)
    query_ret = session.query(RepositoryModel.is_downloaded, RepositoryModel.local_addr).filter(RepositoryModel.uuid == repo_id).first()
    if query_ret.is_downloaded is True:
        repo_path = REPO_PATH_PREFIX + '/' + query_ret.local_addr
        split = query_ret.local_addr.split('/')
        repos_name = split[-1]
        user_name = split[-2]
        ret = git_archive(repo_path, user_name, repos_name, commit_id)
        return ret
    else:
        return None

def get_file_lock(repo_id):
    r = redis_connect(config.REDIS_CONCURRENCY_ACCESS)
    if r is None:
        return None
    if r.exists(repo_id):
        pop = r.lpop(repo_id).decode()
        r.rpush(repo_id, 'none')
        if pop == 'none':
            return None
        else:
            session = db_connect(DB)
            query_ret = session.query(RepositoryModel.local_addr).filter(RepositoryModel.uuid == repo_id).first()


# git -l clone 硬链接
# git clone file:// 先pack再完全克隆


# import subprocess
# from subprocess import Popen
# import pexpect
#
# import os
# os.chdir('/home/fdse/test')
# cmd = 'git clone ssh://fdse@10.141.221.85/home/fdse/user/issueTracker/repo/github/zxing/zxing-master'
#
# password = 'cloudfdse'
# child = pexpect.spawn(cmd)
# child.expect('(yes/no)?')
# child.sendline('yes')
# child.expect("fdse@10.141.221.85's password:")
# child.sendline(password)
# child.expect(pexpect.EOF)
# child.close()

# child.read()
# p = Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
# p.communicate(b'cloudfdse')
# p.wait(3)

# print(p.stdout.read())
