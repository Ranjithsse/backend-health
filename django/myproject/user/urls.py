from django.urls import path
from .views import (
    RegisterView, LoginView, CaseListCreateView,
    AchievementListView, UserAchievementListView, UnlockAchievementView,
    ExplainabilityDetailView, PredictCaseView, DeleteAccountView,
    PasswordResetRequestView, PasswordResetConfirmView, CaseDetailView,
    DashboardStatsView, NotificationListView, MarkNotificationReadView,
    FAQListView, LegalDocumentListView, ReportDownloadView, HighRiskAlertsView,
    ProfileSettingsView, UpdateProfileSettingsView, AppConfigView, CheckSessionView,
    TissueAnalysisView
)

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('settings/', ProfileSettingsView.as_view(), name='profile-settings'),
    path('settings/update/', UpdateProfileSettingsView.as_view(), name='update-settings'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('legal/', LegalDocumentListView.as_view(), name='legal-docs'),
    path('notifications/', NotificationListView.as_view(), name='notifications-list'),
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-mark-read'),
    path('cases/<int:pk>/download/', ReportDownloadView.as_view(), name='report-download'),
    path('cases/high-risk/', HighRiskAlertsView.as_view(), name='high-risk-alerts'),
    path('dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('cases/', CaseListCreateView.as_view(), name='cases'),
    path('cases/<int:pk>/', CaseDetailView.as_view(), name='case-detail'),
    path('cases/<int:case_id>/predict/', PredictCaseView.as_view(), name='case-predict'),
    path('cases/<int:case_id>/tissue-analysis/', TissueAnalysisView.as_view(), name='tissue-analysis'),
    path('achievements/', AchievementListView.as_view(), name='achievements-list'),
    path('my-achievements/', UserAchievementListView.as_view(), name='user-achievements'),
    path('unlock-achievement/', UnlockAchievementView.as_view(), name='unlock-achievement'),
    path('explainability/<int:case_id>/', ExplainabilityDetailView.as_view(), name='explainability-detail'),
    path('config/', AppConfigView.as_view(), name='app-config'),
    path('auth/check/', CheckSessionView.as_view(), name='auth-check'),
]
