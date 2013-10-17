#encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from book.models import Book
from django.conf import settings

def home(request):
    obj_list = Book.objects.all()
    return render_to_response("home.html", locals(), context_instance=RequestContext(request))


def export_books(request, format):
    from book.resources import BookResource
    from django.core.files import File
    if format in settings.DEFAULT_FORMATS:
        try:
            data = BookResource().export()
            f = open(settings.MEDIA_ROOT + '/files/books.' + format,'a')
            mf = File(f)
            mf.write(data.xls)
            mf.close()
            return HttpResponseRedirect("/media/files/books." + format)
        except IOError:
            return HttpResponse("Error, IOError")
        except Exception:
            return HttpResponse("Error, Exception")
    else:
        return HttpResponseRedirect("/")


def import_books(request, format):
    from .forms import ImportForm
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            import_file = request.FILES['import_file']
            from xlrd import open_workbook
            wb = open_workbook(file_contents=import_file.read())
            data = list()
            for s in wb.sheets():
                print 'Sheet:', s.name
                for row in range(s.nrows):
                    values_list = []
                    for col in range(s.ncols):
                        values_list.append(s.cell(row, col).value)
                    data.append(values_list)  # 
    else:
        form = ImportForm()
    return render_to_response("form.html", locals(), context_instance=RequestContext(request))