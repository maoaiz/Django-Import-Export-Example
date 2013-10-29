from django import forms
from book.models import Book
IMPORT_FILE_TYPES = ['.xls', ]


class ImportForm(forms.Form):
    import_file = forms.FileField(
					required= True,
					label= u"Selecione un archivo Excel (.xls)"
				)

    def clean_import_file(self):
    	import os
        import_file = self.cleaned_data['import_file']
        extension = os.path.splitext( import_file.name )[1]
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError( u'%s no es un archivo Excel. Please make sure your input file is an excel file (Excel 2007 is NOT supported.' % extension )
        else:
            return import_file

    class Meta:
    	model = Book