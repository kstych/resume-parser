from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .parser import Engine

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from io import StringIO
import docx2txt
from pdfminer import high_level
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar,LTLine,LAParams


def ExtractHeavyFonts(pdffile):
    Extract_Data = {}
    for page_layout in extract_pages(pdffile):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            Font_size=int(character.size)
                txt = element.get_text().replace('\t', ' ').replace('\n', ' ')
                if Font_size in Extract_Data:
                    if txt not in Extract_Data[Font_size]:
                        Extract_Data[Font_size].append(txt)
                else:
                    Extract_Data[Font_size]= [txt]
    return Extract_Data
                

def extract_text_from_doc(doc_path):
    temp = docx2txt.process(doc_path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)

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
        prediction = None
        doc = None
        pdf = None 
        filename = str(request.FILES.get('resume'))
        
        if filename.endswith('.pdf'):
            pdf = request.FILES.get('resume')
        else:
            doc = request.FILES.get('resume')
        
        if pdf:
            try:
                prediction = ExtractHeavyFonts(pdf)
                received=convert_pdf_to_txt(pdf).replace('\n', ' ')

            except Exception as e:
                
                return JsonResponse({
                        'status':'ERROR',
                        'error': e
                })
        else:
            received = extract_text_from_doc(doc)
            prediction = {}
        return JsonResponse({
                'status':'OK',
                'rawtext': received,
                'result':en.tokeninzer(received),
                'VisualWeights':prediction

        })