from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import (
    User,
    Resume,
    Comment,
    Issue,
    Company,
    Job,
    Application,
    Auction,
    AuctionBid,
    Chat,
    Message,
    Notification,
    PinnedChat,
)
from .serializers import (
    UserSerializer,
    ResumeSerializer,
    CommentSerializer,
    IssueSerializer,
    CompanySerializer,
    JobSerializer,
    ApplicationSerializer,
    AuctionSerializer,
    AuctionBidSerializer,
    ChatSerializer,
    MessageSerializer,
    NotificationSerializer,
    PinnedChatSerializer,
)

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ["email", "password"]


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ResumeFilter(filters.FilterSet):
    class Meta:
        model = Resume
        fields = ["user"]


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ResumeFilter


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class CompanyFilter(filters.FilterSet):
    class Meta:
        model = Company
        fields = ["user"]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CompanyFilter


class JobFilter(filters.FilterSet):
    class Meta:
        model = Job
        fields = ["company", "status"]


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = JobFilter


class ApplicationFilter(filters.FilterSet):
    class Meta:
        model = Application
        fields = ["user", "job", "status"]


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ApplicationFilter


class AuctionFilter(filters.FilterSet):
    class Meta:
        model = Auction
        fields = ["application", "status"]


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuctionFilter


class AuctionBidFilter(filters.FilterSet):
    class Meta:
        model = AuctionBid
        fields = ["auction", "company", "stage"]


class AuctionBidViewSet(viewsets.ModelViewSet):
    queryset = AuctionBid.objects.all()
    serializer_class = AuctionBidSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuctionBidFilter


class ChatFilter(filters.FilterSet):
    class Meta:
        model = Chat
        fields = ["application", "status"]


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ChatFilter

    @action(detail=True, methods=['post'])
    def mark_all_read(self, request, pk=None):
        """Mark all messages in a chat as read for a specific user."""
        try:
            chat = self.get_object()
            user_id = request.data.get('user_id')

            if not user_id:
                return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Get all unread messages in this chat that were not sent by the user
            messages = Message.objects.filter(
                chat=chat,
                read=False
            ).exclude(sender=user_id)

            # Update read status
            count = messages.count()
            messages.update(read=True)

            return Response({
                'success': True,
                'count': count,
                'message': f'Marked {count} messages as read'
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread messages for a user across all chats."""
        try:
            user_id = request.query_params.get('user_id')

            if not user_id:
                return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Get all chats relevant to this user
            user_chats = []

            # If user is a student, get chats for their applications
            user = get_object_or_404(User, id=user_id)
            if user.role == 'student':
                applications = Application.objects.filter(user=user_id)
                user_chats = Chat.objects.filter(application__in=applications)

            # If user is a company, get chats for jobs they posted
            elif user.role == 'company':
                # Get company for this user
                try:
                    company = Company.objects.get(user=user_id)
                    # Get jobs for this company
                    jobs = Job.objects.filter(company=company.id)
                    # Get applications for these jobs
                    applications = Application.objects.filter(job__in=jobs)
                    # Get chats for these applications
                    user_chats = Chat.objects.filter(application__in=applications)
                except Company.DoesNotExist:
                    # User might not have a company yet
                    pass

            # Count unread messages across all relevant chats
            unread_count = Message.objects.filter(
                chat__in=user_chats,
                read=False
            ).exclude(sender=user_id).count()

            return Response({'unread_count': unread_count})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MessageFilter(filters.FilterSet):
    class Meta:
        model = Message
        fields = ["chat", "sender", "read", "message_type"]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MessageFilter

    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        """Mark a specific message as read."""
        message = self.get_object()
        message.read = True
        message.save()
        serializer = self.get_serializer(message)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all messages in a chat as read for a specific user."""
        chat_id = request.data.get('chat_id')
        user_id = request.data.get('user_id')

        if not chat_id or not user_id:
            return Response(
                {"error": "chat_id and user_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all unread messages in the chat that were not sent by the user
        messages = Message.objects.filter(
            chat_id=chat_id,
            read=False
        ).exclude(sender=user_id)

        # Mark all as read
        count = messages.count()
        messages.update(read=True)

        return Response({
            "success": True,
            "marked_count": count,
            "message": f"Marked {count} messages as read in chat {chat_id}"
        })


class NotificationFilter(filters.FilterSet):
    class Meta:
        model = Notification
        fields = ["user", "type", "read"]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NotificationFilter

    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        """Mark a notification as read."""
        notification = self.get_object()
        notification.read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read for a user."""
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all unread notifications for this user
        notifications = Notification.objects.filter(
            user=user_id,
            read=False
        )

        # Mark all as read
        count = notifications.count()
        notifications.update(read=True)

        return Response({
            "success": True,
            "marked_count": count,
            "message": f"Marked {count} notifications as read for user {user_id}"
        })

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications for a user."""
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Count unread notifications
        count = Notification.objects.filter(
            user=user_id,
            read=False
        ).count()

        return Response({"unread_count": count})


class PinnedChatFilter(filters.FilterSet):
    class Meta:
        model = PinnedChat
        fields = ["user", "chat"]


class PinnedChatViewSet(viewsets.ModelViewSet):
    queryset = PinnedChat.objects.all()
    serializer_class = PinnedChatSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PinnedChatFilter

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get all pinned chats for a specific user."""
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        pinned_chats = PinnedChat.objects.filter(user=user_id)
        serializer = self.get_serializer(pinned_chats, many=True)
        return Response(serializer.data)

