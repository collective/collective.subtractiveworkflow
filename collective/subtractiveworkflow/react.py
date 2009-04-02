from zope.component import adapter
from Products.DCWorkflow.interfaces import IAfterTransitionEvent

from Products.CMFCore.utils import getToolByName

from collective.subtractiveworkflow.interfaces import ISubtractiveWorkflowDefinition

@adapter(IAfterTransitionEvent)
def object_transitioned(event):
    """Subtractive workflows need to be able to modify the permissions of an
    object after other workflows may have done their work. This event handler
    will be called after a transition has been invoked.
    """
    
    # On create, there's no transition. Do nothing.
    if event.transition is None:
        return

    obj = event.object
    wf_tool = getToolByName(obj, 'portal_workflow', None)
    
    if wf_tool is None:
        return
    
    # Find the chain for the object. Update security settings for all
    # subtractive workflows *after* the one that executed the transition.
    
    found = False
    transition_workflow_id = event.workflow.getId()
    
    for wf_id in wf_tool.getChainFor(obj):
        if wf_id == transition_workflow_id:
            found = True
        elif found:
            wf = wf_tool.getWorkflowById(wf_id)
            if ISubtractiveWorkflowDefinition.providedBy(wf):
                wf.updateRoleMappingsFor(obj)