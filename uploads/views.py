from django.shortcuts import render
import requests
from uploads.models import Contact
import spacy
import fitz
import sys
from django.core.files.storage import FileSystemStorage

x = []


def home(request):

    if request.method == 'POST':
        x.clear()
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        nlp_model = spacy.load('nlp_model')
        a = 'media/'
        b = uploaded_file.name
        fname = a+b
        doc = fitz.open(fname)
        text = ""
        for page in doc:
            text = text + str(page.getText())
        txt = " ".join(text.split("\n"))
        doc = nlp_model(txt)

        for ent in doc.ents:
            x.append(f'{ent.label_.upper():{30}}- {ent.text}')

    return render(request, 'homepage.html', {'result2': x})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']
        #print(name, email, phone, desc)
        ins = Contact(name=name, email=email, phone=phone, desc=desc)
        ins.save()
        print("the data has been written inside the database")

    return render(request, 'contact.html')
