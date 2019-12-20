import unittest
from main import app


class TestGetCommit(unittest.TestCase):
    # 该方法会首先执行，方法名为固定写法
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # 该方法会在测试代码执行完后执行，方法名为固定写法
    def test_normal_run(self):
        repo_id = 'fe5ed888-6a82-11e9-ad13-e9d58090e871'
        page = 1
        per_page = 100
        response = app.test_client().get('/commit?repo_id=%s&page=%s&per_page=%s' % (repo_id, page, per_page))
        json_data = response.data
        print(json_data)

    def test_is_whole(self):
        repo_id = 'fe5ed888-6a82-11e9-ad13-e9d58090e871'
        is_whole = True
        response = app.test_client().get('/commit?repo_id=%s&is_whole=%s' % (repo_id, is_whole))
        json_data = response.data
        print(json_data)

    def test_invalid_param(self):

        response = app.test_client().get('/commit')
        json_data = response.data
        print(json_data)


if __name__ == '__main__':
    unittest.main()