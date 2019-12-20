import os
import sys

BASE_DIR = os.path.dirname('/home/fdse/pythonApp/restfulAPI')
sys.path.append(BASE_DIR)

from restfulAPI.config import config
from restfulAPI.libs.tool import log

# 进入到每个项目路径下
repo_path_list = []
REPO_PREFIX = config.REPO_PATH
RELEASES_PATH = '/home/fdse/temp/releases'
failed_list = []
with open('./download_list.txt', 'r') as f:
    for line in f.readlines():
        repo_path_list.append(line[:-1])

for repo_path in repo_path_list:
    split = repo_path.split('/')
    repos_name = split[-1]
    user_name = split[-2]
    try:
        os.chdir(repo_path)
        if not os.path.exists(RELEASES_PATH + '/' + user_name):
            os.makedirs(RELEASES_PATH + '/' + user_name)
        ret = os.system('git archive -o %s/%s.zip HEAD' % (RELEASES_PATH + '/' + user_name, repos_name))
        if ret != 0:
            log(' %s: %s archive failed !' % (RELEASES_PATH + '/' + user_name, repos_name))
            failed_list.append(repo_path)
        else:
            log(' %s: export %s successfully !' % (RELEASES_PATH + '/' + user_name, repos_name))
    except Exception as e:
        log(' %s %s: %s archive failed !' % (e.__str__(), RELEASES_PATH + '/' + user_name, repos_name))
        failed_list.append(repo_path)

print(failed_list)

if len(failed_list) != 0:
    with open('./failed_list.txt', 'w+') as f:
        for item in failed_list:
            f.write(item + '\n')