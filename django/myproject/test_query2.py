from user.models import Case
with open(r'c:\Users\Sugumar D\OneDrive\Desktop\django\myproject\db_dump.txt', 'w') as f:
    for c in Case.objects.all().order_by('-id'):
        f.write(f'ID={c.id} patID="{c.patient_id}" patName="{c.patient_name}" date="{c.date}" status="{c.status}"\n')
