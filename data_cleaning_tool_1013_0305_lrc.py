# 代码生成时间: 2025-10-13 03:05:26
import pandas as pd
from quart import Quart, request, jsonify
from typing import Dict, Any

# 创建Quart应用
app = Quart(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    清洗和预处理DataFrame中的数据。
    """
    # 去除空值
    df = df.dropna()
    
    # 将字符串列转换为小写
    df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    
    # 将数字列中的非数字值替换为NaN
    for column in df.select_dtypes(include=['float', 'int']).columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    
    return df

@app.route('/upload', methods=['POST'])
async def upload_data():
    """
    上传文件并清洗数据。
    """
    try:
        # 获取上传的文件
        file = await request.files['file'].read()
        
        # 读取文件内容
        df = pd.read_csv(file)
        
        # 清洗数据
        cleaned_df = clean_data(df)
        
        # 返回清洗后的数据
        return jsonify(cleaned_df.to_dict(orient='records')), 200
    
    except Exception as e:
        # 错误处理
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)