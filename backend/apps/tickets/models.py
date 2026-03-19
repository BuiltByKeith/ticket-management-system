from django.db import models
import secrets
from django.conf import settings
from apps.systems.models import System
from apps.concern_types.models import ConcernType
from ulid import ULID


def generate_ulid():
    return str(ULID())


def generate_reference_id():
    """Generates a unique reference ID for each ticket. like TKT-20240612-5f2e4c8a9b1d4e3f8a7c6b9d0e1f2a3"""
    return f"TKT-{secrets.token_hex(3).upper()}"


def generate_tracking_password():
    """Generates a random tracking password for each ticket. like 8a7c6b9d0e1f2a3"""
    return secrets.token_urlsafe(10)


def ticket_attachment_path(instance, filename):
    """Organizes uploaded files into ticket-specific subdirectories. like attachments/TKT-20240612-5f2e4c8a9b1d4e3f8a7c6b9d0e1f2a3/filename.jpg"""
    return f"tickets/{instance.reference_id}/{filename}"


class Ticket(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    id = models.BigAutoField(primary_key=True)  # Using BigAutoField for scalability
    ulid = models.CharField(
        max_length=26, unique=True, default=generate_ulid, editable=False
    )  # ULID for globally unique identifier

    reference_id = models.CharField(
        max_length=20, unique=True, default=generate_reference_id, editable=False
    )
    tracking_password = models.CharField(
        max_length=100, default=generate_tracking_password, editable=False
    )

    requester_full_name = models.CharField(max_length=255)
    requester_email = models.EmailField()
    system = models.ForeignKey(System, on_delete=models.PROTECT, related_name="tickets")
    concern_type = models.ForeignKey(
        ConcernType, on_delete=models.PROTECT, related_name="tickets"
    )
    description = models.TextField()
    file_attachment = models.FileField(
        upload_to=ticket_attachment_path, blank=True, null=True
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
        limit_choices_to={"role": "developer"},
    )  # only developers can be assigned

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    priority = models.CharField(
        max_length=20, choices=Priority.choices, default=Priority.MEDIUM
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tickets"
        ordering = ["-date_created"]

    def __str__(self):
        return f"{self.reference_id} - {self.status}"
