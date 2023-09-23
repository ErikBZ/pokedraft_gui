"""pokemon_drafts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from pokedraft.views import *

router = routers.DefaultRouter()
router.register(r'draft_set', PokmeonDraftListSimple)
router.register(r'pokemon', PokemonListViewSet)
router.register(r'draft_session', DraftSessionView)
router.register(r'draft_user', DraftUserView)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('draft_set/<pk>', PokmeonDraftListViewSet.as_view({"get": "retrieve"})),
    path('draft_set/<pk>/', PokmeonDraftListViewSet.as_view({"get": "retrieve"}))
]
