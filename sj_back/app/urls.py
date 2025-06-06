from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import pinnedChatsService
from . import views

from .views import (
    UserViewSet,
    ResumeViewSet,
    CommentViewSet,
    IssueViewSet,
    CompanyViewSet,
    JobViewSet,
    JobApplicationViewSet,
    ResumeApplicationViewSet,
    AuctionViewSet,
    AuctionBidViewSet,
    AuctionParticipantViewSet,
    AuctionConfirmationViewSet,
    ChatViewSet,
    MessageViewSet,
    NotificationViewSet,
    PinnedChatViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'resumes', ResumeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'job_applications', JobApplicationViewSet)
router.register(r'resume_applications', ResumeApplicationViewSet)
router.register(r'auctions', AuctionViewSet)
router.register(r'auction-bids', AuctionBidViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r"pinned-chats", PinnedChatViewSet)
router.register(r'auction-confirmations', AuctionConfirmationViewSet)
router.register(r'auction-participants', AuctionParticipantViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('pinned-chats/user/<int:user_id>/', pinnedChatsService.get_pinned_chats, name='get_pinned_chats'),
    path('pinned-chats/', pinnedChatsService.create_pinned_chat, name='create_pinned_chat'),
    path('pinned-chats/user/<int:user_id>/chat/<int:chat_id>/', pinnedChatsService.delete_pinned_chat, name='delete_pinned_chat'),
    path('newsletter/subscribe/', views.subscribe_newsletter, name='newsletter_subscribe'),

]
