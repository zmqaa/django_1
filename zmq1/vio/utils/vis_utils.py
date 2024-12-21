import pandas as pd
import plotly.express as px


def generate_plot(data: pd.DataFrame, plot_type: str, x_col: str, y_cols: list, **kwargs):
    if isinstance(y_cols, str):
        y_cols = [y_cols]

    # 中文支持的标题和标签
    if plot_type == 'scatter':
        fig = px.scatter(data, x=x_col, y=y_cols, title=f'{x_col} 与 {", ".join(y_cols)} 的散点图', **kwargs)

    elif plot_type == 'line':
        fig = px.line(data, x=x_col, y=y_cols, title=f'{x_col} 与 {", ".join(y_cols)} 的折线图', **kwargs)

    elif plot_type == 'bar':
        fig = px.bar(data, x=x_col, y=y_cols, title=f'{x_col} 与 {", ".join(y_cols)} 的柱状图', **kwargs)

    elif plot_type == 'histogram':
        fig = px.histogram(data, x=x_col, y=y_cols, title=f'{", ".join(y_cols)} 的直方图', **kwargs)

    elif plot_type == 'heatmap':
        fig = px.imshow(data[y_cols].corr(), title=f'{", ".join(y_cols)} 的相关性热力图', **kwargs)

    elif plot_type == 'box':
        fig = px.box(data, x=x_col, y=y_cols, title=f'{x_col} 对 {", ".join(y_cols)} 的箱型图', **kwargs)

    elif plot_type == 'scatter_matrix':
        fig = px.scatter_matrix(data, dimensions=y_cols, title=f'{", ".join(y_cols)} 的散点矩阵图', **kwargs)

    else:
        raise ValueError(f"不支持的图像类型: {plot_type}")

    return fig
