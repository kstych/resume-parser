from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .parser import Engine

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def convert_pdf_to_txt(fp):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


en = Engine()


class Index(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        text = request.POST.get('text')
        return JsonResponse({
            'status':'OK',
            'result':en.tokeninzer(text)
        })



class Index2(View):
    def get(self, request):
        return render(request, 'index2.html')

    def post(self, request):
        received = None
        pdf = request.FILES.get('resume')
        if pdf:
            try:
                received=convert_pdf_to_txt(pdf).replace('\n', ' ')         
            except Exception as e:
                
                return JsonResponse({
                        'status':'ERROR',
                        'error': e
                })
        return JsonResponse({
                'status':'OK',
                'rawtext': received,
                'result':en.tokeninzer(received)

        })