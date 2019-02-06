import bcrypt
from django import forms


class MailboxForm(forms.ModelForm):
    def clean_password(self):
        data = self.cleaned_data['password']
        if data[:4] == '$2b$':
            return data
        return bcrypt.hashpw(data.encode(), bcrypt.gensalt()).decode()
