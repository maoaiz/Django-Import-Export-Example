#encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from book.models import Book, Author
from django.conf import settings


def home(request):
    obj_list = Book.objects.all()
    return render_to_response("home.html", locals(), context_instance=RequestContext(request))


def export_books(request, format):
    from book.resources import BookResource
    from django.core.files import File
    if format in settings.DEFAULT_FORMATS:
        try:
            _author = Author.objects.get(name="Lina")
            print _author
            queryset = Book.objects.filter(author=_author)
            print queryset
            data = BookResource().export(queryset)
            print data.csv
            f = open(settings.MEDIA_ROOT + '/files/book.' + format,'a')
            mf = File(f)
            mf.write(data.csv)
            mf.close()
            return HttpResponseRedirect("/media/files/book." + format)
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
                    print values_list
    else:
        form = ImportForm()
    return render_to_response("form.html", locals(), context_instance=RequestContext(request))


def export_xls(request):
    fields = ["id", "name", "author", "author_email", "published", "price"]
    _author = Author.objects.get(name="Mauricio")
    queryset = Book.objects.filter(author=_author)
    try:
        return export_xlwt(Book, queryset.values_list(*fields), fields)
    except Exception, e:
        raise e


def export_xlwt(model, values_list, fields):
    import xlwt
    from datetime import datetime, date
    modelname = model._meta.verbose_name_plural.lower()
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet(modelname)

    default_style = xlwt.Style.default_style
    datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
    date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

    for j, f in enumerate(fields):
        sheet.write(0, j, fields[j])

    for row, rowdata in enumerate(values_list):
        for col, val in enumerate(rowdata):
            if isinstance(val, datetime):
                style = datetime_style
            elif isinstance(val, date):
                style = date_style
            else:
                style = default_style

            sheet.write(row + 1, col, val, style=style)

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % modelname
    book.save(response)
    return response
