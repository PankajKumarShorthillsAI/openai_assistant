from django.urls import path
from .views import CreateAssistant,ChatAssistant,CreateAssistantV2,ChatAssistantV2

urlpatterns = [
    path('create_assistant/', CreateAssistant.as_view(), name='create_assistant'),
    path('chat_assistant/', ChatAssistant.as_view(), name='chat_assistant'),
    path('v2/create_assistant/', CreateAssistantV2.as_view(), name='create_assistant'),
    path('v2/chat_assistant/', ChatAssistantV2.as_view(), name='chat_assistant'),
]