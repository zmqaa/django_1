from django import forms

class ChartForm(forms.Form):
    plot_types = [
        ('scatter', '散点图'),
        ('line', '折线图'),
        ('bar', '柱状图'),
        ('histogram', '直方图'),
        ('heatmap', '热力图'),
        ('box', '箱型图'),
        ('scatter_matrix', '散点矩阵图'),
    ]
    plot_type = forms.ChoiceField(choices=plot_types, label="选择图表类型")
    x_col = forms.ChoiceField(label="选择X轴")
    y_col = forms.MultipleChoiceField(label="选择Y轴", widget=forms.CheckboxSelectMultiple)
    line_count = forms.IntegerField(label='展示的行数')