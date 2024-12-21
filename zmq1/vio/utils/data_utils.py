import os
import tempfile
import pandas as pd
import numpy as np
from ..models import DataFile
from django.core.files import File

def get_original_metrics(data):
    metrics = {
        'shape': {'rows': data.shape[0], 'columns': data.shape[1]},  # 行数和列数
        'columns': data.columns.tolist(),  # 列名
        'missing_values': data.isnull().sum().to_dict(),  # 每列缺失值数量
        'column_types': {col: str(dtype) for col, dtype in data.dtypes.items()}  # 列类型转为字符串
    }
    return metrics

def process_data(
        data: pd.DataFrame,
        columns: list[str],  # 需要处理的列
        missing_method: str = 'drop',  # 缺失值处理方法：'drop'删除, 'mean'均值, 'median'中位数
        outlier_method: str = 'none',  # 异常值处理方法：'none'不处理, 'clip'截断
        outlier_threshold: float = 3.0  # 异常值阈值(标准差倍数)
) -> pd.DataFrame:
    processed_data = data.copy()

    # 缺失值处理
    if missing_method == 'drop':
        processed_data = processed_data.dropna(subset=columns)
    elif missing_method == 'mean':
        processed_data[columns] = processed_data[columns].fillna(processed_data[columns].mean())
    elif missing_method == 'median':
        processed_data[columns] = processed_data[columns].fillna(processed_data[columns].median())

    # 异常值处理
    if outlier_method == 'clip':
        for col in columns:
            mean = processed_data[col].mean()
            std = processed_data[col].std()
            lower_bound = mean - outlier_threshold * std
            upper_bound = mean + outlier_threshold * std
            processed_data[col] = processed_data[col].clip(lower_bound, upper_bound)

    return processed_data

def save_processed_data(processed_data: pd.DataFrame, original_file, user):
    original_name = original_file.original_name
    name_parts = original_name.rsplit('.', 1)
    new_filename = f"{name_parts[0]}_processed.{name_parts[1]}"

    # 创建临时文件并写入处理后的数据
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{name_parts[1]}') as tmp_file:
        if name_parts[1] == 'csv':
            processed_data.to_csv(tmp_file.name, index=False)
        else:  # xlsx
            processed_data.to_excel(tmp_file.name, index=False)

        # 创建并保存新的DataFile对象
        new_file = DataFile(author=user, original_name=new_filename)
        # 将临时文件的内容保存到 DataFile 的 file 字段中。
        # 因为 Django 的 FileField.save() 方法需要一个 Django 的 File 对象，而不是原生的 Python 文件对象s所以要File(f)
        with open(tmp_file.name, 'rb') as f:
            new_file.file.save(new_filename, File(f), save=True)

    # 删除临时文件
    os.remove(tmp_file.name)

    return new_file
