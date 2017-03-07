from django import forms
from .models import Notes, Category, Bookmark
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Button
from crispy_forms.bootstrap import InlineField
from crispy_forms.bootstrap import FormActions
#from crispy_forms.bootstrap import SubmitCancelFormActions

"""
Notes
"""
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        #fields = '__all__'
        exclude = ['owner']
    
    def __init__(self, *args, **kwargs):
        super(NotesForm,self).__init__(*args,**kwargs)
        # Only display second and third level of imbrication
        self.fields["category"].queryset = Category.objects.filter(parent__isnull=False)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ' '
        self.helper.add_input(Submit('submit', 'Submit'))
        """
        self.helper.add_input(FormActions(
            Submit('save', 'Save changes'),
            Button('cancel', 'Cancel')
        ))
        """
        self.helper.form_class = '' # if you want to have a horizontally layout form
        self.helper.label_class = 'input-group-addon' # this css class attribute will be added to all of the labels in your form. For instance, the "Username: " label will have 'col-md-3'
        self.helper.field_class = 'input-group'
    
"""
Categories have 3 level of imbrication
"""
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(CategoryForm,self).__init__(*args, **kwargs)
        # Only display first and second level of imbrication
        self.fields["parent"].queryset = Category.objects.filter(Q(parent__isnull=True) | Q(parent__parent__isnull=True))
        
        
class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        exclude = ['owner']
        
    def __init__(self, *args, **kwargs):
        super(BookmarkForm,self).__init__(*args,**kwargs)
        # Only display second and third level of imbrication
        self.fields["category"].queryset = Category.objects.filter(parent__isnull=False)