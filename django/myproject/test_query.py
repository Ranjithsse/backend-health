from user.models import Case
for c in Case.objects.all():
    print(f'ID={c.id} patID="{c.patient_id}" date="{c.date}" status="{c.status}"')
