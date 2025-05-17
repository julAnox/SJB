from django.test import TestCase
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from sj_back.asgi import application
from .models import User, Chat, Message, Application, Job, Company, Resume


class WebSocketTestCase(TestCase):
    """Test case for WebSocket chat functionality."""

    async def test_connect_with_user_id(self):
        # Create a test user
        user = await self.create_test_user()

        # Connect to the WebSocket with the user_id
        communicator = WebsocketCommunicator(application, f"/ws/chat/{user.id}/")
        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        # Disconnect
        await communicator.disconnect()

    async def test_connect_without_user_id(self):
        # Connect to the WebSocket without a user_id
        communicator = WebsocketCommunicator(application, "/ws/chat/")
        connected, _ = await communicator.connect()

        self.assertFalse(connected)

    async def test_send_message(self):
        # Create test data
        test_data = await self.create_test_data()
        user, chat = test_data['user'], test_data['chat']

        # Connect to the WebSocket
        communicator = WebsocketCommunicator(application, f"/ws/chat/{user.id}/")
        connected, _ = await communicator.connect()

        # Receive connection confirmation
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'connection_established')

        # Send a message
        await communicator.send_json_to({
            'type': 'send_message',
            'chat_id': chat.id,
            'content': 'Hello, world!',
            'message_type': 'text',
            'metadata': {}
        })

        # Receive message confirmation
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'message_sent')

        # Check that the message was saved to the database
        message = await self.get_latest_message(chat.id)
        self.assertEqual(message.content, 'Hello, world!')

        # Disconnect
        await communicator.disconnect()

    async def test_typing_status(self):
        # Create test data
        test_data = await self.create_test_data()
        user, chat = test_data['user'], test_data['chat']

        # Connect to the WebSocket
        communicator = WebsocketCommunicator(application, f"/ws/chat/{user.id}/")
        connected, _ = await communicator.connect()

        # Receive connection confirmation
        await communicator.receive_json_from()

        # Send typing status
        await communicator.send_json_to({
            'type': 'typing_status',
            'chat_id': chat.id,
            'is_typing': True
        })

        # Disconnect
        await communicator.disconnect()

    async def test_mark_read(self):
        # Create test data
        test_data = await self.create_test_data()
        user, chat = test_data['user'], test_data['chat']

        # Create an unread message
        message = await self.create_test_message(chat.id, user.id)

        # Connect to the WebSocket
        communicator = WebsocketCommunicator(application, f"/ws/chat/{user.id}/")
        connected, _ = await communicator.connect()

        # Receive connection confirmation
        await communicator.receive_json_from()

        # Mark message as read
        await communicator.send_json_to({
            'type': 'mark_read',
            'chat_id': chat.id,
            'message_id': message.id
        })

        # Receive confirmation
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'marked_read')

        # Check that the message was marked as read
        message = await self.get_message(message.id)
        self.assertTrue(message.read)

        # Disconnect
        await communicator.disconnect()

    # Helper methods

    @database_sync_to_async
    def create_test_user(self):
        return User.objects.create(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            role="student",
            password="password123"
        )

    @database_sync_to_async
    def create_test_data(self):
        """Create a set of test data including users, companies, jobs, applications, and chats."""
        # Create student user
        student = User.objects.create(
            email="student@example.com",
            first_name="Student",
            last_name="User",
            role="student",
            password="password123"
        )

        # Create company user
        company_user = User.objects.create(
            email="company@example.com",
            first_name="Company",
            last_name="User",
            role="company",
            password="password123"
        )

        # Create company
        company = Company.objects.create(
            user=company_user,
            name="Test Company",
            industry="Technology",
            size="Small",
            founded_year=2020,
            status="active"
        )

        # Create job
        job = Job.objects.create(
            company=company,
            title="Test Job",
            description="A test job",
            salary_min=50000,
            salary_max=100000,
            city="Test City",
            metro="Test Metro",
            type="Full-time",
            schedule="Standard",
            experiense=2,
            status="active",
            type_of_money="USD"
        )

        # Create resume
        resume = Resume.objects.create(
            user=student,
            profession="Software Developer",
            experience="5 years",
            education="Bachelor's",
            institutionName="Test University",
            graduationYear="2020",
            specialization="Computer Science",
            skills="Python, Django, React",
            contacts="test@example.com"
        )

        # Create application
        application = Application.objects.create(
            user=student,
            job=job,
            resume=resume,
            cover_letter="Test cover letter",
            status="active"
        )

        # Create chat
        chat = Chat.objects.create(
            application=application,
            status="active"
        )

        return {
            'student': student,
            'company_user': company_user,
            'company': company,
            'job': job,
            'resume': resume,
            'application': application,
            'chat': chat,
            'user': student  # Default user for tests
        }

    @database_sync_to_async
    def create_test_message(self, chat_id, user_id):
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)

        return Message.objects.create(
            chat=chat,
            sender=user,
            content="Test message",
            message_type="text",
            read=False
        )

    @database_sync_to_async
    def get_latest_message(self, chat_id):
        return Message.objects.filter(chat_id=chat_id).order_by('-created_at').first()

    @database_sync_to_async
    def get_message(self, message_id):
        return Message.objects.get(id=message_id)