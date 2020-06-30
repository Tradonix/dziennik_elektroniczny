from django import forms
from main.models import Messages


class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        exclude = ['send_by', 'is_read']


class MessagesDetailForm(forms.ModelForm):
    class Meta:
        model = Messages

        fields = [
            "send_by",
            "title",
            "message"
        ]

        widgets = {
            'send_by': forms.Select(attrs={'disabled': True}),
            'title': forms.TextInput(attrs={'disabled': True}),
            'message': forms.Textarea(attrs={'disabled': True}),
        }
