import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import DataFile
from ..utils.data_utils import get_original_metrics, process_data, save_processed_data
from ..utils.vis_utils import generate_plot
from ..forms.vis import ChartForm
from ..forms.data import DataProcessForm

@login_required
def data_shape(request, file_id):

    data_file = DataFile.objects.get(pk=file_id, author=request.user)
    file_path = data_file.file.path
    if file_path.endswith('xlsx'):
        data = pd.read_excel(file_path)
    elif file_path.endswith('csv'):
        data = pd.read_csv(file_path)
    else:
        messages.error(request, '仅支持csv与xlsx文件')
        return redirect('profile_file')

    metrics = get_original_metrics(data)
    display_head = data.head(10).to_html()
    return render(request, 'data/data_shape.html', {
        'metrics': metrics,
        'display_head': display_head,
    })


def visualization(request, file_id):
    data_file = DataFile.objects.get(pk=file_id, author=request.user)
    file_path = data_file.file.path

    # 读取数据
    if file_path.endswith('xlsx'):
        data = pd.read_excel(file_path)
    elif file_path.endswith('csv'):
        data = pd.read_csv(file_path)
    else:
        messages.error(request, '仅支持csv与xlsx文件')
        return redirect('profile_file')

    # 获取文件的列
    columns = data.columns.tolist()
    choices = [(col, col) for col in columns]
    plot_html = None    # 这个在没有填写表单的时候就已经传递到前端了，先设置为空
    if request.method == "POST":
        # 创建表单实例时就设置choices
        form = ChartForm(request.POST)
        # 重要：在验证前设置choices
        form.fields['x_col'].choices = choices
        form.fields['y_col'].choices = choices
        if form.is_valid():
            plot_type = form.cleaned_data['plot_type']
            x_col = form.cleaned_data['x_col']
            y_cols = form.cleaned_data['y_col']
            line_count = form.cleaned_data['line_count']
            data = data.head(line_count)

            fig = generate_plot(data, plot_type=plot_type, x_col=x_col, y_cols=y_cols)
            plot_html = fig.to_html(full_html=True)
            print(f'plot_type: {plot_type}, x_col: {x_col}, y_cols: {y_cols}')
    else:
        form = ChartForm()
        form.fields['x_col'].choices = choices
        form.fields['y_col'].choices = choices

    return render(request, 'data/visualization.html', {
        'form': form,
        'plot_html': plot_html,
    })


def process_data_view(request, file_id):
    data_file = DataFile.objects.get(pk=file_id, author=request.user)
    file_path = data_file.file.path

    data = pd.read_csv(file_path) if file_path.endswith('csv') else pd.read_excel(file_path)
    columns = [(col, col) for col in data.columns]

    if request.method == 'POST':
        form = DataProcessForm(request.POST)
        form.fields['columns'].choices = columns
        if form.is_valid():
            try:
                # 读取数据
                if file_path.endswith('xlsx'):
                    data = pd.read_excel(file_path)
                elif file_path.endswith('csv'):
                    data = pd.read_csv(file_path)
                else:
                    messages.error(request, '仅支持csv与xlsx文件')
                    return redirect('profile_file')

                # 处理数据
                processed_data = process_data(
                    data=data,
                    columns=form.cleaned_data['columns'],
                    missing_method=form.cleaned_data['missing_method'],
                    outlier_method=form.cleaned_data['outlier_method'],
                    outlier_threshold=form.cleaned_data['outlier_threshold']
                )

                # 保存处理后的数据
                new_file = save_processed_data(
                    processed_data=processed_data,
                    original_file=data_file,
                    user=request.user
                )

                messages.success(request, '数据处理成功，新文件已生成')
                return redirect('profile_file')  # 或者重定向到新文件的详情页

            except Exception as e:
                messages.error(request, f'处理数据时出错: {str(e)}')
                return redirect('profile_file')
    else:
        # GET请求，需要根据数据文件的列名初始化表单的choices
        form = DataProcessForm()
        form.fields['columns'].choices = columns

    return render(request, 'data/process_data.html', {
        'form': form,
        'file': data_file
    })


