from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

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


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    fields = [
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
        "last_signup",
        "last_login",
    ]
    list_display = ["id", "email", "first_name", "last_name", "role", "is_online"]
    search_fields = ["email", "first_name", "last_name"]
    list_filter = ["role", "is_online"]


@admin.register(Resume)
class AdminResume(admin.ModelAdmin):
    fields = [
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
    ]
    list_display = ["id", "user", "profession", "graduationYear"]
    search_fields = ["user__email", "profession"]
    list_filter = ["gender", "graduationYear"]


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    fields = [
        "user",
        "stars",
        "content",
        "likes",
    ]
    list_display = ["id", "user", "stars", "likes"]
    search_fields = ["user__email", "content"]
    list_filter = ["stars"]


@admin.register(Issue)
class AdminIssue(admin.ModelAdmin):
    fields = [
        "user",
        "issue",
        "solution",
    ]
    list_display = ["id", "user", "issue"]
    search_fields = ["user__email", "issue", "solution"]


@admin.register(Company)
class AdminCompany(admin.ModelAdmin):
    fields = [
        "user",
        "name",
        "logo",
        "description",
        "website",
        "industry",
        "size",
        "founded_year",
        "status",
    ]
    list_display = ["id", "name", "industry", "size", "status"]
    search_fields = ["name", "industry"]
    list_filter = ["status", "industry", "size"]


@admin.register(Job)
class AdminJob(admin.ModelAdmin):
    fields = [
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
        "type_of_money",
    ]
    list_display = ["id", "company", "title", "city", "salary_range", "status"]
    search_fields = ["title", "company__name", "city"]
    list_filter = ["status", "type", "schedule", "city"]

    def salary_range(self, obj):
        return f"{obj.salary_min} - {obj.salary_max} {obj.type_of_money}"


@admin.register(Application)
class AdminApplication(admin.ModelAdmin):
    fields = [
        "user",
        "job",
        "resume",
        # "company",
        "cover_letter",
        "status",
    ]
    list_display = ["id", "user", "job", "status", "created_at"]
    search_fields = ["user__email", "job__title"]
    list_filter = ["status"]


@admin.register(Auction)
class AdminAuction(admin.ModelAdmin):
    fields = [
        "application",
        "status",
        "start_time",
        "current_stage",
        "stage_end_time",
    ]
    list_display = ["id", "application", "status", "current_stage"]
    search_fields = ["application__user__email", "status"]
    list_filter = ["status", "current_stage"]


@admin.register(AuctionBid)
class AdminAuctionBid(admin.ModelAdmin):
    fields = [
        "auction",
        "company",
        "stage",
        "value",
        "timestamp",
    ]
    list_display = ["id", "auction", "company", "stage"]
    search_fields = ["company__name"]
    list_filter = ["stage"]


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    fields = [
        "application",
        "status",
    ]
    list_display = ["id", "application", "status", "created_at", "message_count"]
    search_fields = ["application__id", "status"]
    list_filter = ["status"]

    def message_count(self, obj):
        count = Message.objects.filter(chat=obj).count()
        return count

    message_count.short_description = "Messages"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = [
        "chat",
        "sender",
        "content",
        "message_type",
        "metadata",
        "file",
        "read",
    ]
    list_display = ["id", "chat", "sender", "message_type", "read", "created_at", "file_preview"]
    list_filter = ["read", "message_type"]
    search_fields = ["content", "sender__email"]
    readonly_fields = ["file_preview_large"]

    def file_preview(self, obj):
        """Display a thumbnail or icon for files in the list view"""
        if obj.message_type == 'image' and obj.get_file_url():
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.get_file_url())
        elif obj.message_type == 'document' and obj.get_file_url():
            return format_html('<a href="{}" target="_blank">📄 {}</a>', obj.get_file_url(),
                               obj.get_file_name() or "Document")
        return "-"

    file_preview.short_description = "File"

    def file_preview_large(self, obj):
        """Display a larger preview in the detail view"""
        if obj.message_type == 'image' and obj.get_file_url():
            return format_html('<img src="{}" style="max-width: 500px; max-height: 300px;" />', obj.get_file_url())
        elif obj.message_type == 'document' and obj.get_file_url():
            return format_html('<a href="{}" class="button" target="_blank">Download: {}</a>',
                               obj.get_file_url(), obj.get_file_name() or "Document")
        return "No file attached"

    file_preview_large.short_description = "File Preview"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    fields = [
        "user",
        "type",
        "content",
        "related_id",
        "read",
    ]
    list_display = ["id", "user", "type", "read", "created_at"]
    list_filter = ["read", "type"]
    search_fields = ["content", "user__email"]


@admin.register(PinnedChat)
class PinnedChatAdmin(admin.ModelAdmin):
    fields = [
        "user",
        "chat",
    ]
    list_display = ["id", "user", "chat", "created_at"]
    search_fields = ["user__email", "chat__id"]
    list_filter = ["user"]
