from django.db import models
from django.utils import timezone
from datetime import datetime
from datetime import date
from datetime import time


class User(models.Model):
    email = models.EmailField(max_length=30, unique=True)
    first_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=15, blank=True)
    avatar = models.TextField(default="", blank=True)
    date_of_birth = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True)
    region = models.CharField(max_length=20, blank=True)
    district = models.CharField(max_length=20, blank=True)
    publish_phone = models.BooleanField(default=False)
    publish_status = models.BooleanField(default=False)
    role = models.CharField(max_length=10, default="student")
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_signup = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_online = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id}. {self.first_name} {self.last_name}"


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')],
                              blank=True, null=True)
    profession = models.CharField(max_length=50)
    experience = models.TextField()
    education = models.CharField(max_length=50)
    institutionName = models.CharField(max_length=50)
    graduationYear = models.CharField(max_length=4)
    specialization = models.CharField(max_length=50)
    skills = models.CharField(max_length=255)
    contacts = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id) + ". " + self.user.first_name + " " + self.user.last_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()
    content = models.TextField(default="", max_length=255)
    likes = models.IntegerField()

    def __str__(self) -> str:
        return str(self.id) + ". " + self.user.first_name + " " + self.user.last_name


class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.TextField(default="", max_length=100)
    solution = models.TextField(default="", max_length=100)

    def __str__(self) -> str:
        return str(self.id) + ". " + self.user.first_name + " " + self.user.last_name


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    logo = models.TextField(default="")
    description = models.TextField(default="", max_length=100)
    website = models.TextField(default="")
    industry = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    founded_year = models.IntegerField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id) + ". " + self.name


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField(default="")
    requirements = models.TextField(null=True)
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    city = models.CharField(max_length=20)
    metro = models.CharField(max_length=20)
    type = models.CharField(max_length=30)
    schedule = models.CharField(max_length=30)
    experiense = models.IntegerField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    type_of_money = models.CharField(max_length=3, default="")

    def __str__(self) -> str:
        return str(self.id) + ". " + self.company.name + ", " + self.title


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    cover_letter = models.TextField(default="")
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # If company is not set but job is, get company from job
        if not self.company_id and self.job_id:
            self.company = self.job.company
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (
                str(self.id)
                + ". "
                + self.user.first_name
                + " "
                + self.user.last_name
                + ", "
                + self.job.title
        )


class Auction(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    current_stage = models.IntegerField()
    stage_end_time = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
                str(self.id)
                + ". ApplicationID: "
                + str(self.application.id)
                + ", "
                + self.status
        )


class AuctionBid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    stage = models.IntegerField()
    value = models.JSONField(null=True)
    timestamp = models.CharField(max_length=255)

    def __str__(self) -> str:
        return (
                str(self.id) + ". AuctionID: " + str(self.auction.id) + ", " + self.company.name
        )


class Chat(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
                str(self.id)
                + ". ApplicationID: "
                + str(self.application.id)
                + ", "
                + self.status
        )


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default="")
    message_type = models.CharField(max_length=255)
    metadata = models.JSONField(null=True, blank=True)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return (
                str(self.id)
                + ". ChatID: "
                + str(self.chat.id)
                + ", "
                + self.sender.first_name
                + " "
                + self.sender.last_name
        )

    def get_file_url(self):
        """Return the URL for the file if it exists"""
        if self.file:
            return self.file.url
        elif self.metadata and 'fileUrl' in self.metadata:
            return self.metadata['fileUrl']
        return None

    def get_file_name(self):
        if self.file:
            return self.file.name.split('/')[-1]
        elif self.metadata and 'fileName' in self.metadata:
            return self.metadata['fileName']
        return None


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    content = models.TextField()
    related_id = models.IntegerField(null=True, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id}. {self.type} for {self.user.first_name} {self.user.last_name}"


class PinnedChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'chat')
        ordering = ['created_at']

    def __str__(self) -> str:
        return f"{self.id}. User {self.user.id} pinned Chat {self.chat.id}"
