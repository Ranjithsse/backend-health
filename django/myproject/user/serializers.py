import random
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import CustomUser, Case, ExplainabilityData, Notification, FAQ, LegalDocument, Achievement, UserAchievement

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source='message')
    time = serializers.SerializerMethodField()
    created_at_human = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'title', 'description', 'time', 'type', 'is_read', 'created_at', 'created_at_human')

    def get_time(self, obj):
        return obj.created_at.strftime("%I:%M %p")

    def get_created_at_human(self, obj):
        # Very simple human readable time
        now = timezone.now()
        diff = now - obj.created_at
        if diff.days == 0:
            if diff.seconds < 3600:
                return f"{diff.seconds // 60} min ago"
            else:
                return f"{diff.seconds // 3600} hours ago"
        elif diff.days == 1:
            return "Yesterday"
        else:
            return f"{diff.days} days ago"

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class LegalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = '__all__'

class ExplainabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExplainabilityData
        fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement_details = AchievementSerializer(source='achievement', read_only=True)

    class Meta:
        model = UserAchievement
        fields = ('id', 'achievement', 'achievement_details', 'is_unlocked', 'date_earned')
        read_only_fields = ('achievement_details',)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True, required=False)
    hospital_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    specialization = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'hospital_name', 'specialization', 'full_name', 'role',
            'email_notifications', 'prediction_sensitivity', 'show_confidence_intervals', 'include_experimental_models',
            'xp_points', 'level', 'xp_in_level'
        )

    def to_internal_value(self, data):
        data = data.copy()
        if 'hospital' in data and 'hospital_name' not in data:
            data['hospital_name'] = data.pop('hospital')
        if 'specialty' in data and 'specialization' not in data:
            data['specialization'] = data.pop('specialty')
        return super().to_internal_value(data)

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', '')
        first_name = ""
        last_name = ""
        if full_name:
            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0]
            if len(name_parts) > 1:
                last_name = name_parts[1]

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            hospital_name=validated_data.get('hospital_name', ''),
            specialization=validated_data.get('specialization', ''),
            role=validated_data.get('role', 'PROVIDER'),
            first_name=first_name,
            last_name=last_name
        )
        return user

class CaseSerializer(serializers.ModelSerializer):
    doctor_username = serializers.ReadOnlyField(source='doctor.username')

    patient_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    patient_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    status = serializers.CharField(required=False, allow_blank=True)
    date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Case
        fields = '__all__'
        read_only_fields = ('doctor',)

    def to_internal_value(self, data):
        # Create a copy to avoid mutating the original QueryDict/Dict if needed
        data = data.copy()
        
        # Map camelCase to snake_case to support Android app field names
        field_mapping = {
            'patientId': 'patient_id',
            'patientName': 'patient_name',
            'oneYearPrediction': 'one_year_prediction',
            'oneYearRisk': 'one_year_risk',
            'oneYearInsight': 'one_year_insight',
            'threeYearPrediction': 'three_year_prediction',
            'threeYearRisk': 'three_year_risk',
            'threeYearInsight': 'three_year_insight',
            'fiveYearPrediction': 'five_year_prediction',
            'fiveYearRisk': 'five_year_risk',
            'fiveYearInsight': 'five_year_insight',
            'vascularity': 'vascularity',
            'inflammation': 'inflammation',
            'interventionType': 'intervention_type',
            'monitoringLevel': 'monitoring_level',
            'providerNotes': 'provider_notes',
            'treatmentType': 'treatment_type',
            'primaryMedication': 'primary_medication',
            'dosage': 'dosage',
            'duration': 'duration',
            'bloodPressure': 'blood_pressure',
            'glucoseLevel': 'glucose_level',
            'smokingStatus': 'smoking_status',
            'bloodGroup': 'blood_group',
            'physicalActivity': 'physical_activity',
            'primarySystem': 'primary_system',
            'healthStatus': 'health_status',
            'followUpDate': 'follow_up_date',
            'fileUri': 'file_uri',
            'riskLevel': 'risk_level',
            'healthyTissuePct': 'healthy_tissue_pct',
            'fibrousTissuePct': 'fibrous_tissue_pct',
            'inflamedTissuePct': 'inflamed_tissue_pct',
            'age': 'age',
            'gender': 'gender'
        }
        
        for camel, snake in field_mapping.items():
            if camel in data and snake not in data:
                data[snake] = data.pop(camel)
        
        # Ensure mandatory fields have defaults if empty
        if not data.get('patient_id') or data.get('patient_id') == "":
            data['patient_id'] = f"P-{random.randint(1000, 9999)}"
        if not data.get('patient_name') or data.get('patient_name') == "":
            data['patient_name'] = "Anonymous Patient"
        if not data.get('status') or data.get('status') == "":
            data['status'] = "Pending"
        if not data.get('date') or data.get('date') == "":
            from django.utils import timezone
            data['date'] = timezone.now().date().strftime("%Y-%m-%d")
        
        # Remove 'id' if it's 0 or None (Android defaults to 0)
        if 'id' in data and (data['id'] == 0 or data['id'] == '0' or data['id'] is None):
            data.pop('id')

        return super().to_internal_value(data)
