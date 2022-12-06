# wwdb/urls.py
from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('home/', views.home, name='home'),
    path('castlist/', CastList.as_view(), name='castlist'),
    path('cast/<int:pk>/', views.castdetail, name='castdetail'),
    path('cast/<id>/castenddetail', views.castenddetail, name='castenddetail'),
    path('cast/', views.caststart, name='caststart'),
    path('cast/<int:id>/edit/', views.castedit, name='castedit'),
    path('cast/<int:id>/delete/', CastDelete.as_view(), name='castdelete'),
    path('cast/<id>/castend/', views.castend, name='castend'),
    path('wirelist/', WireList.as_view(), name='wirelist'),
    path('wire/<int:pk>/wiredetail', WireDetail.as_view(), name='wiredetail'),
    path('wire/<int:pk>/edit/', WireEdit.as_view(), name='wireedit'),
    path('wireadd/', WireAdd.as_view(), name='wireadd'),
    path('winchlist/', WinchList.as_view(), name='winchlist'),
    path('winch/<int:pk>/winchdetail', WinchDetail.as_view(), name='winchdetail'),
    path('winch/<int:pk>/edit/', WinchEdit.as_view(), name='winchedit'),
    path('winchadd/', WinchAdd.as_view(), name='winchadd'),
    path('operatorlist/', OperatorList.as_view(), name='operatorlist'),
    path('operator/<int:pk>/operatordetail', OperatorDetail.as_view(), name='operatordetail'),
    path('operator/<int:pk>/edit/', OperatorEdit.as_view(), name='operatoredit'),
    path('operatoradd/', OperatorAdd.as_view(), name='operatoradd'),
    path('deploymentlist/', DeploymentList.as_view(), name='deploymentlist'),
    path('deployment/<int:pk>/deploymentdetail', DeploymentDetail.as_view(), name='deploymentdetail'),
    path('deployment/<int:pk>/edit/', DeploymentEdit.as_view(), name='deploymentedit'),
    path('deploymentadd/', DeploymentAdd.as_view(), name='deploymentadd'),
    path('cutbackreterminationlist/', CutbackReterminationList.as_view(), name='cutbackreterminationlist'),
    path('cutbackretermination/<int:pk>/deploymentdetail', CutbackReterminationDetail.as_view(), name='cutbackreterminationdetail'),
    path('cutbackretermination/<int:pk>/edit/', CutbackReterminationEdit.as_view(), name='cutbackreterminationedit'),
    path('cutbackreterminationadd/', CutbackReterminationAdd.as_view(), name='cutbackreterminationadd'),
    path('cruiseconfigurehome/', views.cruiseconfigurehome, name='cruiseconfigurehome'),
    path('reports/reporting/', views.reportinghome, name='reporting'),
    path('reports/safeworkingload/', views.safeworkingload, name='safeworkingload'),
    path('reports/wireinventory/', views.wireinventory, name='wireinventory'),
    path('reports/postings/', views.postingshome, name='postings'),
]