from Products.Five.browser import BrowserView

class AccountView(BrowserView):
    """Browser views of a domain"""

    def addRecord(self, core, meta=None, key=None):
        """
        Add a record to an account
        Use a timestamp created from the current time (UTC)
        as key unless specifically provided
        The core elements need to be provided.
        Metadata is optional
        Return the key under which teh record has been created
        """
        return "Hello World from a record"

    def listRecords(self, n=10):
        """List the last n records (default: 10)"""
        # for now just return the objectIds
        return self.context.objectIds()
