from django import forms
from django.contrib.auth import forms as auth_forms
from users.models import CustomUser
from django.contrib.auth import admin as auth_admin
from django.urls import reverse


class CustomUserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    username = forms.CharField(label="Username", widget=forms.TextInput)
    # password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    # password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
    #                             help_text="Enter the same password as above, for verification.")

    class Meta:
        model = CustomUser
        fields = ('email',)

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError(
    #             self.error_messages['password_mismatch'],
    #             code='password_mismatch',
    #         )
    #     return password2

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        # user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = auth_forms.ReadOnlyPasswordHashField(label="Password",
                                                    help_text="Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"password/\">this form</a>.")

    class Meta:
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]
