from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """Tag Model."""

    name = models.CharField(max_length=50)
    color_hex = models.CharField(max_length=10)

    @property
    def contrast_color(self):
        """Contrast Color."""
        if self.color_hex.startswith("#"):
            hex_color = self.color_hex[1:]
            r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
            yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000
            return "#222222" if yiq >= 128 else "#EEEEEE"
        return "#000000"

    def __str__(self):
        return f"{self.name}" 


class ChangeLog(models.Model):
    """ChangeLog Model."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    version = models.CharField(max_length=20, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    related_tickets = models.CharField(
        max_length=100, help_text="Comma separated ticket numbers", blank=True, null=True
    )
    tags = models.ManyToManyField(Tag, blank=True)  # New Tags Field

    def __str__(self):
        return f"{self.title} ({self.version})"
