class DatabaseInterface:
    def connect(self, *args):
        raise NotImplementedError()

    def execute_query(self, *args):
        raise NotImplementedError()