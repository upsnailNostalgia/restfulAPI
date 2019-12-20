import unittest
from main import app

class TestGetRepoInfo(unittest.TestCase):
    # 该方法会首先执行，方法名为固定写法
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # 该方法会在测试代码执行完后执行，方法名为固定写法
    def test_normal_run(self):
        data = {
            'query':'stars_count>=1000 and id<=100000 and updated_at>"2019-04-01 10:00:00"',
            'field_list':['id', 'stars_count', 'repos_name', 'updated_at']
        }
        response = app.test_client().post('/repository', data = data)
        json_data = response.data
        print(json_data)

    # def test_except_run(self):
    #     pass


if __name__ == '__main__':
    unittest.main()