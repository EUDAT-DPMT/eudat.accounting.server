import json
import time
from datetime import datetime

from BTrees.IOBTree import IOBTree
from persistent.mapping import PersistentMapping

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
        Return the key under which the record has been created
        """

        grace_period_days = getattr(self, 'grace_period_days', 7)
        now = datetime.utcnow()

        try:
            data = self.context._data
        except AttributeError:
            data = self.context._data = IOBTree()

        if key is None:
            key = int(time.time())  # Seconds since 1.1.1970 0:00 UTC
            submission_t = datetime.utcfromtimestamp(key)

        else:
            key = int(key)
            key_dt = datetime.utcfromtimestamp(key)
            submission_t = datetime.utcnow()
            if key_dt >= now:
                raise ValueError('Timestamp is in future...time travel?')
            if (now - key_dt).days > grace_period_days:
                raise ValueError('Timestamp is outside grace period of {} days'.format(grace_period_days))

        meta = meta or {}
        meta = dict(meta)
        meta['submission_time'] = submission_t.isoformat(' ')
        record = PersistentMapping()
        record['core'] = dict(core)
        record['meta'] = meta
        data[key] = record
        return key

    def listRecordKeys(self, n=10):
        """List the last n records keys (default: 10)"""
        n = int(n) + 1
        try:
            data = self.context._data
        except AttributeError:
            # no records yet
            return []
        result = list(self.context._data.keys())[:-n:-1]
        return result

    def listRecords(self, n=10):
        """List the last n record items (keys and values)
        as JSON"""
        n = int(n) + 1
        result = []
        try:
            data = self.context._data
        except AttributeError:
            data = {}

        keys = list(data.keys())[:-n:-1]
        for k in keys:
            v = dict(data[k])
            v['meta']['ts'] = k
            result.append(v)
        json_data = json.dumps(result, indent=4)
        self.request.response.setHeader('Content-type', 'application/json')
        self.request.response.setHeader('Content-length', str(len(json_data)))
        return json_data

    def dumpJson(self):
        account = self.context
        records = getattr(account, '_data', None)

        values = {k: v for k, v in account.propertyItems()}

        if records:
            values['records'] = {k: v for k, v in records.objectMap()}

        return json.dumps(values)
