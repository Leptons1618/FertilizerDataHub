# urls.py
from django.urls import path
from .views import OPCDataView, OPCDataApiView

urlpatterns = [
    path('opc_data/', OPCDataView.as_view(), name='opc_data'),
    path('api/opc_data/', OPCDataApiView.as_view(), name='opc_data_api'),
]