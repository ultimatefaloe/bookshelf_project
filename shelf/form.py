from django import forms
from .models import Book


# Reusable Tailwind class strings so styling stays consistent
INPUT_CLASSES = (
    "block w-full rounded-md border border-gray-300 bg-white px-3 py-2 "
    "text-gray-900 placeholder-gray-400 shadow-sm "
    "focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none "
    "sm:text-sm"
)

TEXTAREA_CLASSES = INPUT_CLASSES + " resize-y"

SELECT_CLASSES = (
    "block w-full rounded-md border border-gray-300 bg-white px-3 py-2 "
    "text-gray-900 shadow-sm "
    "focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none "
    "sm:text-sm"
)

FILE_CLASSES = (
    "block w-full text-sm text-gray-900 "
    "file:mr-4 file:rounded-md file:border-0 "
    "file:bg-indigo-50 file:px-4 file:py-2 "
    "file:text-sm file:font-semibold file:text-indigo-700 "
    "hover:file:bg-indigo-100"
)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "description", "cover", "status", "isbn_number"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Book title",
            }),
            "author": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Author name",
            }),
            "description": forms.Textarea(attrs={
                "class": TEXTAREA_CLASSES,
                "rows": 4,
                "placeholder": "Short description (optional)",
            }),
            "cover": forms.ClearableFileInput(attrs={
                "class": FILE_CLASSES,
            }),
            "status": forms.Select(
                choices=[("", "Select status")] + Book.STATUS_CHOICES,
                attrs={"class": SELECT_CLASSES},
            ),
            "isbn_number": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "ISBN (optional)",
            }),
        }

    def clean_isbn_number(self):
        isbn = self.cleaned_data.get("isbn_number")
        if isbn:
            cleaned = isbn.replace("-", "").replace(" ", "")
            if not cleaned.isdigit() or len(cleaned) not in (10, 13):
                raise forms.ValidationError("ISBN must be 10 or 13 digits.")
            return cleaned
        return isbn