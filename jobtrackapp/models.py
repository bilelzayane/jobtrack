from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Company(models.Model):
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    size = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def offers_count(self):
        return self.offers.count()


class Offer(models.Model):
    TYPE_CHOICES = [
        ('Internship', 'Internship'),
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
    ]
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Draft', 'Draft'),
        ('Closed', 'Closed'),
    ]
    title = models.CharField(max_length=150)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='offers')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=100, blank=True, null=True)
    salary = models.CharField(max_length=60, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')
    description = models.TextField(blank=True, null=True)
    posted_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title} — {self.company.name}"


class Application(models.Model):
    STATE_CHOICES = [
        ('Reviewed', 'Reviewed'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Contract', 'Contract'),
        ('Rejected', 'Rejected'),
    ]
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='applications')
    candidate_name = models.CharField(max_length=100)
    candidate_email = models.EmailField()
    cv_file = models.FileField(
        upload_to='cvs/',
        blank=True, null=True,
        validators=[FileExtensionValidator(['pdf'])]
    )
    status = models.CharField(max_length=10, choices=STATE_CHOICES, default='Reviewed')
    applied_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate_name} → {self.offer.title}"
