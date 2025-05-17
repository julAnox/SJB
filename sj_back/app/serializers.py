from rest_framework import serializers
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "date_of_birth",
            "phone",
            "country",
            "region",
            "district",
            "publish_phone",
            "publish_status",
            "role",
            "password",
            "created_at",
            "updated_at",
            "last_login",
            "last_signup",
            "is_online",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": False, "allow_blank": True},
            "last_name": {"required": False, "allow_blank": True},
            "avatar": {"required": False, "allow_blank": True},
            "date_of_birth": {"required": False, "allow_blank": True},
            "phone": {"required": False, "allow_blank": True},
            "country": {"required": False, "allow_blank": True},
            "region": {"required": False, "allow_blank": True},
            "district": {"required": False, "allow_blank": True},
            "publish_phone": {"required": False},
            "publish_status": {"required": False},
            "password": {"required": False},
            "role": {"required": False},
            "last_login": {"read_only": True},
            "last_signup": {"read_only": True},
            "is_online": {"read_only": True},
        }

    def create(self, validated_data):
        # Set default values for optional fields
        validated_data.setdefault("first_name", "")
        validated_data.setdefault("last_name", "")
        validated_data.setdefault("avatar", "")
        validated_data.setdefault("role", "student")
        validated_data.setdefault("date_of_birth", "")
        validated_data.setdefault("phone", "")
        validated_data.setdefault("country", "")
        validated_data.setdefault("region", "")
        validated_data.setdefault("district", "")
        validated_data.setdefault("publish_phone", False)
        validated_data.setdefault("publish_status", False)

        return User.objects.create(**validated_data)


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            "id",
            "user",
            "gender",
            "profession",
            "experience",
            "education",
            "institutionName",
            "graduationYear",
            "specialization",
            "skills",
            "contacts",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "stars", "content", "likes"]


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "user", "issue", "solution"]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "user",
            "name",
            "logo",
            "description",
            "website",
            "industry",
            "size",
            "founded_year",
            "status",
            "created_at",
            "updated_at",
        ]


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "company",
            "title",
            "description",
            "requirements",
            "salary_min",
            "salary_max",
            "city",
            "metro",
            "type",
            "schedule",
            "experiense",
            "status",
            "created_at",
            "updated_at",
            "type_of_money",
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id",
            "user",
            "job",
            "resume",
            "company",
            "cover_letter",
            "status",
            "created_at",
            "updated_at",
        ]


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = [
            "id",
            "application",
            "status",
            "start_time",
            "current_stage",
            "stage_end_time",
            "created_at",
            "updated_at",
        ]


class AuctionBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionBid
        fields = [
            "id",
            "auction",
            "company",
            "stage",
            "value",
            "timestamp",
        ]


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = [
            "id",
            "application",
            "status",
            "created_at",
            "updated_at",
        ]


class MessageSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "chat",
            "sender",
            "content",
            "message_type",
            "metadata",
            "file",
            "file_url",
            "read",
            "created_at",
            "updated_at",
        ]

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        elif obj.metadata and 'fileUrl' in obj.metadata:
            return obj.metadata['fileUrl']
        return None


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "type",
            "content",
            "related_id",
            "read",
            "created_at",
        ]


class PinnedChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinnedChat
        fields = [
            "id",
            "user",
            "chat",
            "created_at",
        ]
