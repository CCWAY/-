from django import forms
from django.contrib.auth.hashers import check_password

from web.models import Passenger


class LoginForm(forms.Form):
    # 定义表单，验证数据
    username = forms.CharField(required=True,
                               error_messages={
                                   'required': '必须填写用户名',
                               })
    password = forms.CharField(required=True,
                               error_messages={
                                   'required': '密码不能为空',
                               })

    def clean(self):
        # 登录， 校验username是否已经注册
        passenger = Passenger.objects.filter(username=self.cleaned_data.get('username')).first()
        if not passenger and self.cleaned_data.get('username'):
            raise forms.ValidationError({'username': '该账号未注册，请先去注册'})
        if passenger:
            if not check_password(self.cleaned_data.get('password'), passenger.password):
                raise forms.ValidationError({'password': '你的密码输入有误，请重新输入'})
        return self.cleaned_data


