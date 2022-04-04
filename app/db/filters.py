class Filter:
    def __init__(self, f: 'Filter'):
        self.filter = f

    def keys_to_str(self):
        pass

    def values_for_query(self):
        pass


class ColumnFilter(Filter):
    def __init__(self, name: str, value: any, f: 'Filter'):
        super().__init__(f)
        self.name = name
        self.value = value


class AndFilter(Filter):
    pass


class OrFilter(Filter):
    pass


class DateFilter(Filter):
    pass
