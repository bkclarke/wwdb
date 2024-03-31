# wwdb/urls.py
from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('home/', views.home, name='home'),

    #URLS related to cast reporting
    path('casts/<int:pk>/', views.castdetail, name='castdetail'),
    path('casts/<id>/castenddetail', views.castenddetail, name='castenddetail'),
    path('casts/', views.caststart, name='caststart'),
    path('casts/manualenter/', views.castmanualenter, name='castmanualenter'),
    path('casts/<int:id>/manualedit/', views.castmanualedit, name='castmanualedit'),
    path('casts/<int:id>/edit/', views.castedit, name='castedit'),
    path('casts/<int:pk>/delete/', CastDelete.as_view(), name='castdelete'),
    path('casts/<id>/castend/', views.castend, name='castend'),
    path('casts/cast_end/', views.cast_end, name='cast_end'),


    #URLS related to configuration
    path('configuration/cruiseadd/', views.cruiseadd, name='cruiseadd'),
    path('configuration/cruise/<int:id>/edit/', views.cruiseedit, name='cruiseedit'),
    path('configuration/cruiseconfiguration/', views.cruiseconfigurehome, name='cruiseconfigurehome'),
    path('configuration/operatorlist/', OperatorList.as_view(), name='operatorlist'),
    path('configuration/operator/<int:pk>/operatordetail', OperatorDetail.as_view(), name='operatordetail'),
    path('configuration/operator/<int:pk>/edit/', OperatorEdit.as_view(), name='operatoredit'),
    path('configuration/operator/<int:id>/editstatus/', views.operatoreditstatus, name='operatoreditstatus'),
    path('configuration/operatoradd/', views.operatoradd, name='operatoradd'),
    path('configuration/deploymentlist/', DeploymentList.as_view(), name='deploymentlist'),
    path('configuration/deployment/<int:pk>/deploymentdetail', DeploymentDetail.as_view(), name='deploymentdetail'),
    path('configuration/deployment/<int:pk>/edit/', DeploymentEdit.as_view(), name='deploymentedit'),
    path('configuration/deployment/<int:id>/editstatus/', views.deploymenteditstatus, name='deploymenteditstatus'),
    path('configuration/deploymentadd/', views.deploymentadd, name='deploymentadd'),

    #URLS related to inventories 
    path('inventories/wire/<int:pk>/wiredetail', WireDetail.as_view(), name='wiredetail'),
    path('inventories/wire/<int:pk>/edit/', WireEdit.as_view(), name='wireedit'),
    path('inventories/wire/<int:id>/editfactorofsafety/', views.wireeditfactorofsafety, name='wireeditfactorofsafety'),
    path('inventories/wireadd/', WireAdd.as_view(), name='wireadd'),
    path('inventories/wirelist/', views.wirelist, name='wirelist'),
    path('inventories/winch/<int:pk>/winchdetail', WinchDetail.as_view(), name='winchdetail'),
    path('inventories/winch/<int:pk>/edit/', WinchEdit.as_view(), name='winchedit'),
    path('inventories/winch/<int:id>/editstatus/', views.wincheditstatus, name='wincheditstatus'),
    path('inventories/winchadd/', views.winchadd, name='winchadd'),
    path('inventories/winchlist/', WinchList.as_view(), name='winchlist'),

    #URLS related to maintenance
    path('maintenance/breaktestlist/', views.breaktestlist, name='breaktestlist'),
    path('maintenance/cutbackreterminationlist/', views.cutbackreterminationlist, name='cutbackreterminationlist'),
    path('maintenance/cutbackretermination/<int:pk>/deploymentdetail', CutbackReterminationDetail.as_view(), name='cutbackreterminationdetail'),
    path('maintenance/cutbackretermination/<int:id>/edit/', views.cutbackreterminationedit, name='cutbackreterminationedit'),
    path('maintenance/cutbackreterminationadd/', views.cutbackreterminationadd, name='cutbackreterminationadd'),

    #URLS related to reports
    path('reports/castlist/', views.castlist, name='castlist'),
    path('reports/safeworkingtensions/', views.safeworkingtensions, name='safeworkingtensions'),
    path('reports/safeworkingtensions_file/', views.safeworkingtensions_file, name='safeworkingtensions_file'),
    path('reports/<int:pk>/cruisereport/', views.cruisereport, name='cruisereport'),
    path('reports/castplot/<int:pk>/', views.castplot, name='castplot'),
    path('reports/cruiselist/', views.cruiselist, name='cruiselist'),
    path('<int:pk>/cruise_report_file', views.cruise_report_file, name='cruise_report_file'),
    path('reports/<int:pk>/wirereport/', views.wirereport, name='wirereport'),
    path('reports/unolswirereport/', views.unolswirereport, name='unolswirereport'),
    path('reports/unols_wire_report_file/', views.unols_wire_report_file, name='unols_wire_report_file'),
]