from django import forms
from .models import Company, Offer, Application

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'industry', 'location', 'size', 'website', 'description', 'logo']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'company', 'type', 'location', 'salary', 'status', 'description']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['offer', 'candidate_name', 'candidate_email', 'cv_file']

class AdminApplicationForm(ApplicationForm):
    class Meta(ApplicationForm.Meta):
        fields = ['offer', 'candidate_name', 'candidate_email', 'cv_file', 'status']

