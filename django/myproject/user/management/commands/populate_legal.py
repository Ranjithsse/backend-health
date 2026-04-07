from django.core.management.base import BaseCommand
from user.models import LegalDocument

class Command(BaseCommand):
    help = 'Populate initial legal documents from Android layout'

    def handle(self, *args, **kwargs):
        docs = [
            {
                "slug": "liability-statement",
                "title": "Liability Statement",
                "content": "Health Monitor Prediction is a support tool. The treating clinician maintains full responsibility for all medical decisions and outcomes."
            },
            {
                "slug": "data-privacy",
                "title": "Data Privacy",
                "content": "Patient data is processed using end-to-end encryption and stored in HIPAA-compliant servers. Data is retained for 7 years."
            },
            {
                "slug": "algorithm-transparency",
                "title": "Algorithm Transparency",
                "content": "The prediction model (v2.4) was trained on a dataset of 54,000 cases with a verified accuracy of 96.5% (AUC 0.94)."
            }
        ]

        for item in docs:
            doc, created = LegalDocument.objects.get_or_create(
                slug=item['slug'],
                defaults={'title': item['title'], 'content': item['content']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created legal document: {item["title"]}'))
            else:
                doc.title = item['title']
                doc.content = item['content']
                doc.save()
                self.stdout.write(self.style.WARNING(f'Updated legal document: {item["title"]}'))
