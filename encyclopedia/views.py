from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

import random

from . import util


def index(request):
    if 'wiki-search' in request.GET:
        wiki_search = request.GET.get('q', None)
        if wiki_search in util.list_entries():
            return redirect("/wiki/" + wiki_search)
        elif any(wiki_search in s for s in util.list_entries()):
            return render(request, "encyclopedia/results.html", {
                "wiki": wiki_search,
                "entries": [s for s in util.list_entries() if wiki_search in s],
                "random": random.choice(util.list_entries())
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "error": "Error, the page you searched for cannot be found.",
                "random": random.choice(util.list_entries())
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "random": random.choice(util.list_entries())
        })

def entry(request, entry):
    if 'wiki-search' in request.GET:
        wiki_search = request.GET.get('q', None)
        if wiki_search in util.list_entries():
            return redirect("/wiki/" + wiki_search)
        elif any(wiki_search in s for s in util.list_entries()):
            return render(request, "encyclopedia/results.html", {
                "wiki": wiki_search,
                "entries": [s for s in util.list_entries() if wiki_search in s],
                "random": random.choice(util.list_entries())
            })
    else:
        if entry not in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "error": "Error, this page cannot be found.",
                "random": random.choice(util.list_entries())
            })
        else:
            return render(request, "encyclopedia/entry.html", {
                "entry_page": util.get_entry(entry),
                "random": random.choice(util.list_entries()),
                "entry": entry
            })

def add(request):
    if 'wiki-search' in request.GET:
        wiki_search = request.GET.get('q', None)
        if wiki_search in util.list_entries():
            return redirect("/wiki/" + wiki_search)
        elif any(wiki_search in s for s in util.list_entries()):
            return render(request, "encyclopedia/results.html", {
                "wiki": wiki_search,
                "entries": [s for s in util.list_entries() if wiki_search in s],
                "random": random.choice(util.list_entries())
            })
    else:
        class NewPageForm(forms.Form):
            Title = forms.CharField()
            Markdown = forms.CharField(widget=forms.Textarea)
        if 'wiki-post' in request.POST:
            form = NewPageForm(request.POST)
            if form.is_valid():
                Title = form.cleaned_data["Title"]
                if Title in util.list_entries():
                    return render(request, "encyclopedia/error.html", {
                        "error": "Error, the page you tried to create already exists.",
                        "random": random.choice(util.list_entries())
                    })
                else:
                    Markdown = form.cleaned_data["Markdown"]
                    util.save_entry(Title, Markdown)
                    return redirect("/wiki/" + Title)
            else:
                return render(request, "encyclopedia/add.html", {
                    "form": form,
                    "random": random.choice(util.list_entries()),
                    "title": "Page",
                    "AE": "Add",
                    "action": "/wiki/add/page"
                })
        else:
            return render(request, "encyclopedia/add.html", {
                "form": NewPageForm(),
                "random": random.choice(util.list_entries()),
                "title": "Page",
                "AE": "Add",
                "action": "/wiki/add/page"
            })

def edit(request, entry):
    if 'wiki-search' in request.GET:
        wiki_search = request.GET.get('q', None)
        if wiki_search in util.list_entries():
            return redirect("/wiki/" + wiki_search)
        elif any(wiki_search in s for s in util.list_entries()):
            return render(request, "encyclopedia/results.html", {
                "wiki": wiki_search,
                "entries": [s for s in util.list_entries() if wiki_search in s],
                "random": random.choice(util.list_entries())
            })
    else:
        class EditPageForm(forms.Form):
            Markdown = forms.CharField(widget=forms.Textarea(), initial=util.get_entry(entry))
        if entry not in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "error": "Error, this page cannot be found.",
                "random": random.choice(util.list_entries())
            })
        else:
            if 'wiki-post' in request.POST:
                form0 = EditPageForm(request.POST)
                if form0.is_valid():
                    Markdown = form0.cleaned_data["Markdown"]
                    util.save_entry(entry, Markdown)
                    return redirect("/wiki/" + entry)
                else:
                    return render(request, "encyclopedia/add.html", {
                        "form": form0,
                        "random": random.choice(util.list_entries()),
                        "AE": "Edit",
                        "title": entry,
                        "entry": entry,
                        "action": "/wiki/edit/" + entry
                    })
            else:
                return render(request, "encyclopedia/add.html", {
                "form": EditPageForm(),
                "random": random.choice(util.list_entries()),
                "AE": "Edit",
                "title": entry,
                "entry": entry,
                "action": "/wiki/edit/" + entry
            })
