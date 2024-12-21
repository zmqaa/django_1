from django import forms
from ..models import DataFile

class DataFileForm(forms.ModelForm):
    class Meta:
        model = DataFile
        fields = ('file',)

class DataProcessForm(forms.Form):
    columns = forms.MultipleChoiceField(
        label='选择需要处理的列',
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )

    missing_method = forms.ChoiceField(
        label='缺失值处理方法',
        choices=[
            ('drop', '删除缺失值'),
            ('mean', '均值填充'),
            ('median', '中位数填充')
        ],
        initial='drop',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    outlier_method = forms.ChoiceField(
        label='异常值处理方法',
        choices=[
            ('none', '不处理'),
            ('clip', '截断处理')
        ],
        initial='none',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    outlier_threshold = forms.FloatField(
        label='异常值阈值',
        initial=3.0,
        min_value=0.1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )