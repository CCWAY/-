from __future__ import absolute_import
import xadmin
from .models import UserSettings, Log
from xadmin import views
from xadmin.views.website import LoginView

from django.utils.translation import ugettext_lazy as _


class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True


xadmin.site.register(UserSettings, UserSettingsAdmin)


# class BaseSetting(object):
#     """xadmin的基本配置"""
#     enable_themes = True  # 开启主题切换功能
#     use_bootswatch = True
#
#
# xadmin.site.register(views.BaseAdminView, BaseSetting)


class LoginViewAdmin(LoginView):
    title = '机票管理后台'


xadmin.site.register(LoginView, LoginViewAdmin)


class LogAdmin(object):

    def link(self, instance):
        if instance.content_type and instance.object_id and instance.action_flag != 'delete':
            admin_url = self.get_admin_url('%s_%s_change' % (instance.content_type.app_label, instance.content_type.model), 
                instance.object_id)
            return "<a href='%s'>%s</a>" % (admin_url, _('Admin Object'))
        else:
            return ''
    link.short_description = ""
    link.allow_tags = True
    link.is_column = False

    list_display = ('action_time', 'user', 'ip_addr', '__str__', 'link')
    list_filter = ['user', 'action_time']
    search_fields = ['ip_addr', 'message']
    model_icon = 'fa fa-cog'


xadmin.site.register(Log, LogAdmin)


class GlobalSetting(object):
    site_title = '机票管理后台'
    site_footer = '机票管理系统'
    # menu_style = "accordion"


xadmin.site.register(views.CommAdminView, GlobalSetting)


