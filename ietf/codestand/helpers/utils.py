from ietf.codestand import constants
from django.shortcuts import render
from ietf.person.models import Person, Alias
from ietf.codestand.matches.models import ProjectContainer, CodingProject
from django.conf import settings
import pprint
import json
import requests


# ----------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------

def is_user_allowed(user, permission):
    """ Check if the user has permission
        :param permission:
        :param user:
    """
    print user, permission
    return True


def get_user(request):
    if constants.USER not in request.session or request.session[constants.USER].user != request.user:
        if request.user.is_authenticated():
            user = Person.objects.using('datatracker').get(user=request.user)
            request.session[constants.USER] = user
            return user
        else:
            return None
    else:
        return request.session[constants.USER]


def get_menu_arguments(request, keys):
    user = get_user(request)

    # Always setted
    keys['from'] = request.GET.get('from', None)
    keys['codestand_debug'] = settings.CODESTAND_DEBUG
    keys['codestand_version'] = constants.VERSION
    keys['codestand_revision_date'] = constants.RELEASE_DATE

    if user is not None:  # Only when user is logged

        my_codings = CodingProject.objects.filter(coder=user.id)
        my_own_projects = ProjectContainer.objects.filter(owner=user.id)
        my_mentoring_projects = ProjectContainer.objects.filter(code_request__mentor=user.id)

        # Some tests are made on the templates, should be here in the code?

        keys["mycodings"] = my_codings
        keys["projectsowner"] = my_own_projects
        keys["projectsmentoring"] = my_mentoring_projects

        keys["canaddcoding"] = is_user_allowed(user, "canaddcoding")
        keys["canaddrequest"] = is_user_allowed(user, "canaddrequest")
        keys["ismentor"] = is_user_allowed(user, "ismentor")

        # Try get pretty name user (otherwise, email will be used)
        alias = Alias.objects.using('datatracker').filter(person=user)

        alias_name = alias[0].name if alias else user.name

        keys["username"] = alias_name

    return keys


def clear_session(request):
    # All session variables
    keys = [constants.ALL_PROJECTS, constants.PROJECT_INSTANCE, constants.REQUEST_INSTANCE, constants.CONTACT_INSTANCE,
            constants.ACTUAL_PROJECT, constants.MENTOR_INSTANCE, constants.IS_MENTOR,
            constants.CODE_INSTANCE, constants.ADD_DOCS, constants.ADD_TAGS, constants.ADD_LINKS,
            constants.ADD_CONTACTS,
            constants.REM_CONTACTS, constants.REM_DOCS, constants.REM_TAGS, constants.REM_LINKS]

    # If MAINTAIN_STATE is true then session variables shouldn't be deleted
    if constants.MAINTAIN_STATE in request.session and request.session[constants.MAINTAIN_STATE] == True:
        del request.session[constants.MAINTAIN_STATE]
    else:  # Otherwise all session variables must be erased
        for key in keys:
            if key in request.session:
                del request.session[key]


def render_page(request, template, keys=None):
    """ Special method for rendering pages
        :param keys:
        :param template:
        :param request:
    """
    if not keys:
        keys = {}

    clear_session(request)

    # if the template has changed then update actual and previous templates
    if constants.ACTUAL_TEMPLATE in request.session:
        actual_template = request.session[constants.ACTUAL_TEMPLATE]
        if actual_template != request.path:
            request.session[constants.PREVIOUS_TEMPLATE] = actual_template

    request.session[constants.ACTUAL_TEMPLATE] = request.path

    return render(request, template, get_menu_arguments(request, keys))



def googleSearchApi(term):
    searchResult = []
    try:      
        api_key='AIzaSyCAsmtGQqlw4fnAU1J9MVvmJTe0XMiDeco'

        result = requests.get('https://content.googleapis.com/customsearch/v1', 
            params={ 'cx': '004640575567140933121:sqsoy1bwcq8', 'q': term, 'key': api_key} )
        
        resultJson = result.json()
        #pprint.pprint(resultJson)
        
        searchResult = []
        for item in resultJson['items']:
            title = item['title']
            snippet = item['snippet']
            link = item['link']
            
            searchResult.append((title, snippet, link))
        return searchResult
    except:
        searchResult.append(('No results', '', ''))
        return searchResult