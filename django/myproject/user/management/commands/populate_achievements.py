from django.core.management.base import BaseCommand
from user.models import Achievement

class Command(BaseCommand):
    help = 'Populate initial achievements with UI metadata'

    def handle(self, *args, **kwargs):
        achievements = [
            {
                'achievement_id': 'first_analysis',
                'title': 'First Analysis',
                'description': 'Completed your first patient risk assessment',
                'icon_slug': 'ic_star_badge',
                'color_hex': '#FEF9C3'
            },
            {
                'achievement_id': 'high_accuracy',
                'title': 'High Accuracy',
                'description': 'Achieved >95% prediction accuracy streak',
                'icon_slug': 'ic_target_badge',
                'color_hex': '#FEE2E2'
            },
            {
                'achievement_id': 'power_user',
                'title': 'Power User',
                'description': 'Analyzed 50+ patient cases',
                'icon_slug': 'ic_bolt_badge',
                'color_hex': '#DBEAFE'
            },
            {
                'achievement_id': 'risk_guardian',
                'title': 'Risk Guardian',
                'description': 'Identified 10 critical high-risk cases',
                'icon_slug': 'ic_shield_check_badge',
                'color_hex': '#DCFCE7'
            },
        ]

        for ach_data in achievements:
            obj, created = Achievement.objects.update_or_create(
                achievement_id=ach_data['achievement_id'],
                defaults={
                    'title': ach_data['title'],
                    'description': ach_data['description'],
                    'icon_slug': ach_data['icon_slug'],
                    'color_hex': ach_data['color_hex'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created achievement: {ach_data['title']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated achievement: {ach_data['title']}"))
