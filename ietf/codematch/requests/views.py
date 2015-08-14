import datetime
from django.shortcuts import get_object_or_404, render

from django import forms
from django.forms import CharField
from django.forms import ModelForm
from django.forms.models import modelform_factory, inlineformset_factory

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from ietf.group.models import Group
from ietf.person.models import Person
from ietf.doc.models import DocAlias, Document

from ietf.codematch.matches.forms import SearchForm, ProjectContainerForm, DocNameForm
from ietf.codematch.requests.forms import CodeRequestForm
from ietf.codematch.matches.models import ProjectContainer, CodingProject
from ietf.codematch.requests.models import CodeRequest

from ietf.codematch.utils import (get_prefix, render_page, is_user_allowed)

import debug                            

def show_list(request):
    """List all CodeRequests by Title"""
    
    project_containers = ProjectContainer.objects.exclude(code_request__isnull=True).order_by('creation_date')[:20]
    return render_page(request, "codematch/requests/list.html", {
            'projectcontainers' : project_containers
    }) 

@login_required(login_url=get_prefix() + '/codematch/accounts/login')
def show_my_list(request):
    """List CodeRequests i've created"""
    
    user = Person.objects.get( user = request.user )
    
    project_containers = ProjectContainer.objects.exclude(code_request__isnull=True).filter( owner = user ).order_by('creation_date')[:20]
    
    if project_containers.count() == 0:
        raise Http404()
    
    return render_page(request, "codematch/requests/mylist.html", {
            'projectcontainers' : project_containers
    })

@login_required(login_url=get_prefix() + '/codematch/accounts/login')
def show_mentoring_list(request):
    """List CodeRequests i'm mentoring"""
    
    user = Person.objects.get( user = request.user )
    
    project_containers = ProjectContainer.objects.exclude(code_request__isnull=True).filter( code_request__mentor = user ).order_by('creation_date')[:20]
    
    if project_containers.count() == 0:
        raise Http404()
    
    return render_page(request, "codematch/requests/mentoringlist.html", {
            'projectcontainers' : project_containers
    })     

@login_required(login_url=get_prefix() + '/codematch/accounts/login')
def edit(request, pk):
    """ New CodeRequest Entry """
    
    project_container = get_object_or_404(ProjectContainer, id=pk)
    
    user = Person.objects.get( user = request.user )
    
    if project_container.owner != user:
        raise Http404()
    
    proj_form = ProjectContainerForm(instance=project_container)
    req_form  = CodeRequestForm(instance=project_container.code_request)
    
    if request.method == 'POST':
       new_project = ProjectContainerForm(request.POST, instance=project_container)
       new_code_request = CodeRequestForm(request.POST, instance=project_container.code_request)
       
       if new_project.is_valid() and new_code_request.is_valid():
          new_project.save()
          new_code_request.save()
          return HttpResponseRedirect( get_prefix() + '/codematch/requests/'+str(project_container.id))
       else:
          print "Some form is not valid"

    return render_page(request, 'codematch/requests/edit.html', {
        'projectcontainer' : project_container,
        'projform' : proj_form,
        'reqform'  : req_form,
    })

def search(request):
    search_type = request.GET.get("submit")
    if search_type:
        form               = SearchForm(request.GET)
        project_containers = []
        template           = "codematch/requests/list.html"
    
        # get query field
        query = ''
        if request.GET.get(search_type):
            query = request.GET.get(search_type)

        if query :

            # Search by ProjectContainer Title or description
            if search_type   == "title":
                project_containers  =  ProjectContainer.objects.filter(title__icontains=query) | ProjectContainer.objects.filter(description__icontains=query) 

            elif search_type == "protocol":
                project_containers  =  ProjectContainer.objects.filter(protocol__icontains=query) 

            elif search_type == "mentor":
                project_containers = ProjectContainer.objects.filter(code_request__mentor__name__icontains=query) 

            else:
                raise Http404("Unexpected search type in ProjectContainer query: %s" % search_type)

            return render(request, template, {
                "projectcontainers" : project_containers,
                "form"              : form,
            })

        return HttpResponseRedirect(request.path)

    else:
        form = SearchForm()
        return render_page(request, "codematch/requests/search.html", { "form" : form })

def show(request,pk):
    """View individual Codematch Project and Add Document and Implementation"""
    
    project_container = get_object_or_404(ProjectContainer, id=pk)
    docs              = project_container.docs.select_related()
    doc_form          = DocNameForm()
    
    my_request = False
    
    if request.user.is_authenticated():
        user = Person.objects.get( user = request.user )
        my_request = project_container.owner == user
    
    if request.method == 'POST':
        doc_name=request.POST.get("name")

        if doc_name:
            doc = DocAlias.objects.get( name = doc_name )
            project_container.docs.add(doc)
            project_container.save()
            
            return HttpResponseRedirect(get_prefix() + '/codematch/requests/'+str(pk))
    
    return render_page(request, "codematch/requests/show.html",  {
        'projectcontainer': project_container,
        'docs'            : docs,
        'docform'         : doc_form,
        'myrequest'       : my_request
    })


@login_required(login_url=get_prefix() + '/codematch/accounts/login')
def new(request):
    """ New CodeRequest Entry """
    
    if is_user_allowed(request.user, "canaddrequest"):
        raise Http404()
    
    proj_form = modelform_factory(ProjectContainer,form=ProjectContainerForm)
    req_form  = modelform_factory(CodeRequest,form=CodeRequestForm)
    
    if request.method == 'POST':
       new_project = ProjectContainerForm(request.POST)
       new_request = CodeRequestForm(request.POST)
       
       if new_project.is_valid() and new_request.is_valid():
          code_request              = new_request.save()
          project                   = new_project.save(commit=False)
          project.owner             = Person.objects.get(user=request.user)
          project.code_request      = code_request
          project.save()
          return HttpResponseRedirect( get_prefix() + '/codematch/requests/'+str(project.id))
       else:
          print "Some form is not valid"

    return render_page(request, 'codematch/requests/new.html', {
        'projform' : proj_form,
        'reqform'  : req_form,
    })

