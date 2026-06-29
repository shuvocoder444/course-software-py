from django import forms
from .models import Account

class AccountCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ড্রপডাউন থেকে ADMIN বাদ দেওয়া হলো যেন অ্যাডমিন নতুন কোনো অ্যাডমিন তৈরি করতে না পারে
        self.fields['role'].choices = [choice for choice in Account.Role.choices if choice[0] != 'ADMIN']

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data["password"])
        if commit:
            account.save()
        return account



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class AccountCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap styling add korar jonno
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
