from django.shortcuts import render, redirect 
from django.http import HttpResponseNotFound
from django.contrib import messages

from . import util
import markdown as md
from . import functions
import random


form = functions.SearchForm()

def index(request):
    form, entries = functions.search_entries(request)

    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "form": form
    })


def entry_detail(request, entry_name):
    content = util.get_entry(entry_name)
    if content is not None:
        html_content = md.markdown(content)
        return render(request, "encyclopedia/entry_detail.html", {
            "title": entry_name,
            "entry_detail": html_content,
            "form": form
        })
    else:
        return HttpResponseNotFound("Page not found")
    

def add(request):
    if request.method == "GET":
        new_page_form = functions.NewPageForm()
        return render(request, "encyclopedia/add.html", {
            "form": form,
            "new_page_form": new_page_form,
        })
    else:
        new_page_form = functions.NewPageForm(request.POST)
        if new_page_form.is_valid():
            title = new_page_form.cleaned_data["title"]
            content = new_page_form.cleaned_data["content"]
            if title.lower() in [entry.lower() for entry in util.list_entries()]:       
                messages.warning(request, "Page already exists!")
                # To keep content if title already exists, use render instead of redirect
                return render(request, "encyclopedia/add.html", {
                    "form": form,
                    "new_page_form": new_page_form,      
                })
            else:
                util.save_entry(title, content)
                return redirect("encyclopedia:index")


def edit(request,entry_name):
    if request.method == "GET":
        content = util.get_entry(entry_name)
        if content is not None:
            new_page_form = functions.NewPageForm(initial={'title': entry_name, 'content': content})
            return render(request, "encyclopedia/editpage.html", {
                "form": form,
                "new_page_form": new_page_form,
                "title": entry_name,
            })
        else:
            return HttpResponseNotFound("Page not found")
    else:
        new_page_form = functions.NewPageForm(request.POST)
        if new_page_form.is_valid():
            title = new_page_form.cleaned_data["title"]
            content = new_page_form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("encyclopedia:entry_detail", entry_name=title)
        

def delete(request, entry_name):
    if request.method == "GET":
        util.delete_entry(entry_name)
        return redirect("encyclopedia:index")
    

def random_page(request):
    if request.method == "GET":
        entries = util.list_entries()
        randomEntry = random.choice(entries)
        return redirect("encyclopedia:entry_detail", entry_name=randomEntry)

