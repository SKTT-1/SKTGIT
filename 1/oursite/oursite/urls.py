from django.conf.urls import patterns, include, url
from books.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oursite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^log/$',log),
    url(r'^login/$',login),
    url(r'^add/$',add),
    url(r'^addpeople/$',addpeople),
    url(r'^add1/$',add1),
    url(r'^addf/$',addf),
    url(r'^searchform/$',searchform),
    url(r'^search/$',search),
    url(r'^manage/$',manage),
    url(r'^check/$',check),
    url(r'^manage/$',manage),
    url(r'^manage1/$',manage1),
    url(r'^manage2/$',manage2),
    url(r'^state/$',state),
    url(r'^up/$',up),
    url(r'^update/$',update),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', logout),
)
