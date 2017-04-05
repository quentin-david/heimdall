from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from .models import Notes, Category, Bookmark, NotesFile
from .forms import NotesForm, CategoryForm, BookmarkForm
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from django.http import HttpResponse

"""
Notes
"""
class NotesList(ListView):
    model = Notes
    context_object_name = 'notes_list'
    template_name = 'notes/notes_list.html'
    def get_context_data(self, **kwargs):
        context = super(NotesList, self).get_context_data(**kwargs)
        context['root_category_list'] = Category.objects.filter(parent__isnull=True)
        context['notes_form'] = NotesForm(None)
        return context



def notesCreateOrUpdate(request, notes_id=None):
    root_category_list = Category.objects.filter(parent__isnull=True)
    if notes_id:
        note_to_edit = Notes.objects.get(id=notes_id)
        upfiles = note_to_edit.notesfile_set.all()
    else:
        note_to_edit = None
    form = NotesForm(request.POST or None,request.FILES or None, instance=note_to_edit)
    files = request.FILES.getlist('uploaded_files')
    if form.is_valid():
        note = form.save(commit=False)
        note.owner = request.user
        note.save()
        for upfile in files:
            f = NotesFile(notes=note, uploaded_file=upfile)
            f.save()
        return redirect('topic_view', category_id=note.category.id)
    return render(request,'notes/notes_create_form.html',locals())

"""
class NotesDelete(DeleteView):
    model = Notes
    context_object_name = 'note'
    template_name = 'notes/notes_delete.html'
    success_url = reverse_lazy('notes_list')
"""
def notesDelete(request, notes_id):
    notes_to_delete = Notes.objects.get(id=notes_id)
    if notes_to_delete:
        # Deletion of all the physical files
        for notes_file in NotesFile.objects.filter(notes=notes_to_delete):
            notes_file.delete_physical_file()
        notes_to_delete.delete()
    messages.success(request, 'Notes "{}" deleted !'.format(notes_to_delete.title))
    return redirect('topic_view', category_id=notes_to_delete.category.id)



"""
NotesFile
"""
# Ajax call (csrf disabled...probably not the right thing to do)
@csrf_exempt
def notesFileDelete(request, notes_file_id):
    file_to_delete = NotesFile.objects.get(id=notes_file_id)
    if file_to_delete:
        file_to_delete.delete_physical_file()
        file_to_delete.delete()
    messages.success(request, 'File "{}" deleted !'.format(file_to_delete.uploaded_file))
    return redirect('topic_view', category_id=file_to_delete.notes.category.id)


"""
Categories
"""
def categoryList(request):
    root_category_list = Category.objects.filter(parent__isnull=True)
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        category = form.save(commit=False)
        category.save()
        return redirect('category_list')
    return render(request, 'category/category_home.html', locals())

class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_create_form.html'
    success_url = reverse_lazy('category_list')
    def get_context_data(self, **kwargs):
        context = super(CategoryCreate, self).get_context_data(**kwargs)
        context['root_category_list'] = Category.objects.filter(parent__isnull=True)
        return context
    
class CategoryDelete(DeleteView):
    model = Category
    context_object_name = 'category'
    template_name = 'category/category_delete.html'
    success_url = reverse_lazy('category_list')


"""
Bookmark
"""
def bookmarkList(request):
    unsorted_bookmark_list = Bookmark.objects.filter(category__isnull=True)
    root_category_list = Category.objects.filter(parent__isnull=True)
    form = BookmarkForm(request.POST or None)
    if form.is_valid():
        bookmark = form.save(commit=False)
        bookmark.owner = request.user
        bookmark.save()
        return redirect('bookmark_list')
    return render(request, 'bookmark/bookmark_list.html', locals())


def bookmarkDelete(request, bookmark_id):
    bookmark_to_delete = Bookmark.objects.get(id=bookmark_id)
    if bookmark_to_delete:   
        bookmark_to_delete.delete()
    messages.success(request, 'Bookmark "{}" deleted !'.format(bookmark_to_delete.url))
    return redirect('topic_view', category_id=bookmark_to_delete.category.id)

"""
Topic
list every elements (Notes, bookmarks...) by category
"""
def topicView(request, category_id):
    category = Category.objects.get(id=category_id)
    root_category_list = Category.objects.filter(parent__isnull=True)
    bookmark_list = Bookmark.objects.filter(category=category.id)
    bookmark_form = BookmarkForm(request.POST or None)
    form = NotesForm(None, initial={'category':category.id})
    notes_list = Notes.objects.filter(category=category)
    #file_list = NotesFile.objects.filter(notes__set=notes_list) # to check
    if bookmark_form.is_valid():
        bookmark = bookmark_form.save(commit=False)
        bookmark.owner = request.user
        bookmark.category = category
        bookmark.save()
        return redirect('topic_view', category_id=category.id)
        
    return render(request, 'topic/topic_view.html', locals())


"""
def topicViewPdf(request, category_id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)
    # Topic text
    category = Category.objects.get(id=category_id)
    text_to_render = category.get_topic_pdf_render()
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(10, 10, text_to_render)
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
"""
