import os

from libs.tool import log


def git_checkout(pwd, commit_id):
    pass

def git_log(pwd, target):
    pass

def git_archive(path, user_name, repos_name, commitd_id):
    # RELEASES_ROOT_PATH = '/home/fdse/data/temp/releases'
    RELEASES_ROOT_PATH = 'd:/valysin/releases'

    try:
        os.chdir(path)
        release_path = '%s/%s-%s' % (RELEASES_ROOT_PATH + '/' + user_name, repos_name, commitd_id)
        release_name = '%s-%s' % (repos_name, commitd_id)
        if not os.path.exists(RELEASES_ROOT_PATH + '/' + user_name):
            os.makedirs(RELEASES_ROOT_PATH + '/' + user_name)

        ret = os.system('git archive -o %s.zip %s' % (release_path, commitd_id))
        if ret != 0:
            log(' %s: %s archive failed !' % (RELEASES_ROOT_PATH + '/' + user_name, repos_name))
            return None
        else:
            log(' %s: export %s successfully !' % (RELEASES_ROOT_PATH + '/' + user_name, repos_name))
            os.chdir(RELEASES_ROOT_PATH + '/' + user_name)
            ret = os.system('unzip %s.zip -d %s' % (release_name, release_name))
            if ret != 0:
                log(' %s: %s.zip unzip failed !' % (RELEASES_ROOT_PATH + '/' + user_name, release_name))
                return None

    except Exception as e:
        log(' %s %s: %s archive failed !' % (e.__str__(), RELEASES_ROOT_PATH + '/' + user_name, repos_name))
        return None

    return release_path

def git_clone(src, dest, depth=''):
    if depth != '':
        src = 'file://' + dest
        depth = '--depth=%s' % depth
    arg = '%s %s %s' % (depth, src, dest)
    ret = os.system('git clone %s' % arg)
    if ret != 0:
        return None
    return ret

