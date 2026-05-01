from django.urls import path
from . import views

urlpatterns = [
    path('auth', views.auth_view),
    path('auth/register', views.register_view),
    path('auth/login', views.login_view),
    # Expenses
    path('expenses', views.expenses_list_or_create),
    path('expenses/bulk', views.expenses_bulk),
    path('expenses/<int:pk>', views.expenses_update_or_delete),
    # Budget
    path('budget', views.budget_get_or_set),
    # Dashboard & AI
    path('dashboard', views.dashboard),
    path('insights', views.insights),
    path('categorize', views.categorize),
    # Upload
    path('upload', views.upload),
    # Email sync
    path('sync/<str:provider_key>', views.email_sync),
    path('sync-status', views.sync_status),
    # Notifications
    path('notification-settings', views.notification_settings),
    # Push
    path('push/vapid-key', views.vapid_key),
    path('push/subscribe', views.push_subscribe),
    path('push/unsubscribe', views.push_unsubscribe),
]
