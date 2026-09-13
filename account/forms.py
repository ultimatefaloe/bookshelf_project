from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


# ─── Reusable Tailwind class strings ──────────────────────────────
INPUT_CLASSES = (
    "block w-full rounded-lg border border-gray-300 bg-white px-3.5 py-2.5 "
    "text-gray-900 placeholder-gray-400 shadow-sm "
    "focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30 focus:outline-none "
    "transition sm:text-sm"
)

PASSWORD_CLASSES = INPUT_CLASSES + " pr-11"   # room for the eye toggle


class LoginForm(AuthenticationForm):
    """Login form — inherits all validation from AuthenticationForm."""

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": INPUT_CLASSES,
            "placeholder": "Username",
            "autofocus": True,
            "autocomplete": "username",
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": PASSWORD_CLASSES,
            "placeholder": "Password",
            "autocomplete": "current-password",
        }),
    )


class RegisterForm(UserCreationForm):
    """Registration form — extends UserCreationForm with an email field."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": INPUT_CLASSES,
            "placeholder": "you@example.com",
            "autocomplete": "email",
        }),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Choose a username",
                "autocomplete": "username",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Style the two password fields provided by UserCreationForm
        self.fields["password1"].widget.attrs.update({
            "class": PASSWORD_CLASSES,
            "placeholder": "Create a password",
            "autocomplete": "new-password",
        })
        self.fields["password2"].widget.attrs.update({
            "class": PASSWORD_CLASSES,
            "placeholder": "Confirm password",
            "autocomplete": "new-password",
        })

        # Friendlier help text (default is a long bulleted list)
        self.fields["password1"].help_text = (
            "At least 8 characters. Can't be too similar to your username."
        )
        self.fields["password2"].help_text = ""

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class ProfileForm(forms.ModelForm):
    """Update a user's basic profile fields with uniqueness checks."""

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Username",
                "autocomplete": "username",
            }),
            "email": forms.EmailInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Email",
                "autocomplete": "email",
            }),
            "first_name": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "First Name",
                "autocomplete": "given-name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Last Name",
                "autocomplete": "family-name",
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip()
        if not email:
            return email

        qs = User.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                "This email is already in use.", code="email_taken"
            )
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()
        if not username:
            return username

        qs = User.objects.filter(username__iexact=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                "This username is taken.", code="username_taken"
            )
        return username
    
    
class StyledPasswordResetForm(PasswordResetForm):
    """Password reset form — just styles the email field."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            "class": INPUT_CLASSES,
            "placeholder": "you@example.com",
            "autocomplete": "email",
            "autofocus": True,
        })


class ResetPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, placeholder in (
            ("old_password", "Current password"),
            ("new_password1", "New password"),
            ("new_password2", "Confirm new password"),
        ):
            self.fields[name].widget.attrs.update({
                "class": PASSWORD_CLASSES,
                "placeholder": placeholder,
                "autocomplete": "current-password" if name == "old_password" else "new-password",
            })