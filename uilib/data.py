class namespace(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        return None
    
    def __setattr__(self, attr, val):
        self[attr] = val