from django.contrib.auth.models import *
from rest_framework import serializers
from api.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group

class PartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Party

class MemberSerializer(serializers.ModelSerializer):
    signatures = serializers.ReadOnlyField(read_only=True)
    
    #party = PartySerializer(read_only=True, many=True)

    class Meta:
        model = Member
        fields = ('member_id', 'name', 'dob', 'signatures')


class IssueSerializer(serializers.HyperlinkedModelSerializer):

    #session = SessionSerializer()

    class Meta:
        model = Issue
        fields = ('issue_id', 'url', 'name', )

class SeatSerializer(serializers.HyperlinkedModelSerializer):
    member = serializers.ReadOnlyField(source='member.name')
    session = serializers.ReadOnlyField(source='session.session_id')
    class Meta:
        model = Seat
        fields = ('session', 'date_from', 'date_to', 'party', 'member', 'role')

class SessionSerializer(serializers.HyperlinkedModelSerializer):
    issues = IssueSerializer(many=True, read_only=True, source='issue_set')
    #issue_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ('session_id', 'date_from', 'date_to', 'issues', 'members')

class CommitteeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Session
        fields = ('committee_id', 'name', 'short_abbr', 'long_abbr')


class IssueSerializer(serializers.HyperlinkedModelSerializer):

    #session = SessionSerializer()

    class Meta:
        model = Issue
        fields = ('issue_id', 'url', 'name', )



class SignatureSerializer(serializers.HyperlinkedModelSerializer):
    member = serializers.ReadOnlyField(source='member.name')
    member_id = serializers.ReadOnlyField(source='member.id')    
    issue = serializers.ReadOnlyField(source='petition.issue.name')
    

    class Meta:
        model = Signature
        fields = ('member', 'member_id', 'stance', 'issue')
    
    

class PetitionSerializer(serializers.HyperlinkedModelSerializer):
    signatures = SignatureSerializer(source='signature_set', many=True)
    issue = IssueSerializer()
    #members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Petition
        fields = ('petition_id', 'signatures', 'issue', 'date_created')

