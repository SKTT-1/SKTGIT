# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
from extend.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^media/(?P<path>.*)','django.views.static.serve',{'document_root':'./extend/'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login),
    url(r'^homepage/', show_homepage),
    url(r'^logout/', log_out),
    url(r'^check_user/', check_user),
    url(r'^add_user/',add_user),
    url(r'^search_device/',search_device),
    url(r'^add_device/',add_device),
    url(r'^manage_form/',manage_form),
    url(r'^add_apply/',add_apply),
    url(r'^show_addform/',show_addform),
    url(r'^show_form/',show_form),
    url(r'^borrow_apply/',borrow_apply),
    url(r'^dumping_apply/',dumping_apply),
    url(r'^manage_apply/',manage_apply),
    url(r'^myform/',myform),
    url(r'^user_addform/',user_addform),
    url(r'^user_form/',user_form),
    url(r'^check_borrow/',show_device),
    url(r'^check_dumping/',show_device),
    url(r'^check_manage/',show_device),
    url(r'^form_inform/',show_device),
    url(r'^delete_user/',delete_user),
    url(r'^updata_user/',updata_user), 
    url(r'^user_inform',user_inform),
    url(r'^check_device',check_device),
    url(r'^my_inform',my_inform),
    url(r'^change_passwd',change_passwd),
)
