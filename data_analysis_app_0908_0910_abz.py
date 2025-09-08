# 代码生成时间: 2025-09-08 09:10:32
import quart
from quart import jsonify, request
import pandas as pd
import numpy as np

# 定义全局数据存储
data_storage = {}

class DataAnalysisError(Exception):
    """
    自定义异常类用于处理数据分析错误
    """
    pass

class DataAnalyzer:
    """
    数据分析师类，负责处理数据相关的业务逻辑
    """
    def __init__(self, data_storage):
        self.data_storage = data_storage

    def load_data(self, dataset_name, data):
        """
        加载数据到存储中
        """
        try:
            self.data_storage[dataset_name] = pd.DataFrame(data)
        except Exception as e:
            raise DataAnalysisError(f"Failed to load data: {e}")

    def calculate_mean(self, dataset_name):
        """
        计算指定数据集的平均值
        """
        try:
            data = self.data_storage[dataset_name]
            mean_value = data.mean().to_dict()
            return mean_value
        except KeyError:
            raise DataAnalysisError(f"Dataset '{dataset_name}' not found.")
        except Exception as e:
            raise DataAnalysisError(f"Failed to calculate mean: {e}")

    def calculate_median(self, dataset_name):
        """
        计算指定数据集的中位数
        """
        try:
            data = self.data_storage[dataset_name]
            median_value = data.median().to_dict()
            return median_value
        except KeyError:
            raise DataAnalysisError(f"Dataset '{dataset_name}' not found.")
        except Exception as e:
            raise DataAnalysisError(f"Failed to calculate median: {e}")

app = quart.Quart(__name__)
analyzer = DataAnalyzer(data_storage)

@app.route('/upload', methods=['POST'])
async def upload_data():
    """
    上传数据接口
    """
    try:
        dataset_name = request.form.get('dataset_name')
        data = request.json.get('data')
        if dataset_name and data:
            analyzer.load_data(dataset_name, data)
            return jsonify({'status': 'success', 'message': 'Data uploaded successfully'})
        else:
            raise ValueError('Missing dataset_name or data in request')
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except DataAnalysisError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/mean/<dataset_name>', methods=['GET'])
async def calculate_mean(dataset_name):
    """
    计算并返回指定数据集的平均值
    """
    try:
        mean_value = analyzer.calculate_mean(dataset_name)
        return jsonify({'status': 'success', 'message': 'Mean calculated successfully', 'mean': mean_value})
    except DataAnalysisError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/median/<dataset_name>', methods=['GET'])
async def calculate_median(dataset_name):
    """
    计算并返回指定数据集的中位数
    """
    try:
        median_value = analyzer.calculate_median(dataset_name)
        return jsonify({'status': 'success', 'message': 'Median calculated successfully', 'median': median_value})
    except DataAnalysisError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)