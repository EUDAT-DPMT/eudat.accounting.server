from zope.interface import alsoProvides
from Products.Five.browser import BrowserView
from Products.BTreeFolder2.BTreeFolder2 import manage_addBTreeFolder
from eudat.accounting.server.interfaces import IAccount

class DomainView(BrowserView):
    """Browser views of a domain"""

    def addAccount(self, id, title='', owner=None):
        """
        Add an account within a domain
        The id is usually the (P)ID of a resource
        Pass in the userid of the account owner
        If not provided the caller will own the account
        """
        manage_addBTreeFolder(self.context, id=id, title=title)
        account = self.context[id]
        alsoProvides(account, IAccount)
        if owner is not None:
            # careful: this works even if no user 'owner' exists
            # TODO: add check here?
            account.manage_addLocalRoles(owner, ['Owner'])
        return "Account '%s (%s)' created." % (id, title)

