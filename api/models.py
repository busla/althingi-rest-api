from django.db import models
from django.db.models import Count, Max, Q

class Session(models.Model):
    session_id = models.IntegerField(null=True, blank=True)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)

    def _get_members(self):

        members = Member.objects.filter(seat__session=self) \
            .values() \
            .annotate(total=Count('member_id')) \
            .order_by('-total')
        
        return members

    members = property(_get_members)

    class Meta:
        ordering = ('session_id',)
    
    def __str__(self):
        return self.session_id

class Member(models.Model):
    member_id = models.IntegerField(null=True, blank=True)
    #image = models.ImageField(upload_to='uploads/')
    image_url = models.URLField()
    name = models.CharField(max_length=254)
    dob = models.DateField()
    party = models.ManyToManyField(
        'Party',
        through='Seat',
        through_fields=('member', 'party'),
    )    
    
    def _get_total_signatures(self):

        total_signatures = Signature.objects \
            .filter(member=self) \
            .values('stance') \
            .annotate(total=Count('stance')) \
            .order_by('stance')

        return total_signatures

    signatures = property(_get_total_signatures)

    def _get_total_absence(self):

        total_absence = Signature.objects \
            .filter(member=self) \
            .filter(Q(stance='fjarverandi') | Q(stance='boðaði fjarvist')) \
            .count()
        return total_absence

    absence = property(_get_total_absence)


    def __str__(self):
        return self.name

class Issue(models.Model):
    issue_id = models.IntegerField(null=True, blank=True)
    url = models.URLField()
    name = models.CharField(max_length=254)
    #session = models.ForeignKey(Session)
    session = models.ForeignKey(Session)
    
    def __str__(self):
        return self.name

class Petition(models.Model):
    petition_id = models.IntegerField(null=True, blank=True)
    issue = models.ForeignKey(Issue)
    date_created = models.DateTimeField()

    members = models.ManyToManyField(
        Member,
        through='Signature',
        through_fields=('petition', 'member'),
    )    

    def __str__(self):
        return self.issue.name

class Signature(models.Model):
    """
    SIGNATURES = (
        ('yes', 'já'),
        ('no', 'nei'),
        ('pass', 'greiðir ekki atkvæði'),
        ('absent', 'fjarverandi'),
        ('permission', 'boðaði fjarvist'),
    )  
    """      
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    #stance = models.CharField(max_length=4, choices=SIGNATURES)
    stance = models.CharField(max_length=254)

    def __str__(self):
        return "%s - %s" % (self.member.name, self.stance)

class Party(models.Model):
    party_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=254)
    short_name = models.CharField(max_length=254)
    long_name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

class Seat(models.Model):

    session = models.ForeignKey(Session)
    date_from = models.DateTimeField(null=True)
    date_to = models.DateTimeField(null=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)    
    role = models.CharField(max_length=254, null=True, blank=True)

    """
    region model gæti komið síðar, þarf að skoða sögu
    sameiningu kjördæma.
    """
    region = models.CharField(max_length=254, null=True, blank=True)
    seat_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.member.name, self.party.name)

class Committee(models.Model):
    committee_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    short_abbr = models.CharField(max_length=254, null=True, blank=True)
    long_abbr = models.CharField(max_length=254, null=True, blank=True)
    session = models.ManyToManyField(Session)

    def __str__(self):
        return self.name

class CommitteeMeeting(models.Model):
    meeting_id = models.IntegerField(null=True, blank=True)
    session = models.ForeignKey(Session)    
    committee = models.ForeignKey(Committee)    
    date_from = models.DateTimeField(null=True)
    date_to = models.DateTimeField(null=True)
    attended = models.ManyToManyField(Member)

    def __str__(self):
        return "%s - %s" % (self.committee.name, self.attended.all)        