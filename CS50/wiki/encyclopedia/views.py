from django.shortcuts import render
from django.http import HttpResponse 

from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def markdown_to_html(title):
    contents = util.get_entry(title)
    if contents is None:
        return None
    return markdown2.Markdown().convert(contents)

def get_title(request, title):
    html_content = markdown_to_html(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html",{
            "message": f"No page with title {title}"
        })
    
    return render(request, "encyclopedia/entry.html",
        {
            "html_content": html_content,
            "title":title
        }
    )

def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        html_content = markdown_to_html(title)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html",
            {
                "html_content": html_content,
                "title":title
            }
        )

        available_entries = util.list_entries()
        recommended_entries = [entries for entries in available_entries if title in entries]

        return render(request, "encyclopedia/search.html",
            {
                "entries": recommended_entries,
                "title":title
            }
        )
    
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_entry.html")
    
    if request.method == "POST":
        title = request.POST["page_title"]
        content = request.POST["textarea"]

        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html",{
            "message": f"Page with title {title} already exists"
        })

        util.save_entry(title, content)
        return get_title(request, title)

def edit(request):
    if request.method == "POST":
        page_title = request.POST["page_title"]
        markdown_content = util.get_entry(page_title)
        return render(request, "encyclopedia/edit.html", 
        {
            "page_title":page_title,
            "markdown_content":markdown_content
        })
    
def save_edit_page(request):
    if request.method == "POST":
        title = request.POST["page_title"]
        content = request.POST["textarea"]

        util.save_entry(title, content)
        return get_title(request, title)


def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return get_title(request, random_title)
   
        


