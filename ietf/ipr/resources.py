# Autogenerated by the mkresources management command 2015-03-21 14:05 PDT
from tastypie.resources import ModelResource
from tastypie.fields import ToOneField, ToManyField     # pyflakes:ignore
from tastypie.constants import ALL, ALL_WITH_RELATIONS  # pyflakes:ignore

from ietf import api

from ietf.ipr.models import *                            # pyflakes:ignore


from ietf.person.resources import PersonResource
from ietf.name.resources import IprDisclosureStateNameResource
from ietf.doc.resources import DocAliasResource
class IprDisclosureBaseResource(ModelResource):
    by               = ToOneField(PersonResource, 'by')
    state            = ToOneField(IprDisclosureStateNameResource, 'state')
    docs             = ToManyField(DocAliasResource, 'docs', null=True)
    rel              = ToManyField('ietf.ipr.resources.IprDisclosureBaseResource', 'rel', null=True)
    class Meta:
        queryset = IprDisclosureBase.objects.all()
        #resource_name = 'iprdisclosurebase'
        filtering = { 
            "id": ALL,
            "compliant": ALL,
            "holder_legal_name": ALL,
            "notes": ALL,
            "other_designations": ALL,
            "submitter_name": ALL,
            "submitter_email": ALL,
            "time": ALL,
            "title": ALL,
            "by": ALL_WITH_RELATIONS,
            "state": ALL_WITH_RELATIONS,
            "docs": ALL_WITH_RELATIONS,
            "rel": ALL_WITH_RELATIONS,
        }
api.ipr.register(IprDisclosureBaseResource())

from ietf.doc.resources import DocAliasResource
class IprDocRelResource(ModelResource):
    disclosure       = ToOneField(IprDisclosureBaseResource, 'disclosure')
    document         = ToOneField(DocAliasResource, 'document')
    class Meta:
        queryset = IprDocRel.objects.all()
        #resource_name = 'iprdocrel'
        filtering = { 
            "id": ALL,
            "sections": ALL,
            "revisions": ALL,
            "disclosure": ALL_WITH_RELATIONS,
            "document": ALL_WITH_RELATIONS,
        }
api.ipr.register(IprDocRelResource())

from ietf.person.resources import PersonResource
from ietf.name.resources import IprDisclosureStateNameResource, IprLicenseTypeNameResource
from ietf.doc.resources import DocAliasResource
class HolderIprDisclosureResource(ModelResource):
    by               = ToOneField(PersonResource, 'by')
    state            = ToOneField(IprDisclosureStateNameResource, 'state')
    iprdisclosurebase_ptr = ToOneField(IprDisclosureBaseResource, 'iprdisclosurebase_ptr')
    licensing        = ToOneField(IprLicenseTypeNameResource, 'licensing')
    docs             = ToManyField(DocAliasResource, 'docs', null=True)
    rel              = ToManyField(IprDisclosureBaseResource, 'rel', null=True)
    class Meta:
        queryset = HolderIprDisclosure.objects.all()
        #resource_name = 'holderiprdisclosure'
        filtering = { 
            "id": ALL,
            "compliant": ALL,
            "holder_legal_name": ALL,
            "notes": ALL,
            "other_designations": ALL,
            "submitter_name": ALL,
            "submitter_email": ALL,
            "time": ALL,
            "title": ALL,
            "ietfer_name": ALL,
            "ietfer_contact_email": ALL,
            "ietfer_contact_info": ALL,
            "patent_info": ALL,
            "has_patent_pending": ALL,
            "holder_contact_email": ALL,
            "holder_contact_name": ALL,
            "holder_contact_info": ALL,
            "licensing_comments": ALL,
            "submitter_claims_all_terms_disclosed": ALL,
            "by": ALL_WITH_RELATIONS,
            "state": ALL_WITH_RELATIONS,
            "iprdisclosurebase_ptr": ALL_WITH_RELATIONS,
            "licensing": ALL_WITH_RELATIONS,
            "docs": ALL_WITH_RELATIONS,
            "rel": ALL_WITH_RELATIONS,
        }
api.ipr.register(HolderIprDisclosureResource())

from ietf.person.resources import PersonResource
from ietf.name.resources import IprDisclosureStateNameResource
from ietf.doc.resources import DocAliasResource
class ThirdPartyIprDisclosureResource(ModelResource):
    by               = ToOneField(PersonResource, 'by')
    state            = ToOneField(IprDisclosureStateNameResource, 'state')
    iprdisclosurebase_ptr = ToOneField(IprDisclosureBaseResource, 'iprdisclosurebase_ptr')
    docs             = ToManyField(DocAliasResource, 'docs', null=True)
    rel              = ToManyField(IprDisclosureBaseResource, 'rel', null=True)
    class Meta:
        queryset = ThirdPartyIprDisclosure.objects.all()
        #resource_name = 'thirdpartyiprdisclosure'
        filtering = { 
            "id": ALL,
            "compliant": ALL,
            "holder_legal_name": ALL,
            "notes": ALL,
            "other_designations": ALL,
            "submitter_name": ALL,
            "submitter_email": ALL,
            "time": ALL,
            "title": ALL,
            "ietfer_name": ALL,
            "ietfer_contact_email": ALL,
            "ietfer_contact_info": ALL,
            "patent_info": ALL,
            "has_patent_pending": ALL,
            "by": ALL_WITH_RELATIONS,
            "state": ALL_WITH_RELATIONS,
            "iprdisclosurebase_ptr": ALL_WITH_RELATIONS,
            "docs": ALL_WITH_RELATIONS,
            "rel": ALL_WITH_RELATIONS,
        }
api.ipr.register(ThirdPartyIprDisclosureResource())

from ietf.name.resources import DocRelationshipNameResource
class RelatedIprResource(ModelResource):
    source           = ToOneField(IprDisclosureBaseResource, 'source')
    target           = ToOneField(IprDisclosureBaseResource, 'target')
    relationship     = ToOneField(DocRelationshipNameResource, 'relationship')
    class Meta:
        queryset = RelatedIpr.objects.all()
        #resource_name = 'relatedipr'
        filtering = { 
            "id": ALL,
            "source": ALL_WITH_RELATIONS,
            "target": ALL_WITH_RELATIONS,
            "relationship": ALL_WITH_RELATIONS,
        }
api.ipr.register(RelatedIprResource())

from ietf.person.resources import PersonResource
from ietf.name.resources import IprDisclosureStateNameResource
from ietf.doc.resources import DocAliasResource
class NonDocSpecificIprDisclosureResource(ModelResource):
    by               = ToOneField(PersonResource, 'by')
    state            = ToOneField(IprDisclosureStateNameResource, 'state')
    iprdisclosurebase_ptr = ToOneField(IprDisclosureBaseResource, 'iprdisclosurebase_ptr')
    docs             = ToManyField(DocAliasResource, 'docs', null=True)
    rel              = ToManyField(IprDisclosureBaseResource, 'rel', null=True)
    class Meta:
        queryset = NonDocSpecificIprDisclosure.objects.all()
        #resource_name = 'nondocspecificiprdisclosure'
        filtering = { 
            "id": ALL,
            "compliant": ALL,
            "holder_legal_name": ALL,
            "notes": ALL,
            "other_designations": ALL,
            "submitter_name": ALL,
            "submitter_email": ALL,
            "time": ALL,
            "title": ALL,
            "holder_contact_name": ALL,
            "holder_contact_email": ALL,
            "holder_contact_info": ALL,
            "patent_info": ALL,
            "has_patent_pending": ALL,
            "statement": ALL,
            "by": ALL_WITH_RELATIONS,
            "state": ALL_WITH_RELATIONS,
            "iprdisclosurebase_ptr": ALL_WITH_RELATIONS,
            "docs": ALL_WITH_RELATIONS,
            "rel": ALL_WITH_RELATIONS,
        }
api.ipr.register(NonDocSpecificIprDisclosureResource())

from ietf.person.resources import PersonResource
from ietf.name.resources import IprDisclosureStateNameResource
from ietf.doc.resources import DocAliasResource
class GenericIprDisclosureResource(ModelResource):
    by               = ToOneField(PersonResource, 'by')
    state            = ToOneField(IprDisclosureStateNameResource, 'state')
    iprdisclosurebase_ptr = ToOneField(IprDisclosureBaseResource, 'iprdisclosurebase_ptr')
    docs             = ToManyField(DocAliasResource, 'docs', null=True)
    rel              = ToManyField(IprDisclosureBaseResource, 'rel', null=True)
    class Meta:
        queryset = GenericIprDisclosure.objects.all()
        #resource_name = 'genericiprdisclosure'
        filtering = { 
            "id": ALL,
            "compliant": ALL,
            "holder_legal_name": ALL,
            "notes": ALL,
            "other_designations": ALL,
            "submitter_name": ALL,
            "submitter_email": ALL,
            "time": ALL,
            "title": ALL,
            "holder_contact_name": ALL,
            "holder_contact_email": ALL,
            "holder_contact_info": ALL,
            "statement": ALL,
            "by": ALL_WITH_RELATIONS,
            "state": ALL_WITH_RELATIONS,
            "iprdisclosurebase_ptr": ALL_WITH_RELATIONS,
            "docs": ALL_WITH_RELATIONS,
            "rel": ALL_WITH_RELATIONS,
        }
api.ipr.register(GenericIprDisclosureResource())

from ietf.person.resources import PersonResource
from ietf.message.resources import MessageResource
from ietf.name.resources import IprEventTypeNameResource
class IprEventResource(ModelResource):
    type             = ToOneField(IprEventTypeNameResource, 'type')
    by               = ToOneField(PersonResource, 'by')
    disclosure       = ToOneField(IprDisclosureBaseResource, 'disclosure')
    message          = ToOneField(MessageResource, 'message', null=True)
    in_reply_to      = ToOneField(MessageResource, 'in_reply_to', null=True)
    class Meta:
        queryset = IprEvent.objects.all()
        #resource_name = 'iprevent'
        filtering = { 
            "id": ALL,
            "time": ALL,
            "desc": ALL,
            "response_due": ALL,
            "type": ALL_WITH_RELATIONS,
            "by": ALL_WITH_RELATIONS,
            "disclosure": ALL_WITH_RELATIONS,
            "message": ALL_WITH_RELATIONS,
            "in_reply_to": ALL_WITH_RELATIONS,
        }
api.ipr.register(IprEventResource())

from ietf.person.resources import PersonResource
from ietf.message.resources import MessageResource
from ietf.name.resources import IprEventTypeNameResource
class LegacyMigrationIprEventResource(ModelResource):
    type             = ToOneField(IprEventTypeNameResource, 'type')
    by               = ToOneField(PersonResource, 'by')
    disclosure       = ToOneField(IprDisclosureBaseResource, 'disclosure')
    message          = ToOneField(MessageResource, 'message', null=True)
    in_reply_to      = ToOneField(MessageResource, 'in_reply_to', null=True)
    iprevent_ptr     = ToOneField(IprEventResource, 'iprevent_ptr')
    class Meta:
        queryset = LegacyMigrationIprEvent.objects.all()
        #resource_name = 'legacymigrationiprevent'
        filtering = { 
            "id": ALL,
            "time": ALL,
            "desc": ALL,
            "response_due": ALL,
            "type": ALL_WITH_RELATIONS,
            "by": ALL_WITH_RELATIONS,
            "disclosure": ALL_WITH_RELATIONS,
            "message": ALL_WITH_RELATIONS,
            "in_reply_to": ALL_WITH_RELATIONS,
            "iprevent_ptr": ALL_WITH_RELATIONS,
        }
api.ipr.register(LegacyMigrationIprEventResource())
