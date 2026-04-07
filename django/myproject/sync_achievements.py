import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from user.models import Achievement

achievements = [
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

for a in achievements:
    obj, created = Achievement.objects.update_or_create(
        achievement_id=a['id'],
        defaults={
            'title': a['title'],
            'description': a['desc'],
            'icon_slug': a['icon'],
            'color_hex': a['color']
        }
    )
    if created:
        print(f"Created achievement: {a['title']}")
    else:
        print(f"Updated achievement: {a['title']}")
