from django.shortcuts import render
from . import util
from django import forms
from random import randrange
import markdown2

class searchForm(forms.Form): #search form
    search = forms.CharField(label='',
    widget = forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class titleForm(forms.Form):
    title = forms.CharField(label='',
    widget = forms.TextInput(attrs={'placeholder': 'Enter content'}))

class contentForm(forms.Form):
    content = forms.CharField(label='',
    widget = forms.Textarea(attrs={'style': 'height: 25em;' 'resize:' 'none;', 'placeholder': 'Enter content'}))

def index(request):
    query = ""
    res = []

    if request.method == "POST": # search bar
        form = searchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["search"]
            
            for title in util.list_entries():
                if query.lower() == title.lower(): # found exact match
                    return wiki_title(request, title) # redirect to wiki/query

                if query.lower() in title.lower(): # substring match = find all matches
                    res.append(title)

        if res != []: # all results with substring
            return render(request, "encyclopedia/search.html", {
                "results":res,
                "form": searchForm()
            })

        else:
            return wiki_title(request, query) # error 404

        
    else: # homepage, list all entries
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": searchForm()
        })

# entry page for wiki/title
def wiki_title(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/404.html", {
            "message": "Requested page was not found" 
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "title":title.capitalize(),
            "entry":markdown2.markdown(util.get_entry(title)),
            "form": searchForm()
        })

def new(request):
    title_form = titleForm(request.POST)
    content_form = contentForm(request.POST)

    if request.method == "POST":
        if title_form.is_valid() and content_form.is_valid():
            title = title_form.cleaned_data["title"]
            content = content_form.cleaned_data["content"]

            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/404.html", {
                    "message": "Entry has already been created for this topic!"
                })
            else:
                util.save_entry(title, '#' + title + '\n' + content)
                return wiki_title(request, title)

    else:
        return render(request, "encyclopedia/new.html", {
            "form": searchForm(),
            "new_title": titleForm(),
            "new_content": contentForm
        })

def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "form": searchForm(),
            "text_edit": contentForm(initial={'content':content})
        })

    else:
        content_form = contentForm(request.POST)
        if content_form.is_valid():
            content = content_form.cleaned_data["content"]
            util.save_entry(title, content)

            return wiki_title(request, title)

def random(request):
    index = randrange(len(util.list_entries()))
    return wiki_title(request, util.list_entries()[index])

    

