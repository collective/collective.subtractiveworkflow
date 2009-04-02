Introduction
============

This product provides an alternative type of workflow definition. It works
much like a regular workflow, but instead of granting permissions when 
entering a particular state, it takes them away from the selected roles.

The original use case was to support "confidential" content items via a
secondary workflow. The primary chain on the type has a publishing workflow
that will grant the View permission to various roles in various states. The
secondary 'confidentiality workflow' has two states: 'normal' and
'confidential'. In the 'normal' state, no roles are selected for the View
permission, and so the role mappings from the primary workflow apply. However,
in the 'confidential' state, Anonymous, Authenticated and Member have been
selected for the View permission and so these roles no longer have the ability
to view the item.

Note that the 'acquire' flag should almost always be off. The subtractive
workflow will set the acquire property in the same way as the default
workflow definition, but the results will probably not be what you expect,
since permissions that were "turned off" may well be acquired.

Also note that groups loocal role mappings are not "subtractive" and work
exactly as in the standard workflow definition. In general, local roles are
always inherited in Zope (although Plone has an extension to turn this off).

Finally, note that there is an event handler installed which will perform the
permission "subtraction" after a transition in a non-subtractive workflow
in the chain for all subtractive workflows defined *later* in the chain. In
the scenario above, this means that if an item is marked 'confidential' (and
so the View permission should be removed from Anonymous, Authenticated and
Member) and then goes from 'private' to 'published' (which would normally
grant View to Anonymous), the event handler will adjust the permissions
according to the rules of the secondary, subtractive workflow. However, if
the subtractive workflow had been earlier in the chain, the permission
adjustment would be skipped.

