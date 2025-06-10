from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import base64
from .models import NewsletterSubscriber

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
    NewsletterSubscriberSerializer,
)

@csrf_exempt
@require_http_methods(["POST"])
def subscribe_newsletter(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()

        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email address is required'
            }, status=400)

        # Check if email already exists
        if NewsletterSubscriber.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'This email is already subscribed to our newsletter'
            }, status=400)

        subscriber = NewsletterSubscriber.objects.create(email=email)

        try:
            # Context for the email template
            context = {
                'email': email,
                'company_name': "Student's Job",
                'website_url': 'https://sjf-three.vercel.app/',  # Your frontend URL
                'year': 2025,
            }

            html_content = render_to_string('emails/newsletter_welcome.html', context)
            text_content = render_to_string('emails/newsletter_welcome.txt', context)  # Plain text version

            subject = "🎉 Welcome to Student's Job Newsletter!"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [email]

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return JsonResponse({
                'success': True,
                'message': 'Successfully subscribed! Check your email for confirmation.'
            })

        except Exception as email_error:
            print(f"Email sending failed: {email_error}")
            return JsonResponse({
                'success': True,
                'message': 'Successfully subscribed! (Email confirmation may be delayed)'
            })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)

    except Exception as e:
        print(f"Newsletter subscription error: {e}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again later.'
        }, status=500)


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
