__author__ = 'dheerendra'

from django import forms
from models import Complaint, Reply

class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ['title', 'message']
