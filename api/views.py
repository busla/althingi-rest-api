import django_filters
from django.contrib.auth.models import *
from django.utils.dateparse import parse_datetime
from django.db.models import Count
import pytz
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from api.serializers import *
from api.models import *
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.decorators import api_view, detail_route, list_route, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import filters

import requests
import json
import datetime
import re

from urllib.parse import unquote_plus
from api import utils

@api_view(['GET'])
def session_spider(request, spider):
    """
    Scraped sessions from althingi
    """
    payload = {'spider_name': spider, 'url': unquote_plus(utils.spider_url[spider])}
    r = requests.get('http://localhost:9080/crawl.json?', params=payload)
    spider_response = r.json()['items']

    for item in spider_response:
        date_from = datetime.datetime.strptime(item['date_from'], '%d.%m.%Y').date()
        if item['date_to']:
            date_to = datetime.datetime.strptime(item['date_to'], '%d.%m.%Y').date()
        else:
            date_to = ''

        Session.objects.update_or_create(
            session_id=item['session_id'],
            defaults={'date_to': date_from, 'date_from': date_from}
            )        
    
    return Response(r.json()['items'])

@api_view(['GET'])
def committee_spider(request, spider, session):
    """
    Scraped committees from althingi
    """
    payload = {'spider_name': spider, 'url': unquote_plus(utils.spider_url[spider] % session)}
    r = requests.get('http://localhost:9080/crawl.json?', params=payload)
    spider_response = r.json()['items']

    session_obj = Session.objects.get(session_id=int(session))

    for item in spider_response:

        committee_obj, created = Committee.objects.update_or_create(
            committee_id=item['committee_id'],
            defaults = {
                'name': item['name'], 
                'short_abbr': item['short_abbr'], 
                'long_abbr': item['long_abbr'], 
                }
            )        
        committee_obj.session.add(session_obj)

    return Response(r.json()['items'])

@api_view(['GET'])
def committee_meeting_spider(request, spider, session):
    """
    Scraped committee meetings from althingi
    """
    payload = {'spider_name': spider, 'url': unquote_plus(utils.spider_url[spider] % session)}
    r = requests.get('http://localhost:9080/crawl.json?', params=payload)
    spider_response = r.json()['items']

    session_obj = Session.objects.get(session_id=session)

    for item in spider_response:
        committee_obj = Committee.objects.get(committee_id=item['committee'])
        if (item['start_time'] and item['end_time']):

            CommitteeMeeting.objects.update_or_create(
                meeting_id=item['meeting_id'],
                defaults = {
                    'session': session_obj, 
                    'committee': committee_obj, 
                    'date_from': datetime.datetime.strptime(item['start_time'], '%Y-%m-%dT%H:%M:%S'),
                    'date_to': datetime.datetime.strptime(item['end_time'], '%Y-%m-%dT%H:%M:%S'),
                    }
                )            
    
    return Response(r.json()['items'])

@api_view(['GET'])
def issue_spider(request, spider, session):
    """
    Scraped issues from althingi
    """

    payload = {'spider_name': spider, 'url': unquote_plus(utils.spider_url[spider] % session)}
    r = requests.get('http://localhost:9080/crawl.json?', params=payload)
    spider_response = r.json()['items']

    session_obj = Session.objects.get(session_id=session)

    for item in spider_response:
        issue_obj, created = Issue.objects.update_or_create(
            issue_id=item['issue_id'], 
            session=session_obj,            
            defaults={'name': item['name'], 'url': item['url'], 'issue_id': item['issue_id']})        
        
    return Response(r.json()['items'])

@api_view(['GET'])
def member_spider(request, spider, session):
    """
    Scraped members from althingi
    """

    payload = {'spider_name': spider, 'url': unquote_plus(utils.spider_url[spider] % session)}
    r = requests.get('http://localhost:9080/crawl.json?', params=payload)
    spider_response = r.json()['items']    
    session_obj = get_object_or_404(Session, session_id=session)

    for item in spider_response:
        member_obj, member_created = Member.objects.update_or_create(
            member_id=item['member_id'], 
            defaults={
                'name': item['name'],
                'dob': datetime.datetime.strptime(item['dob'], '%Y-%m-%d').date(),
                #'abbr': item['abbr'],            
            })
        for seat in item['seats']:
            
            party_obj = Party.objects.get(party_id=seat['party_id'])            

            Seat.objects.update_or_create(                
                member=member_obj,
                session=session_obj,
                party=party_obj,
                role=seat['role'],
                region=seat['region_name'],
                date_from = datetime.datetime.strptime(seat['date_from'], '%d.%m.%Y').date() or None,
             )                
    return Response(r.json()['items'])

@api_view(['GET'])
def party_spider(request, spider):
    """
    Scraped parties from althingi
    """

    payload = {'spider_name': spider, 'url': unquote_plus(utils.spider_url[spider])}
    r = requests.get('http://localhost:9080/crawl.json?', params=payload)
    spider_response = r.json()['items']

    #session_obj = get_object_or_404(Session, session_id=session)

    for item in spider_response:
        Party.objects.update_or_create(
            party_id=item['party_id'], 
            defaults={
                'name': item['name'],
                'short_name': item['short_abbr'],
                #'long_name': item['long_name'],
            })        
    
    return Response(r.json()['items'])    

@api_view(['GET'])
def petition_spider(request, spider, session):
    """
    Scraped and created petitions
    """

    payload = {'spider_name': spider, 'url': unquote_plus(utils.spider_url[spider] % session)}
    r = requests.get('http://localhost:9080/crawl.json?', params=payload)
    spider_response = r.json()['items']

    session_obj = get_object_or_404(Session, session_id=session)
    created_petitions = []
    
    for item in spider_response:
        
        issue_obj = get_object_or_404(Issue, issue_id=item['issue_id'], session=session_obj)
        #member_obj = get_object_or_404(Member, pm_id=item['issue_id'])
        petition_obj, created = Petition.objects.update_or_create(
            petition_id=item['petition_id'], 
            defaults={
                'issue': issue_obj,
                #'date_created': dateutil.parser.parse(item['date_created'], tzinfos={'UTC': 0}),
                'date_created': pytz.timezone("UTC").localize(parse_datetime(item['date_created']), is_dst=None)
                #'date_created': parse_datetime(item['date_created'])                
            })
        for signature in item['signatures']:            
            member_obj = get_object_or_404(Member, member_id=signature['member_id'])

            
            signature_obj, created = Signature.objects.update_or_create(
                petition=petition_obj,
                member=member_obj,
                defaults={                    
                    'stance': signature['signature'].lower()
                })            

    return Response(r.json()['items'])

@api_view(['GET'])
def scrape_all(request, session):

    response = (
        session_spider(request, spider='session') and
        committee_spider(request, spider='committeestee') and
        party_spider(request, spider='party') and
        member_spider(request, spider='member', session=session) and
        issue_spider(request, spider='issue', session=session) and
        petition_spider(request, spider='petition', session=session) and
        committee_meeting_spider(request, spider='committee_meeting', session=session)
   )    
    return response


class SessionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.    
    """
    lookup_field = 'session_id'
    queryset = Session.objects.all().order_by('-session_id')
    serializer_class = SessionSerializer
    
    """
    @detail_route()
    def issues(self, request, session_id):
    
        Returns a list of all the group names that the given
        user belongs to.
    
        
        session = self.get_object()
        issues = session.issue_set.all()
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)
    """


class IssueFilter(filters.FilterSet):

    session = django_filters.CharFilter(name="session__session_id")

    class Meta:
        model = Issue
        fields = ['session']

class IssueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.    
    """
    lookup_field = 'issue_id'
    queryset = Issue.objects.all().order_by('-issue_id')
    serializer_class = IssueSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = IssueFilter

    """
    @detail_route()
    def petitions(self, request, issue_id):
       
        Returns a list of all the group names that the given
        user belongs to.
       
               
        
        issue = self.get_object()
        petitions = issue.petition_set.all()
        serializer = PetitionSerializer(petitions, many=True)
        return Response(serializer.data)
    """

class PetitionFilter(filters.FilterSet):

    issue = django_filters.CharFilter(name="issue__issue_id")
    session = django_filters.CharFilter(name="issue__session__session_id")
    class Meta:
        model = Petition
        fields = ['issue', 'session']

class PetitionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    lookup_field = 'petition_id'
    queryset = Petition.objects.all().order_by('-petition_id')
    serializer_class = PetitionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PetitionFilter


class SignatureFilter(filters.FilterSet):

    member = django_filters.CharFilter(name="member__member_id")
    #session = django_filters.CharFilter(name="petition__issue__session__session_id")

    class Meta:
        model = Signature
        fields = ['member', 'stance']

class SignatureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.        
    """

    queryset = Signature.objects.all()        
    serializer_class = SignatureSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SignatureFilter


class MemberFilter(filters.FilterSet):

    #session = django_filters.CharFilter(name="member__pm_id")
    session = django_filters.CharFilter(name="seat__session__session_id")

    class Meta:
        model = Member
        fields = ['session']

class MemberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.       
    """
    lookup_field = 'member_id'

    #queryset = Member.objects.all()
    queryset = Member.objects.annotate(total_signatures=Count('signature'))
    serializer_class = MemberSerializer    

    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = MemberFilter   

class SeatFilter(filters.FilterSet):

    class Meta:
        model = Seat
        fields = ['role']

class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.    
    """
    queryset = Seat.objects.all().order_by('member')
    serializer_class = SeatSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SeatFilter   

class CommitteeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.    
    """
    queryset = Committee.objects.all().order_by('committee_id')
    serializer_class = CommitteeSerializer

class CommitteeMeetingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.    
    """
    queryset = CommitteeMeeting.objects.all().order_by('meeting_id')
    serializer_class = CommitteeMeetingSerializer

class PartyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.        
    """
    queryset = Party.objects.all().order_by('name')
    serializer_class = PartySerializer

