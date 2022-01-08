from django import forms
from django.core.validators import MinValueValidator,MaxValueValidator

from .models import Comment,Category

class CommentForm(forms.ModelForm):

    class Meta:
        model   = Comment
        fields  = [ "content","target","star" ]


#モデルを継承しないフォームクラス
class YearMonthForm(forms.Form):
    year    = forms.IntegerField()
    month   = forms.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(12)])

