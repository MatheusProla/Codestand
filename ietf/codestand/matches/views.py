from ietf.codestand import constants
from django.shortcuts import get_object_or_404
from django.forms.models import modelform_factory
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from ietf.person.models import Person
from ietf.doc.models import DocAlias
from ietf.codestand.matches.forms import SearchForm, ProjectContainerForm, CodingProjectForm, LinkImplementationForm, ContactForm
from ietf.codestand.requests.forms import TagForm, DocNameForm
from ietf.codestand.matches.models import ProjectContainer, CodingProject, Implementation, ProjectTag
from ietf.codestand.helpers.utils import (render_page, is_user_allowed, clear_session, get_user)
from django.conf import settings
from django.core.paginator import Paginator


def show_list(request, is_my_list="False", att=constants.ATT_CREATION_DATE, state="False", page=1):
    """ List all CodeStand type_list (all = All CodeRequests / mylist = CodeRequests I've Created /
        mentoring = CodeRequests i'm mentoring)
        :param page: 
        :param request: HttpResponse
        :param state: string - if the state is true then the project_containers
                      has been previously loaded (eg. Loaded from the search)
        :param att: string - List will be sorted by this attribute (eg. if creation_date then ordered by date)
        :param is_my_list:
    """

    user = get_user(request)
    user_id = None
    if user:
        user_id = int(user.id)
    elif is_my_list != 'False':
        raise Http404
    all_ids = None
    if state == "True" and constants.ALL_PROJECTS in request.session:
        all_projects = request.session[constants.ALL_PROJECTS]
        all_ids = request.session[constants.ALL_CODINGS]
        request.session[constants.MAINTAIN_STATE] = True
    else:
        all_projects = ProjectContainer.objects.all()

    selected_codings = []
    if att == constants.STRING_CODER:
        all_codings = []
        codings = sorted(CodingProject.objects.all(), key=lambda p: Person.objects.get(id=p.coder))
        for c in codings:
            for proj in all_projects:
                for cod in proj.codings.all():
                    if cod == c and (not all_ids or cod.id in all_ids): 
                        all_codings.append(cod)
    else:
        all_codings = []
        codings = CodingProject.objects.order_by(att)
        for c in codings:
            for proj in all_projects:
                for cod in proj.codings.all():
                    if cod == c and (not all_ids or cod.id in all_ids):
                        all_codings.append(cod)
    ids = []

    paginator = Paginator(all_codings, 5)
    page = int(page)
    all_codings = paginator.page(page)

    for coding in all_codings:
        ids.append(coding.coder)
    ids = list(set(ids))
    all_coders = list(Person.objects.using('datatracker').filter(id__in=ids).values_list('id', 'name'))
    for coding in all_codings:
        if coding.is_archived and coding.coder != user_id:
            continue
        for project in all_projects:
            if coding in project.codings.all() and (is_my_list == "False" or user.id == coding.coder):
                coder_id = coding.coder
                coder = 'None'
                is_owner = False
                for id, name in all_coders:
                    if coder_id == id:
                        coder = name
                    if user_id is not None and coder_id == user_id:
                        is_owner = True
                selected_codings.append((coding, project, coder, coder_id, is_owner))

    keys = []
    for project_container in all_projects:
        if project_container.docs:
            keys += filter(None, project_container.docs.split(';'))
    keys = list(set(keys))
    all_documents = list(
        DocAlias.objects.using('datatracker').filter(name__in=keys).values_list('name', 'document__group__name',
                                                                                'document__group__parent__name'))
    docs = []
    areas_list = []
    working_groups_list = []
    for project_container in all_projects:
        areas = []
        working_groups = []
        # According to model areas and working groups should come from documents
        keys = []
        documents = []
        if project_container.docs:
            keys = filter(None, project_container.docs.split(';'))
        for key in keys:
            for name, gname, gparentname in all_documents:
                if name == key:
                    documents.append((gname, gparentname))
        for gname, gparentname in documents:
            if gname not in working_groups:
                working_groups.append(gname)
            if gparentname:
                if gparentname not in areas:
                    areas.append(gparentname)
            else:
                if gname not in areas:
                    areas.append(gname)
        if not areas:
            areas = [constants.STRING_NONE]
        if not working_groups:
            working_groups = [constants.STRING_NONE]
        areas_list.append((areas, project_container))
        working_groups_list.append((working_groups, project_container))

    docs = list(set(docs))
    return render_page(request, constants.TEMPLATE_MATCHES_LIST, {
        'codings': selected_codings,
        'docs': docs,
        'numpages': paginator.num_pages,
        'pages': range(1, paginator.num_pages + 1),
        'hasnext': all_codings.has_next(),
        'hasprevious': all_codings.has_previous(),
        'page': page,
        'areas_list': areas_list,
        'workinggroups_list': working_groups_list,
        'attribute': att,
        'mylist': is_my_list,
        'state': state,
        'template': "ietf.codestand.matches.views.show_list"  # TODO fix this
    })


def show(request, pk, ck):
    """ Show individual Codestand Project and Add Implementation
        :param request: HttpResponse
        :param ck: int - Indicates which coding must be loaded
        :param pk: int - Indicates which project must be loaded
    """

    project_container = get_object_or_404(ProjectContainer, id=pk)
    coding = get_object_or_404(CodingProject, id=ck)

    user = get_user(request)
    coder = Person.objects.using('datatracker').get(id=coding.coder)
    if project_container.code_request is None:
        mentor = coder
    else:
        mentor = Person.objects.using('datatracker').get(id=project_container.code_request.mentor)

    # According to model areas and working groups should come from documents
    tags = []
    keys = []
    areas = []
    if project_container.docs:
        keys = filter(None, project_container.docs.split(';'))
    docs = list(DocAlias.objects.using('datatracker').filter(name__in=keys).values_list('name', 'document__group__name',
                                                                                        'document__group__parent__name'))
    for name, gname, gparentname in docs:
        if gparentname:
            if gparentname not in areas:
                areas.append(gparentname)  # use acronym?
        else:
            areas.append(gname)
    tags += coding.tags.all()

    if not areas:
        areas = [constants.STRING_NONE]
    if not tags:
        tags = [constants.STRING_NONE]

    return render_page(request, constants.TEMPLATE_MATCHES_SHOW, {
        'projectcontainer': project_container,
        'coding': coding,
        'areas': areas,
        'tags': tags,
        'docs': docs,
        'coder': coder,
        'mentor': mentor,
        'owner': user,
        'list_template': constants.TEMPLATE_MATCHES_LIST
    })


def search(request, is_my_list="False"):
    """ Shows the list of CodeStand, filtering according to the selected checkboxes
        :param request: HttpResponse
        :param is_my_list: string - if true then must be show only my codings
    """

    search_type = request.GET.get("submit")
    if search_type:
        
        # get query field
        query = ''
        if request.GET.get(search_type):
            query = request.GET.get(search_type)

        proj_ids = []
        cod_ids = []

        valid_searches = [constants.STRING_TITLE, constants.STRING_DESCRIPTION, constants.STRING_PROTOCOL,
                          constants.STRING_CODER, constants.STRING_AREA, constants.STRING_WORKINGGROUP]

        search_in_all = True
        for v in valid_searches:
            if v in request.GET:
                search_in_all = False
                break

        if search_in_all or request.GET.get(constants.STRING_TITLE):
            codings = CodingProject.objects.all()
            for cod in codings:
                if query.lower() in cod.title.lower():
                    cod_ids.append(cod.id)

        if search_in_all or request.GET.get(constants.STRING_DESCRIPTION):
            codings = CodingProject.objects.all()
            for cod in codings:
                if query.lower() in cod.additional_information.lower():
                    cod_ids.append(cod.id)

        if request.GET.get(constants.STRING_PROTOCOL):
            proj_ids += ProjectContainer.objects.filter(protocol__icontains=query).values_list('id', flat=True)

        #Neimar 04/01/2018- didnt work if user = Person.objects.using != 1
        if search_in_all or request.GET.get(constants.STRING_CODER):
            for pr in ProjectContainer.objects.all():
                for cd in pr.codings.all():
                    for user in list(Person.objects.using('datatracker').filter(id=cd.coder)):
                        if query.lower() in user.name.lower():
                            proj_ids.append(pr.id)
                            break

        if search_in_all or request.GET.get(constants.STRING_AREA):
            for project_container in ProjectContainer.objects.all():
                docs = []
                if not project_container.docs or project_container.docs == '':
                    continue
                keys = filter(None, project_container.docs.split(';'))
                docs.extend(list(DocAlias.objects.using('datatracker').filter(name__in=keys).values_list(
                    'document__group__parent__name')))
                for doc in docs:
                    if query.lower() in doc[0].lower():
                        proj_ids.append(project_container.id)
                        break

        if search_in_all or request.GET.get(constants.STRING_WORKINGGROUP):
            for project_container in ProjectContainer.objects.all():
                docs = []
                if not project_container.docs or project_container.docs == '':
                    continue
                keys = filter(None, project_container.docs.split(';'))
                docs.extend(list(
                    DocAlias.objects.using('datatracker').filter(name__in=keys).values_list('document__group__name')))
                for doc in docs:
                    if query.lower() in doc[0].lower():
                        proj_ids.append(project_container.id)
                        break
                
        if cod_ids:
            cod_ids = list(set(cod_ids))
            proj_ids += ProjectContainer.objects.filter(codings__id__in=cod_ids).values_list('id', flat=True)
        project_containers = ProjectContainer.objects.filter(id__in=list(set(proj_ids)))
    
        request.session[constants.ALL_CODINGS] = cod_ids
        request.session[constants.ALL_PROJECTS] = project_containers

        request.session[constants.MAINTAIN_STATE] = True

        return HttpResponseRedirect(
            settings.CODESTAND_PREFIX + '/codestand/matches/show_list/' + 
            is_my_list + '/{0}/'.format(constants.ATT_CREATION_DATE) + 'True')

    else:
        return render_page(request, constants.TEMPLATE_MATCHES_SEARCH, {
            "form": SearchForm()
        })


def save_code(request, is_edit, pk, ck="", coding=None):
    """ Used to create or update a CodeRequest.
        When project container is null then a new
        instance is created in the database
        :param request: HttpResponse
        :param coding: CodingProject
        :param ck: int - Indicates which coding must be loaded
        :param pk: int - Indicates which project must be loaded
        :param is_edit: boolean
    """

    # User must have permission to add new CodeRequest
    if not is_user_allowed(request.user, "canaddcode"):
        raise Http404

    doc_form = DocNameForm()
    link_form = LinkImplementationForm()
    tag_form = modelform_factory(ProjectTag, form=TagForm)

    user = get_user(request)

    # TODO: check permission
    can_add_documents = is_user_allowed(user, "canadddocuments")
    can_add_links = is_user_allowed(user, "canaddlinks")
    can_add_tags = is_user_allowed(user, "canaddtags")
    can_add_contact = is_user_allowed(user, "canaddcontact")

    project_container = None
    if constants.ACTUAL_PROJECT in request.session:
        project_container = request.session[constants.ACTUAL_PROJECT]

    # If not there in the current session then should be setted a default
    proj_form = request.session[
        constants.PROJECT_INSTANCE] if constants.PROJECT_INSTANCE in request.session else ProjectContainerForm()
    code_form = request.session[
        constants.CODE_INSTANCE] if constants.CODE_INSTANCE in request.session else CodingProjectForm()
    contact_form = request.session[
        constants.CONTACT_INSTANCE] if constants.CONTACT_INSTANCE in request.session else ContactForm()

    docs = request.session[constants.ADD_DOCS]
    links = request.session[constants.ADD_LINKS]
    tags = request.session[constants.ADD_TAGS]
    contacts = request.session[constants.ADD_CONTACTS]

    previous_template = "codestand/matches/show_list"  # Fix this

    if constants.PREVIOUS_TEMPLATE not in request.session:
        request.session[constants.PREVIOUS_TEMPLATE] = previous_template

    if request.method == 'POST':

        implementation = LinkImplementationForm(request.POST)
        tag = TagForm(request.POST)
        new_contact = ContactForm(request.POST)
        doc_name = request.POST.get("doc")

        project = None
        new_project = None

        if coding is not None:
            new_code = CodingProjectForm(request.POST, instance=coding)
        else:
            new_code = CodingProjectForm(request.POST)

        # If there wasn't associated Project Container, must create a new one. Functionality used to legacy RFC.
        if project_container is None or project_container.code_request is None:
            post = request.POST.copy()
            post._mutable = True
            post[constants.STRING_TITLE] = post.getlist(constants.STRING_TITLE)[0]
            new_project = ProjectContainerForm(post, instance=project_container)
            if request.POST.get(constants.STRING_SAVE) and new_project.is_valid():
                 #project = new_project.save(commit=False)  # Create new
                project = new_project.save(commit=True)  # Create new #25/09/2017 - Neimar Braga - Error may to many relation
        else:
            project = project_container  # Update only

        # Adding document to the documents list to be saved in the project
        if request.POST.get(constants.STRING_LINK) and implementation.is_valid():
            new_link = implementation.save(commit=False)
            links.append(new_link)  # Updating tags to appear after rendering

        # Adding document to the documents list to be saved in the project
        elif request.POST.get(constants.STRING_DOC) and doc_name:
            selected_document = DocAlias.objects.using('datatracker').filter(name=doc_name)
            if selected_document:
                new_doc = selected_document[0]
                docs.append(new_doc)  # Updating documents to appear after rendering

        # Adding new tag to the tags list to be saved in the project
        elif request.POST.get(constants.STRING_TAG) and tag.is_valid():
            new_tag = tag.save(commit=False)
            new_tag.name = "#" + new_tag.name
            tags.append(new_tag)  # Updating tags to appear after rendering
            
        # Adding new contact to the mailing list to be saved in the project
        elif request.POST.get(constants.STRING_CONTACT) and new_contact.is_valid():
            m = new_contact.save(commit=False)
            if m.type.lower() == constants.STRING_TWITTER:
                m.contact = '@' + m.contact
            contacts.append(m)

        # Saving project (new or not) in the database
        elif request.POST.get(constants.STRING_SAVE) and project and new_code.is_valid():

            coding_project = new_code.save(commit=False)
            coding_project.coder = Person.objects.using('datatracker').get(user=request.user).id
            coding_project.save()
            project.codings.add(coding_project)
            if not project.owner:
                project.owner = Person.objects.using('datatracker').get(user=request.user).id
            project.save()

            modified = False

            rem_docs = request.session[constants.REM_DOCS]
            rem_links = request.session[constants.REM_LINKS]
            rem_tags = request.session[constants.REM_TAGS]
            rem_contacts = request.session[constants.REM_CONTACTS]

            for link in rem_links:
                coding_project.links.remove(link)
                modified = True

            for tag in rem_tags:
                coding_project.tags.remove(tag)
                modified = True

            for doc in rem_docs:
                project.docs = project.docs.replace(doc.name, '', 1)
                modified = True
                
            for m in rem_contacts:
                coding.contacts.remove(m)
                modified = True

            for link in links:
                try:
                    # Trying get an existing tag
                    new_link = Implementation.objects.get(link=link.link)
                except:
                    # Otherwise you need to create a new tag
                    link.save()
                    new_link = link

                # Save the tag in the project (existing or new)
                coding_project.links.add(new_link)
                modified = True

            for tag in tags:
                try:
                    # Trying get an existing tag
                    new_tag = ProjectTag.objects.get(name=tag.name)
                except:
                    # Otherwise you need to create a new tag
                    tag.save()
                    new_tag = tag

                # Save the tag in the project (existing or new)
                coding_project.tags.add(new_tag)
                modified = True
                
            for m in contacts:
                try:
                    # Trying get an existing contact
                    new_m = CodingProject.objects.get(contact=m.contact, type=m.type)
                except:
                    # Otherwise you need to create a new contact
                    m.save()
                    new_m = m

                coding_project.contacts.add(new_m)
                modified = True

            for doc in docs:
                keys = project.docs
                if keys is None:
                    project.docs = '{};'.format(doc.name)
                else:
                    if doc.name not in project.docs:
                        project.docs += '{};'.format(doc.name)
                modified = True

            if modified:
                coding_project.save()
                project.save()

            return HttpResponseRedirect(
                settings.CODESTAND_PREFIX + "/codestand/matches/" + str(project.id) + '/' + str(coding_project.id))

        # Updating session variables
        # if new_project != None and ( project_container == None or project_container.code_request != None ):
        if new_project is not None:
            request.session[constants.PROJECT_INSTANCE] = new_project
            proj_form = new_project

        request.session[constants.CODE_INSTANCE] = new_code
        code_form = new_code

    return render_page(request, constants.TEMPLATE_MATCHES_NEW, {
        'projectcontainer': project_container,
        'isedit': is_edit,
        'projform': proj_form,
        'codeform': code_form,
        'linkform': link_form,
        'tagform': tag_form,
        'docform': doc_form,
        'contactform': contact_form,
        'pk': pk,
        'ck': ck,
        'links': links,
        'tags': tags,
        'docs': docs,
        'contacts': contacts,
        'canadddocuments': can_add_documents,
        'canaddlinks': can_add_links,
        'canaddtags': can_add_tags,
        'canaddcontact': can_add_contact
    })


@login_required(login_url=settings.CODESTAND_PREFIX + constants.TEMPLATE_LOGIN)
def archive(request, ck):

    user = get_user(request)
    coding_project = get_object_or_404(CodingProject, id=ck)
    if coding_project.coder != user.id:
        raise Http404

    coding_project.is_archived = not coding_project.is_archived
    coding_project.save()

    refresh_template = request.session[constants.ACTUAL_TEMPLATE]
    return HttpResponseRedirect(refresh_template)


@login_required(login_url=settings.CODESTAND_PREFIX + constants.TEMPLATE_LOGIN)
def edit(request, pk, ck):
    """ Edit CodeRequest Entry
        :param request: HttpResponse
        :param pk: int - Indicates which project must be loaded
        :param ck: int - Indicates which coding must be loaded
    """

    project_container = get_object_or_404(ProjectContainer, id=pk)
    coding = get_object_or_404(CodingProject, id=ck)

    if request.path != request.session[constants.ACTUAL_TEMPLATE]:
        clear_session(request)
        request.session[constants.REM_LINKS] = []
        request.session[constants.REM_TAGS] = []
        request.session[constants.REM_DOCS] = []
        request.session[constants.REM_CONTACTS] = []

    request.session[constants.MAINTAIN_STATE] = True

    # Fills session variables with project values already saved

    if constants.ADD_LINKS not in request.session:
        links = coding.links.all()
        request.session[constants.ADD_LINKS] = list(links)

    if constants.ADD_TAGS not in request.session:
        tags = coding.tags.all()
        request.session[constants.ADD_TAGS] = list(tags)
        
    if constants.ADD_CONTACTS not in request.session:
        contacts = coding.contacts.all()
        request.session[constants.ADD_CONTACTS] = list(contacts)

    if constants.ADD_DOCS not in request.session:
        docs = []
        if project_container.docs:
            keys = filter(None, project_container.docs.split(';'))
            for key in keys:
                docs.append(DocAlias.objects.using('datatracker').get(name=key))
        request.session[constants.ADD_DOCS] = list(docs)
     
    us = get_user(request)
    user = us

    # Project must have been created by the current user and
    # User must have permission to add new CodeRequest
    if coding.coder != user.id:
        raise Http404

    # Save project and code request in the cache to make 'update' and 'new' use the same code (save_project)
    if project_container.code_request is None:
        request.session[constants.PROJECT_INSTANCE] = ProjectContainerForm(instance=project_container)
    request.session[constants.ACTUAL_PROJECT] = project_container
    request.session[constants.CODE_INSTANCE] = CodingProjectForm(instance=coding)

    return save_code(request, True, pk, ck, coding)


@login_required(login_url=settings.CODESTAND_PREFIX + constants.TEMPLATE_LOGIN)
def new(request, pk=""):
    """ New CodeStand Entry
        When user presses 'Associate new project' there is a Project Container
        associated, then you need reuse this information in the form
        :param request: HttpResponse
        :param pk: int - Indicates which project must be loaded
    """

    if request.path != request.session[constants.ACTUAL_TEMPLATE]:
        clear_session(request)
        request.session[constants.REM_LINKS] = []
        request.session[constants.REM_TAGS] = []
        request.session[constants.REM_DOCS] = []
        request.session[constants.REM_CONTACTS] = []
        request.session[constants.ADD_CONTACTS] = []
        request.session[constants.ADD_LINKS] = []
        request.session[constants.ADD_TAGS] = []
        request.session[constants.ADD_DOCS] = []

    request.session[constants.MAINTAIN_STATE] = True

    if pk != "":
        request.session[constants.ACTUAL_PROJECT] = get_object_or_404(ProjectContainer, id=pk)

    # User must have permission to add new CodeStand
    if not is_user_allowed(request.user, "canaddmatch"):
        raise Http404

    return save_code(request, False, pk)


@login_required(login_url=settings.CODESTAND_PREFIX + constants.TEMPLATE_LOGIN)
def remove_link(request, ck, link_name):
    """ Adds the removal list, but will only be removed when saving changes
        ck (ck = 0 - new CodeStand / ck > 0 edit CodeStand
        :param request: HttpResponse
        :param ck: int - Indicates which coding must be loaded
        :param link_name: string - Indicates which link must be removed
    """

    refresh_template = request.session[constants.ACTUAL_TEMPLATE]

    links = request.session[constants.ADD_LINKS]
    if '://' not in link_name:
        link_name = link_name.replace(':/', '://')
    link = next(el for el in links if el.link == link_name)
    if ck != "0":
        coding = get_object_or_404(CodingProject, id=ck)
       
        us = get_user(request)
        user = us

        # Coding must have been created by the current user and
        if coding.coder != user.id:
            raise Http404

        if coding.links.filter(link=link_name):
            cache_list = request.session[constants.REM_LINKS]
            cache_list.append(link)

    links.remove(link)
    request.session[constants.ADD_LINKS] = links

    return HttpResponseRedirect(refresh_template)


@login_required(login_url=settings.CODESTAND_PREFIX + constants.TEMPLATE_LOGIN)
def delete(request, pk, ck, template=None):
    
    project = get_object_or_404(ProjectContainer, id=pk)
    coding = get_object_or_404(CodingProject, id=ck)
    user = get_user(request)
    
    if coding.coder != user.id:
        raise Http404
    
    if not project.code_request:
        project.delete()
    coding.delete()
    
    if not template:
        template = request.session[constants.ACTUAL_TEMPLATE]
        return HttpResponseRedirect(template)
    else:
        return HttpResponseRedirect('/codestand/matches/show_list/')


@login_required(login_url=settings.CODESTAND_PREFIX + constants.TEMPLATE_LOGIN)
def remove_contact(request, ck, contact_name):
    """ Adds the removal list, but will only be removed when saving changes
        pk (pk = 0 - new ProjectContainer / pk > 0 - edit ProjectContainer
        :param request: HttpResponse
        :param ck: int - Indicates which project must be loaded
        :param contact_name: string - Indicates which contact must be loaded
    """

    refresh_template = request.session[constants.ACTUAL_TEMPLATE]

    contacts = request.session[constants.ADD_CONTACTS]
    contact = next(el for el in contacts if el.contact == contact_name)

    if ck != "0":
        coding = get_object_or_404(CodingProject, id=ck)
     
        us = get_user(request)
        user = us

        # Project must have been created by the current user
        if coding.coder != user.id:
            raise Http404

        if coding.contacts.filter(contact=contact_name):
            cache_list = request.session[constants.REM_CONTACTS]
            cache_list.append(contact)

    contacts.remove(contact)
    request.session[constants.ADD_CONTACTS] = contacts

    return HttpResponseRedirect(refresh_template)


@login_required(login_url=settings.CODESTAND_PREFIX + constants.TEMPLATE_LOGIN)
def remove_tag(request, ck, tag_name):
    """ Adds the removal list, but will only be removed when saving changes
        ck (ck = 0 - new CodeStand / ck > 0 edit CodeStand
        :param request: HttpResponse
        :param ck: int - Indicates which coding must be loaded
        :param tag_name: string - Indicates which tag must be removed
    """

    refresh_template = request.session[constants.ACTUAL_TEMPLATE]

    tags = request.session[constants.ADD_TAGS]
    tag = next(el for el in tags if el.name == tag_name)

    if ck != "0":
        coding = get_object_or_404(CodingProject, id=ck)
       
        us = get_user(request)
        user = us

        # Coding must have been created by the current user
        if coding.coder != user.id:
            raise Http404

        if coding.tags.filter(name=tag_name):
            cache_list = request.session[constants.REM_TAGS]
            cache_list.append(tag)

    tags.remove(tag)
    request.session[constants.ADD_TAGS] = tags

    return HttpResponseRedirect(refresh_template)


@login_required(login_url=settings.CODESTAND_PREFIX + constants.TEMPLATE_LOGIN)
def remove_document(request, pk, doc_name):
    """ Adds the removal list, but will only be removed when saving changes
        pk (pk = 0 - new ProjectContainer / pk > 0 - edit ProjectContainer
        :param request: HttpResponse
        :param pk: int - Indicates which project must be loaded
        :param doc_name: string  - Indicates which document must be removed
    """

    refresh_template = request.session[constants.ACTUAL_TEMPLATE]

    docs = request.session[constants.ADD_DOCS]
    document = next(el for el in docs if el.name == doc_name)

    if pk != "0":
        project_container = get_object_or_404(ProjectContainer, id=pk)
        
        us = get_user(request)
        user = us

        # Project must have been created by the current user
        if project_container.owner != user.id:
            raise Http404

        if project_container.docs.filter(name=doc_name):
            cache_list = request.session[constants.REM_DOCS]
            cache_list.append(document)

    docs.remove(document)
    request.session[constants.ADD_DOCS] = docs

    return HttpResponseRedirect(refresh_template)
