# wwdb/urls.py
from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('castlist/', CastList.as_view(), name='castlist'),
    path('cast/<int:pk>/', CastDetail.as_view(), name='castdetail'),
    path('cast/<int:pk>/castenddetail', CastEndDetail.as_view(), name='castenddetail'),
    path('home/', CastStart.as_view(), name='caststart'),
    path('cast/<int:pk>/edit/', CastEdit.as_view(), name='castedit'),
    path('cast/<int:pk>/delete/', CastDelete.as_view(), name='castdelete'),
    path('cast/<int:pk>/castend/', CastEnd.as_view(), name='castend'),
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
    path('reporting/', views.reportinghome, name='reporting'),
    path('safeworkingloadposting/', views.safeworkingloadposting, name='safeworkingloadposting'),
    path('wireinventory/', views.wireinventory, name='wireinventory'),
]