from django import forms
from ..models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dis_name', 'avatar']
        labels = {
            'dis_name': '名称',
            'avatar': '头像'
        }