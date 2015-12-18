class SetNonEmptyPropertyMixin(object):
    def _set_property(self, k, v):
        if k and v:
            self[k] = v
