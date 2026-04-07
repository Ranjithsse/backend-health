from django.core.management.base import BaseCommand
from user.models import FAQ

class Command(BaseCommand):
    help = 'Populate the database with FAQs from HelpSupportActivity.java'

    def handle(self, *args, **kwargs):
        faqs = [
            {
                "question": "How is the AI confidence score calculated?",
                "answer": "The confidence score represents the model's certainty based on the quality and completeness of the input data. It factors in data density, historical pattern matching, and variance in the probabilistic output.",
                "order": 1
            },
            {
                "question": "Can I override the AI risk assessment?",
                "answer": "Yes, the AI is designed as a decision-support tool. Clinicians can provide 'Provider Notes' and adjust the clinical plan based on their expert judgment, which the model uses for continuous learning.",
                "order": 2
            },
            {
                "question": "Is the data encrypted at rest?",
                "answer": "All patient health information (PHI) is encrypted using AES-256 standards both in transit and at rest, ensuring full compliance with HIPAA and relevant data protection regulations.",
                "order": 3
            }
        ]

        for item in faqs:
            faq, created = FAQ.objects.get_or_create(
                question=item['question'],
                defaults={'answer': item['answer'], 'order': item['order']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created FAQ: "{item["question"]}"'))
            else:
                faq.answer = item['answer']
                faq.order = item['order']
                faq.save()
                self.stdout.write(self.style.WARNING(f'Updated FAQ: "{item["question"]}"'))
