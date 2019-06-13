from django import forms

from web.models import Passenger


class PassengerForm(forms.Form):
    # 定义表单，验证数据
    username = forms.CharField(required=True, max_length=10, min_length=3,
                               error_messages={
                                   'required': '必须填写用户名',
                                   'max_length': '至多10字符',
                                   'min_length': '至少3字符'
                               })
    real_name = forms.CharField(required=True, max_length=10, min_length=2,
                                error_messages={
                                    'required': '必须填写真实姓名',
                                    'max_length': '至多10字符',
                                    'min_length': '至少2字符'
                                })
    password = forms.CharField(required=True, max_length=16, min_length=6,
                               error_messages={
                                   'required': '密码不能为空',
                                   'max_length': '密码不能超过16位',
                                   'min_length': '密码不能短于6位'
                               })
    password2 = forms.CharField(required=True, max_length=16, min_length=6,
                                error_messages={
                                    'required': '密码不能为空',
                                    'max_length': '密码不能超过16位',
                                    'min_length': '密码不能短于6位'
                                })
    card_id = forms.CharField(required=True, max_length=18, min_length=18,
                              error_messages={
                                  'required': '此为必填项',
                                  'max_length': '请输入正确的身份证号码',
                                  'min_length': '请输入正确的身份证号码'
                              })
    sex = forms.IntegerField()

    def clean(self):
        # 用于校验form表单的数据,必须返回校验字段后的结果
        # 默认调用
        # 校验密码是否一致
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password2')
        if pwd1 and pwd2:
            if pwd1 != pwd2:
                raise forms.ValidationError({'password2': '两次密码输入不一致'})

        return self.cleaned_data

    def clean_username(self):
        # 注册， 校验username是否存在
        user = Passenger.objects.filter(username=self.cleaned_data.get('username'))
        if user:
            raise forms.ValidationError('该账号已注册，请更换账号')

        return self.cleaned_data['username']
