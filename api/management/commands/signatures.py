from django.core.management.base import BaseCommand, CommandError
from api.models import *
from django.db.models import Count

class Command(BaseCommand):
    help = 'Show total signatures'

    def handle(self, *args, **options):
        all_members = Member.objects.all()
        member_list = []
        
        for member in all_members:
            signatures = Signature.objects.filter(member=member)

            """
            total = signatures \
                .annotate(total=Count('stance')) \
                .order_by('stance')

            for result in total:
                print(result)

            """

            total = signatures \
                .values('stance') \
                .annotate(total=Count('stance')) \
                .order_by('stance')
            
            member_list.append({'member': member.name, 'signatures': total})

        print(member_list)