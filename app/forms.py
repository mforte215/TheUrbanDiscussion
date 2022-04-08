from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from ckeditor.widgets import CKEditorWidget

User = get_user_model()

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class ThreadCreateForm(forms.Form):
    title = forms.CharField(label='Thread Name', max_length=200)
    

