from django import forms
from ..models import Article, Comment, Tag


class ArticleForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='标签，多个标签可用逗号隔开',
        label='标签'
    )
    class Meta:
        model = Article
        fields = ['title', 'content']
        labels = {
            'title': '标题',
            'content': '内容',
        }
    # 重写save，处理标签的输入

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        tags_str = self.cleaned_data.get('tags', '')
        if tags_str:
            # strip()去除字符串两边空格
            tags_names = [name.strip() for name in tags_str.split(',') if name.strip()]
            # get_or_create返回值为(object, created)，object是获取或创建的对象，created为true或false。
            tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_names]
            instance.tags.set(tags)

        return instance
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        label = {
            'content':'内容',
        }