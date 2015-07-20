from django.db import models

import debug
import datetime

from ietf.group.models import Group
from ietf.person.models import Person
from ietf.doc.models import DocAlias

class CodeRequest (models.Model):
    """ A CodeRequest is additional information to a Project Container"""
    """ Some elements in the project Container do not have a CodeRequest"""
    """ because they're Past projects or may haven't been formaly """
    """ requested by an author """

    #Estimated Level of Effort
    estimated_lof          = models.CharField(max_length=80)
    # The author can include additional text to describe his request
    additional_information = models.CharField(max_length=255)
    coder                  = models.ForeignKey(Person)
    creation_date          = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.additional_information