import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from user.models import Achievement, UserAchievement, CustomUser
from user.views import check_and_unlock_achievements

# Correct metadata from Image 1
achievements_data = [
    {
        'id': 'first_analysis',
        'title': 'First Analysis',
        'desc': 'Completed your first patient risk assessment',
        'icon': 'ic_star_badge',
        'color': '#FEF9C3'
    },
    {
        'id': 'high_accuracy',
        'title': 'High Accuracy',
        'desc': 'Achieved >95% prediction accuracy streak',
        'icon': 'ic_target_badge',
        'color': '#FEE2E2'
    },
    {
        'id': 'power_user',
        'title': 'Power User',
        'desc': 'Analyzed 50+ patient cases',
        'icon': 'ic_bolt_badge',
        'color': '#DBEAFE'
    },
    {
        'id': 'risk_guardian',
        'title': 'Risk Guardian',
        'desc': 'Identified 10 critical high-risk cases',
        'icon': 'ic_shield_check_badge',
        'color': '#DCFCE7'
    }
]

print("Syncing Achievements Metadata...")
for data in achievements_data:
    obj, created = Achievement.objects.update_or_create(
        achievement_id=data['id'],
        defaults={
            'title': data['title'],
            'description': data['desc'],
            'icon_slug': data['icon'],
            'color_hex': data['color']
        }
    )
    print(f"{'Created' if created else 'Updated'}: {data['title']}")

print("\nTriggering Achievement Checks for all users...")
users = CustomUser.objects.all()
for user in users:
    print(f"Checking user: {user.username}")
    check_and_unlock_achievements(user)

print("\nDone.")
