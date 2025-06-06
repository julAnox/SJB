from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import (
    User,
    Resume,
    Comment,
    Issue,
    Company,
    Job,
    JobApplication,
    ResumeApplication,
    Auction,
    AuctionBid,
    AuctionConfirmation,
    AuctionParticipant,
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
    JobApplicationSerializer,
    ResumeApplicationSerializer,
    AuctionSerializer,
    AuctionBidSerializer,
    AuctionConfirmationSerializer,
    AuctionParticipantSerializer,
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
        model = JobApplication
        fields = ["user", "job", "status"]


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ApplicationFilter

    def perform_create(self, serializer):
        """Override create to set company if not provided"""
        if not serializer.validated_data.get('company') and serializer.validated_data.get('job'):
            job = serializer.validated_data['job']
            serializer.save(company=job.company)
        else:
            serializer.save()


class ResumeApplicationFilter(filters.FilterSet):
    class Meta:
        model = ResumeApplication
        fields = ["resume", "company", "status"]


class ResumeApplicationViewSet(viewsets.ModelViewSet):
    queryset = ResumeApplication.objects.all().select_related('resume__user', 'company')
    serializer_class = ResumeApplicationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ResumeApplicationFilter


class AuctionFilter(filters.FilterSet):
    class Meta:
        model = Auction
        fields = ["application", "status"]


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuctionFilter


@action(detail=True, methods=['get'])
def with_details(self, request, pk=None):
    """Get auction with full details including student, companies, and bids"""
    try:
        auction = self.get_object()

        # Get student details
        student_data = None
        if auction.student:
            student = User.objects.get(id=auction.student.id)
            student_data = {
                'id': student.id,
                'firstName': student.first_name,
                'lastName': student.last_name,
                'avatar': student.avatar,
                'profession': 'Software Developer',  # Можно получить из резюме
                'experience': '3+ years'  # Можно получить из резюме
            }

        # Get participating companies
        participants = AuctionParticipant.objects.filter(auction=auction)
        companies_data = []
        for participant in participants:
            company = participant.company
            companies_data.append({
                'id': company.id,
                'name': company.name,
                'logo': company.logo,
                'user_id': company.user.id
            })

        # Get all bids with company details
        bids = AuctionBid.objects.filter(auction=auction).order_by('timestamp')
        bids_data = []
        for bid in bids:
            bids_data.append({
                'id': bid.id,
                'company': {
                    'id': bid.company.id,
                    'name': bid.company.name,
                    'logo': bid.company.logo
                },
                'stage': bid.stage,
                'value': bid.value,
                'timestamp': bid.timestamp,
                'bid_order': bid.bid_order
            })

        response_data = {
            'id': auction.id,
            'status': auction.status,
            'current_stage': auction.current_stage,
            'stage_end_time': auction.stage_end_time,
            'student': student_data,
            'companies': companies_data,
            'bids': bids_data
        }

        return Response(response_data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@action(detail=True, methods=['post'])
def next_stage(self, request, pk=None):
    """Move auction to next stage"""
    try:
        auction = self.get_object()
        next_stage = auction.current_stage + 1

        if next_stage > 4:
            auction.status = 'completed'
            auction.stage_end_time = None
        else:
            auction.stage_end_time = timezone.now() + timezone.timedelta(minutes=1)

        auction.current_stage = next_stage
        auction.save()

        serializer = self.get_serializer(auction)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


class AuctionBidFilter(filters.FilterSet):
    class Meta:
        model = AuctionBid
        fields = ["auction", "company", "stage"]


class AuctionBidViewSet(viewsets.ModelViewSet):
    queryset = AuctionBid.objects.all()
    serializer_class = AuctionBidSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuctionBidFilter


class AuctionConfirmationFilter(filters.FilterSet):
    class Meta:
        model = AuctionConfirmation
        fields = ['student', 'company', 'confirmed']


class AuctionConfirmationViewSet(viewsets.ModelViewSet):
    queryset = AuctionConfirmation.objects.all()
    serializer_class = AuctionConfirmationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuctionConfirmationFilter


class AuctionParticipantViewSet(viewsets.ModelViewSet):
    queryset = AuctionParticipant.objects.all()
    serializer_class = AuctionParticipantSerializer
    filter_backends = (filters.DjangoFilterBackend,)


class ChatFilter(filters.FilterSet):
    class Meta:
        model = Chat
        fields = ["application", "resume_application", "status"]


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

            # Get user
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Initialize chat IDs list
            chat_ids = []

            if user.role == 'student':
                # Get job application chats where student is the applicant
                job_applications = JobApplication.objects.filter(user=user_id)
                job_chat_ids = Chat.objects.filter(
                    application__in=job_applications
                ).values_list('id', flat=True)
                chat_ids.extend(list(job_chat_ids))

                # Get resume application chats where student owns the resume
                user_resumes = Resume.objects.filter(user=user_id)
                resume_applications = ResumeApplication.objects.filter(resume__in=user_resumes)
                resume_chat_ids = Chat.objects.filter(
                    resume_application__in=resume_applications
                ).values_list('id', flat=True)
                chat_ids.extend(list(resume_chat_ids))

            elif user.role == 'company':
                try:
                    company = Company.objects.get(user=user_id)

                    # Get job application chats for jobs posted by this company
                    jobs = Job.objects.filter(company=company.id)
                    job_applications = JobApplication.objects.filter(job__in=jobs)
                    job_chat_ids = Chat.objects.filter(
                        application__in=job_applications
                    ).values_list('id', flat=True)
                    chat_ids.extend(list(job_chat_ids))

                    # Get resume application chats where this company contacted students
                    resume_applications = ResumeApplication.objects.filter(company=company.id)
                    resume_chat_ids = Chat.objects.filter(
                        resume_application__in=resume_applications
                    ).values_list('id', flat=True)
                    chat_ids.extend(list(resume_chat_ids))

                except Company.DoesNotExist:
                    # User doesn't have a company profile yet
                    pass

            # Count unread messages across all relevant chats
            unread_count = Message.objects.filter(
                chat_id__in=chat_ids,
                read=False
            ).exclude(sender=user_id).count()

            return Response({'unread_count': unread_count})

        except Exception as e:
            # Log the actual error for debugging
            import traceback
            print(f"Error in unread_count: {str(e)}")
            print(traceback.format_exc())
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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