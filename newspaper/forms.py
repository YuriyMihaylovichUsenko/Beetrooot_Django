from django import forms

from . models import Comment


class CommentForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.Meta.required:
    #         self.fields[field].required = True

    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment')
        labels = {'name': '', 'email': '', 'comment': ''}
        required = ('name', 'email', 'comment')
        # widgets = {
        #     'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
        #     'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
        #     'message': forms.Textarea(
        #         attrs={
        #             'placeholder': 'Your Message',
        #             'maxlength': '1000'
        #         }
        #     )
        # }