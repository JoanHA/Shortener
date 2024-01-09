from django.urls import path 
from .views import CreaterShorter,LinkPage,RedirectLink,LinksAvailables
from . import views
app_name ="core"
urlpatterns = [
    path("",CreaterShorter.as_view(),name="index"),
    path("<int:pk>/",LinkPage.as_view(),name="details"),
    path("<str:code>/",RedirectLink.as_view(),name="redirect"),
    path("links/",LinksAvailables.as_view(),name="links"),
]
