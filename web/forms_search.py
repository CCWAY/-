from django import forms


class SearchForm(forms.Form):
    # 定义表单，验证数据
    start_city = forms.CharField(required=True, max_length=10, min_length=2,
                                 error_messages={
                                     'required': '必须填写出发城市',
                                     'max_length': '至多10字符',
                                     'min_length': '至少3字符'
                                 })
    arrive_city = forms.CharField(required=True, max_length=10, min_length=2,
                                  error_messages={
                                      'required': '必须填写目的城市',
                                      'max_length': '至多10字符',
                                      'min_length': '至少2字符'
                                  })
    leave_date = forms.CharField(required=True, error_messages={
                                       'required': '日期还没选取',
                               })

