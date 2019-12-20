import unittest
from main import app


class TestGetCommit(unittest.TestCase):
    # 该方法会首先执行，方法名为固定写法
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # 该方法会在测试代码执行完后执行，方法名为固定写法
    def test_normal_run(self):
        data = {
            'key_set':'88fe3fb82d2d8715e565abc15899ae3bcfe7c296,ae4e0caecf4040ba943d2d75aafd1975fa476a55'
        }
        response = app.test_client().post('/commit/developer-lists-by-commits', data=data)
        json_data = response.data
        print(json_data)


if __name__ == '__main__':
    unittest.main()