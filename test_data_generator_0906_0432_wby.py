# 代码生成时间: 2025-09-06 04:32:22
import quart
from random import randint, choice, sample
from string import ascii_letters, digits
from faker import Faker


# 定义一个测试数据生成器类
class TestDataGenerator:
    def __init__(self):
        self.fake = Faker()

    # 生成随机字符串
    def generate_random_string(self, length):
        """
        根据指定长度生成一个随机字符串。
        :param length: 字符串长度
        :return: 随机字符串
        """
        return ''.join(choice(ascii_letters + digits) for _ in range(length))

    # 生成随机整数
    def generate_random_integer(self, start, end):
        """
        根据指定范围生成一个随机整数。
        :param start: 范围开始值
        :param end: 范围结束值
        :return: 随机整数
        """
        return randint(start, end)

    # 生成随机列表
    def generate_random_list(self, size, element_type):
        """
        根据指定大小和元素类型生成一个随机列表。
        :param size: 列表大小
        :param element_type: 元素类型（'string' 或 'integer'）
        :return: 随机列表
        """
        if element_type == 'string':
            return [self.generate_random_string(10) for _ in range(size)]
        elif element_type == 'integer':
            return [self.generate_random_integer(1, 100) for _ in range(size)]
        else:
            raise ValueError('Unsupported element type')

    # 生成随机样本
    def generate_random_sample(self, population, k):
        """
        从给定的总体中随机生成一个大小为k的样本。
        :param population: 总体
        :param k: 样本大小
        :return: 随机样本
        """
        return sample(population, k)

    # 生成随机 Faker 数据
    def generate_random_faker_data(self):
        """
        使用 Faker 生成随机数据。
        :return: 随机 Faker 数据
        """
        return {
            'name': self.fake.name(),
            'email': self.fake.email(),
            'address': self.fake.address(),
            'phone_number': self.fake.phone_number()
        }


# 创建 Quart 应用
app = quart.Quart(__name__)

# 定义测试数据生成器路由
@app.route('/generate-test-data', methods=['GET'])
async def generate_test_data():
    try:
        generator = TestDataGenerator()
        random_string = generator.generate_random_string(10)
        random_integer = generator.generate_random_integer(1, 100)
        random_list = generator.generate_random_list(5, 'string')
        random_sample = generator.generate_random_sample(list(range(100)), 10)
        random_faker_data = generator.generate_random_faker_data()

        # 返回测试数据 JSON 响应
        return quart.jsonify({
            'random_string': random_string,
            'random_integer': random_integer,
            'random_list': random_list,
            'random_sample': random_sample,
            'random_faker_data': random_faker_data
        })
    except Exception as e:
        # 返回错误信息
        return quart.jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)