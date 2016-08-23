from django.conf.urls import url, include
from rest_framework import routers
from api import views
from api import urls

router = routers.DefaultRouter()
router.register(r'sessions', views.SessionViewSet)
router.register(r'committees', views.CommitteeViewSet)
router.register(r'issues', views.IssueViewSet)
router.register(r'petitions', views.PetitionViewSet)
router.register(r'signatures', views.SignatureViewSet)
router.register(r'members', views.MemberViewSet)
router.register(r'parties', views.PartyViewSet)
router.register(r'seats', views.SeatViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),    
    url(r'^spider/all/$', views.scrape_all),
    url(r'^spider/session/$', views.session_spider, {'spider': 'session'}),
    url(r'^spider/parties/$', views.party_spider, {'spider': 'party'}),
    url(r'^spider/committees/$', views.committee_spider, {'spider': 'committee'}),
    url(r'^spider/session/(?P<session>[\d-]+)/issues/$', views.issue_spider, {'spider': 'issue'}),    
    url(r'^spider/session/(?P<session>[\d-]+)/members/$', views.member_spider, {'spider': 'member'}),    
    url(r'^spider/session/(?P<session>[\d-]+)/petitions/$', views.petition_spider, {'spider': 'petition'}),
    
    

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^', include('api.urls')),
    

]