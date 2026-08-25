from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Administración Publicerias CGC"
admin.site.site_title = "Publicerias CGC"
admin.site.index_title = "Panel de administración"

admin.site.index_template = "admin/custom_index.html"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]