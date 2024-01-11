from django.urls import  path
from . import views, api

urlpatterns=[
    path("api",api.Dlist,name='json'),
    path("api/post",api.Dhtviews.as_view(),name='json'),
    path('index',views.index_view,name='index'),
    path("table",views.table_view,name='table'),
    path("chart",views.chart_view,name='chart'),
    path('download_csv/',views.download_csv,name='download_csv'),
    path('',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('chart-data-<str:period>/', views.chart_data_period, name='chart_data_period'),

]