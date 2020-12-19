from django import forms 
from django.contrib.auth.models import User
from .models import Course
from django.forms import ModelForm

from .models import Homework   # 新增

from .models import Handin   # 新增
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Comment # 新增

 
class RegistrationForm(forms.Form):
    username = forms.CharField(label=' 用户名',max_length=50, widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'用户名'}))
    password1 = forms.CharField(label=' 密 码 ', widget=forms.widgets.PasswordInput(attrs={'class':'form-control','placeholder':'密码'}))
    password2 = forms.CharField(label='确认密码', widget=forms.widgets.PasswordInput(attrs={'class':'form-control','placeholder':'确认密码'}))
    role = forms.ChoiceField(label='角色',choices=((0,'学生'),(1,'教师')), widget=forms.widgets.Select(attrs={'class': 'form-control'}))
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
 
        if len(username) < 6:
            raise forms.ValidationError("用户名必须至少为6个字符！")
        elif len(username) > 50:
            raise forms.ValidationError("用户名太长！")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("用户名已存在！")
        return username
 
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
 
        if len(password1) < 6:
            raise forms.ValidationError("密码太短！")
        elif len(password1) > 20:
            raise forms.ValidationError("密码太长！")
        return password1
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配，请重新输入！")
 
        return password2
 
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
 
    def clean_username(self):
        username = self.cleaned_data.get('username')
        filter_result =  User.objects.filter(username__exact=username)
        if not filter_result:
            raise forms.ValidationError("用户名不存在！")
        return username


class ProfileForm(forms.Form):
    """
        个人信息的表单类
    """
    name = forms.CharField(label='姓名', max_length=50, required=False)
    gender = forms.ChoiceField(label='性别',
                                widget=forms.Select(),
                                choices=([('0', '男'), ('1', '女')]),
                                required=False
                            )


class PwdChangeForm(forms.Form):
    """
        密码修改的表单类
    """
    old_password = forms.CharField(label=' 原 密 码 ', widget=forms.PasswordInput)
    password1 = forms.CharField(label=' 新 密 码 ', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("密码太短！")
        elif len(password1) > 20:
            raise forms.validationError("密码太长！")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配，请重新输入！")
        return password2


class CourseForm(forms.ModelForm):
    """
        课程的表单类
    """
    class Meta:
        model = Course
        # 选择指定字段的所有数据 field
        fields = ['cname', 'classes', 'description']
        # boostrap表单需要 form-control 这个样式
        widgets = {
            'cname': forms.TextInput(attrs={'class': 'form-control'}),
            'classes': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                'rows':'3'})
        }

class HomeworkForm(ModelForm):

    """
        发布作业的表单类
    """
    class Meta:
        model = Homework
        # 剔除指定字段的所有数据 exclude
        exclude = ['author', 'views', 'published', 'course']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'body': forms.Textarea(attrs={'class': 'form-control'}),
            'body': CKEditorUploadingWidget(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '作业标题',
            'body': '作业内容',
            'status': '作业状态',
            'group': '组队状态',
            'file': '上传文件',
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in ["", "jpg", "png", "pdf", "xlsx", "docx", "doc"]:
                raise forms.ValidationError(
                "Only jpg, png, pdf, doc, docx, and xlsx files are allowed."
                    )
            return file

class HandinForm(ModelForm):
    """
        提交作业的表单类
    """

    class Meta:
        model = Handin
        exclude = ['author', 'homework', 'course', 'score']
        widgets = {
            # 'body': forms.Textarea(attrs={'class': 'form-control'}),
            'body': CKEditorUploadingWidget(attrs={'class': 'form-control'}),
            # 'file': forms.FileInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in ["", "jpg", "png", "pdf", "xlsx", "docx", "doc"]:
                raise forms.ValidationError(
                "Only jpg, png, pdf, doc, docx, and xlsx files are allowed"
                    )
            return file


class CommentForm(forms.ModelForm):
    """
        作业评论的表单类
    """
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control','rows':'3'}),
        }
        labels = {
            'text':'评论内容',
        }