import json

from zope.interface import alsoProvides
from Products.Five.browser import BrowserView
from Products.BTreeFolder2.BTreeFolder2 import manage_addBTreeFolder
from eudat.accounting.server.interfaces import IAccount

class DomainView(BrowserView):
    """Browser views of a domain"""

    def hasAccount(self, id):
        """ Check if the current Domain folder has an account with ID ``id`` """
        self.request.response.setHeader('content-type', 'application/json')
        return json.dumps(dict(exists=id in self.context.objectIds()))

    def addAccount(self, id, title='', owner=None):
        """
        Add an account within a domain
        The id is usually the (P)ID of a resource
        Pass in the userid of the account owner
        If not provided the caller will own the account
        """

        if id in self.context.objectIds():
            self.request.response.setStatus(500)
            return 'Folder "{}" already exists'.format(id)

        if owner:
            user = self.context.acl_users.getUser(owner)
            if not user:
                self.request.response.setStatus(500)
                return 'No account for "{}" found - unable to set owner role'.format(owner)


        manage_addBTreeFolder(self.context, id=id, title=title)
        account = self.context[id]
        alsoProvides(account, IAccount)
        account.manage_addProperty('grace_period_days', 7, 'int')
        if owner is not None:
            account.manage_addLocalRoles(owner, ['Owner'])
        self.request.response.setStatus(201)
        return 'Account {} ({}) created'.format(id, title)

