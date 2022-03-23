class Data():
    def __init__(self, **kwargs):
        self.website = kwargs.get('website')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')