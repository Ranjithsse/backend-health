from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('PROVIDER', 'Healthcare Provider'),
        ('PATIENT', 'Patient'),
        ('LAB', 'Lab Technician'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PROVIDER')
    hospital_name = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    
    # Settings Preferences
    email_notifications = models.BooleanField(default=True)
    prediction_sensitivity = models.CharField(max_length=100, default='Standard (Balanced)')
    show_confidence_intervals = models.BooleanField(default=True)
    include_experimental_models = models.BooleanField(default=False)
    xp_points = models.IntegerField(default=0)

    @property
    def level(self):
        # Calculation: Level 1 starts at 0 XP, Level 2 starts at 100, etc.
        return (self.xp_points // 100) + 1

    @property
    def xp_in_level(self):
        # Current XP progress within the current level (0-99)
        return self.xp_points % 100

    def __str__(self):
        return self.username

class Case(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cases')
    patient_id = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=255)
    date = models.DateField()
    
    # Demographics
    gender = models.CharField(max_length=20, blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    smoking_status = models.CharField(max_length=50, blank=True, null=True)
    
    # Medical Conditions
    medical_conditions = models.JSONField(default=list, blank=True)
    
    # Vitals & Activity
    physical_activity = models.CharField(max_length=100, blank=True, null=True)
    primary_system = models.CharField(max_length=100, blank=True, null=True)
    blood_pressure = models.CharField(max_length=50, blank=True, null=True)
    glucose_level = models.CharField(max_length=50, blank=True, null=True)
    
    # Imaging & Treatment
    tissue_density = models.CharField(max_length=100, default='Normal')
    calcification = models.CharField(max_length=100, default='Minimal')
    vascularity = models.CharField(max_length=100, default='Good')
    inflammation = models.CharField(max_length=100, default='None')
    primary_medication = models.CharField(max_length=255, default='ACE Inhibitors')
    dosage = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    treatment_type = models.CharField(max_length=100, default='Preventative')
    intervention_type = models.CharField(max_length=100, default='Non-Invasive')
    monitoring_level = models.CharField(max_length=100, default='Standard Monitoring')
    adjuvant_therapy_required = models.BooleanField(default=False)
    
    # Tissue Composition (%)
    healthy_tissue_pct = models.FloatField(default=0.0)
    fibrous_tissue_pct = models.FloatField(default=0.0)
    inflamed_tissue_pct = models.FloatField(default=0.0)
    
    # Prediction Results
    risk_score = models.CharField(max_length=50, blank=True, null=True)
    risk_level = models.CharField(max_length=50, blank=True, null=True)
    accuracy = models.CharField(max_length=50, blank=True, null=True)
    ai_insight = models.TextField(blank=True, null=True)
    
    # Outlook
    one_year_prediction = models.CharField(max_length=10, blank=True, null=True)
    one_year_risk = models.CharField(max_length=20, blank=True, null=True)
    one_year_insight = models.TextField(blank=True, null=True)
    
    three_year_prediction = models.CharField(max_length=10, blank=True, null=True)
    three_year_risk = models.CharField(max_length=20, blank=True, null=True)
    three_year_insight = models.TextField(blank=True, null=True)
    
    five_year_prediction = models.CharField(max_length=10, blank=True, null=True)
    five_year_risk = models.CharField(max_length=20, blank=True, null=True)
    five_year_insight = models.TextField(blank=True, null=True)
    
    provider_notes = models.TextField(blank=True, null=True)
    file_uri = models.CharField(max_length=500, blank=True, null=True)
    clinical_recommendations = models.JSONField(default=list, blank=True)
    health_status = models.CharField(max_length=100, blank=True, null=True)
    follow_up_date = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=100, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Case for {self.patient_name} by Dr. {self.doctor.username}"
class Achievement(models.Model):
    achievement_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon_slug = models.CharField(max_length=100, default='ic_star_badge')
    color_hex = models.CharField(max_length=7, default='#FEF9C3')

    def __str__(self):
        return self.title

class UserAchievement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    is_unlocked = models.BooleanField(default=False)
    date_earned = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} - {self.achievement.title}"
class ExplainabilityData(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name='explainability')
    confidence_score = models.FloatField(default=0.0)
    feature_importance = models.JSONField(default=dict)
    risk_factors = models.JSONField(default=list, blank=True)
    model_reasoning = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Explainability for Case {self.case.id}"

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50, default='INFO') # SUCCESS, INFO, ALERT
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question

class LegalDocument(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
