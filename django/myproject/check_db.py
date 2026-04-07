import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from user.models import Achievement, UserAchievement, CustomUser

print("--- Achievements ---")
for a in Achievement.objects.all():
    print(f"ID: {a.achievement_id}, Title: {a.title}, Icon: {a.icon_slug}, Color: {a.color_hex}")

print("\n--- User Achievements ---")
for ua in UserAchievement.objects.all():
    print(f"User: {ua.user.username}, Achievement: {ua.achievement.achievement_id}, Unlocked: {ua.is_unlocked}")
