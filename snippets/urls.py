from django.conf.urls import url
from .views.user import UserRegister, UserLogin, UserDetails, UserList
from .views.location import LocationList, LocationDetails
from .views.visit import VisitDetails, VisitList, VisitCheckIn, UserVisits, LocationVisits

urlpatterns = [
    url(r'^register$', UserRegister.as_view()),
    url(r'^sign_in$', UserLogin.as_view()),

    url(r'^users$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)$', UserDetails.as_view()),

    url(r'^locations$', LocationList.as_view()),
    url(r'^locations/(?P<pk>[0-9]+)$', LocationDetails.as_view()),

    url(r'^locations/(?P<pk>[0-9]+)/visit$', VisitCheckIn.as_view()),

    url(r'^visits$', VisitList.as_view()),
    url(r'^visits/(?P<pk>[0-9]+)$', VisitDetails.as_view()),

    url(r'^locations/(?P<pk>[0-9]+)/ratio$', LocationVisits.as_view()),

    url(r'^users/(?P<pk>[0-9]+)/ratio$', UserVisits.as_view()),
]
