from django.urls import path
from .views import CreateAssistant,ChatAssistant

urlpatterns = [
    path('create_assistant/', CreateAssistant.as_view(), name='create_assistant'),
    path('chat_assistant/', ChatAssistant.as_view(), name='chat_assistant'),
]