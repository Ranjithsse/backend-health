from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from user.models import Case
import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with mock case history from HistoryManager.java'

    def handle(self, *args, **kwargs):
        # Ensure we have a default doctor for these mock cases
        doctor, created = User.objects.get_or_create(
            username='dr_smith',
            defaults={
                'email': 'smith@healthmonitor.ai',
                'hospital_name': 'Central Health Institute',
                'specialization': 'Cardiology'
            }
        )
        if created:
            doctor.set_password('password123')
            doctor.save()
            self.stdout.write(self.style.SUCCESS('Created default doctor: dr_smith'))

        mock_cases = [
            {
                "patient_id": "P-1020",
                "patient_name": "Robert Wilson",
                "date": datetime.date(2025, 1, 20),
                "gender": "Male",
                "age": "45",
                "primary_system": "Cardiovascular",
                "risk_level": "High",
                "risk_score": "92%",
                "one_year_prediction": "12.5%",
                "one_year_risk": "High",
                "intervention_type": "Surgical",
                "monitoring_level": "Intensive",
                "provider_notes": "Patient shows significant arterial thickening. Immediate follow-up required."
            },
            {
                "patient_id": "P-1021",
                "patient_name": "Emily Davis",
                "date": datetime.date(2025, 1, 19),
                "gender": "Female",
                "age": "32",
                "primary_system": "Respiratory",
                "risk_level": "Low",
                "risk_score": "15%",
                "one_year_prediction": "98.2%",
                "one_year_risk": "Low",
                "intervention_type": "Non-Invasive",
                "monitoring_level": "Standard",
                "provider_notes": "Routine check-up. All parameters within normal range."
            },
            {
                "patient_id": "P-1022",
                "patient_name": "Michael Brown",
                "date": datetime.date(2025, 1, 18),
                "gender": "Male",
                "age": "58",
                "primary_system": "Neurological",
                "risk_level": "Moderate",
                "risk_score": "45%",
                "one_year_prediction": "85.5%",
                "one_year_risk": "Moderate",
                "intervention_type": "Pharmacological",
                "monitoring_level": "Bi-weekly",
                "provider_notes": "Monitor cognitive response to new medication."
            }
        ]

        for item in mock_cases:
            case, created = Case.objects.get_or_create(
                patient_id=item['patient_id'],
                doctor=doctor,
                defaults=item
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created history for: {item["patient_name"]}'))
            else:
                for key, value in item.items():
                    setattr(case, key, value)
                case.save()
                self.stdout.write(self.style.WARNING(f'Updated history for: {item["patient_name"]}'))
