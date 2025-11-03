from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'name', 'profile_picture', 'office_id','phone', 'address', 
            'date_of_birth', 'gender', 'membership_type'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(),
            'membership_type': forms.Select(),
        }
