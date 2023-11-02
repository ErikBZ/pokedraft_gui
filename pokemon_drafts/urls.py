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
BACKEND_URI_PREFIX = "api/v1/"
router = routers.DefaultRouter()
router.register(BACKEND_URI_PREFIX + 'draft_set', PokmeonDraftListSimple)
router.register(BACKEND_URI_PREFIX + 'pokemon', PokemonListViewSet)
router.register(BACKEND_URI_PREFIX + 'draft_session', DraftSessionView)
router.register(BACKEND_URI_PREFIX + 'draft_user', DraftUserView)
router.register(BACKEND_URI_PREFIX + 'draft_rules', DraftRuleListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path(BACKEND_URI_PREFIX + 'draft_set/<pk>', PokmeonDraftListViewSet.as_view({"get": "retrieve"})),
    path(BACKEND_URI_PREFIX + 'draft_set/<pk>/', PokmeonDraftListViewSet.as_view({"get": "retrieve"}))
]
