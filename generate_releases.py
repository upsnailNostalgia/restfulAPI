import os
# import sys

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)

from ..config import config
from libs.tool import log

# 进入到每个项目路径下
repo_path_list = []
REPO_PREFIX = config.REPO_PATH
RELEASES_PATH = '/home/fdse/temp/releases'

with open('./download_list.txt') as f:
    for line in f.readlines():
        repo_path_list.append(line[:-1])

for repo_path in repo_path_list:
    os.chdir(repo_path)
    split = repo_path.split('/')
    repos_name = split[-1]
    user_name = split[-2]
    if not os.path.exists(RELEASES_PATH + '/' + user_name):
        os.makedirs(RELEASES_PATH + '/' + user_name)
    ret = os.system('git archive -o %s/%s.zip HEAD' % (RELEASES_PATH + '/' + user_name, repos_name))
    if ret != 0:
        log(' %s: %s archive failed !' % (RELEASES_PATH + '/' + user_name, repos_name))
    else:
        log(' %s: export %s successfully !' % (RELEASES_PATH + '/' + user_name, repos_name))

