from Products.Five.browser import BrowserView

class DomainView(BrowserView):
    """Browser views of a domain"""

    def addAccount(self, id=None, owner=None):
        """
        Add an account within a domain
        The id is usually the (P)ID of a resource
        Pass in the userid of the account owner
        If not provided the caller will own the account
        """
        return "Hello World from an account"
