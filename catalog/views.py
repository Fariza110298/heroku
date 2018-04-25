from django.shortcuts import render
import datetime
#import timedelta
# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
    """
View function for home page of site.
"""
# Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

# Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_instances_reserved = BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count() # The 'all()' is implied by default.
    time = datetime.datetime.now()

    hour = time.hour
    minute = time.minute
    second = time.second
    year = time.year
    month = time.month
    day = time.day
    w_day = time.weekday()
    fari= "Fariza"




#n = (next_day - time.weekday()) % 7 # mod-7 ensures we don't go backward in time
#next_run_date = time + datatime.timedelta(days=n)
# Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)

    request.session['num_visits'] = num_visits + 1

# Render the HTML template index.html with the data in the context variable.
    return render( request, 'index.html',               context={'num_books': num_books, 'num_instances': num_instances,
'num_instances_available': num_instances_available, 'num_authors': num_authors,
'num_visits': num_visits,'hour': hour, 'minute': minute, 'second': second, 'year': year,
'month': month, 'day': day, 'weekdays': w_day, 'fariiii': fari }, # num_visits appended
)
from django.views import generic
class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
class BookDetailView(generic.DetailView):
    model = Book
from django.views import generic

class AuthorListView(generic.ListView):
    model = Author
class AuthorDetailView(generic.DetailView):
    model = Author
    model2=Book
    paginate_by = 2
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
Generic class-based view listing books on loan to current user.
"""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
Generic class-based view listing books on loan to current user.
"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def  get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
View function for renewing a specific BookInstance by librarian
"""
    book_inst=get_object_or_404(BookInstance, pk = pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)

# Check if the form is valid:
    if form.is_valid():# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
        book_inst.due_back = form.cleaned_data['renewal_date']
        book_inst.save()# redirect to a new URL:
        return HttpResponseRedirect(reverse('all-borrowed') )
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
        return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})