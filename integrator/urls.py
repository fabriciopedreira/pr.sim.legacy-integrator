
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

app_name = 'api'
API_V1 = "api/v1"

schema_view = get_schema_view(
    openapi.Info(
        title="Pricing Legacy Integrator",
        default_version='v1',
        description="Service to integrate with the Legacy system.",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="frank.ramirez@solfacil.com.br"),
        license=openapi.License(name="SOLFACIL LICENSE"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Swagger UI.
    re_path(
        r'^swagger-ui(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(
        r'^swagger-ui/$',
        schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(
        r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # rest_framework urls.
    path('', include('rest_framework.urls', namespace='rest_framework')),
    # apps urls.

]