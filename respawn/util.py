class ToStringMixin(object):
    def __str__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        return unicode(self.to_string())


class SetNonEmptyPropertyMixin(object):
    def _set_property(self, k, v):
        if k and v:
            self[k]=v

