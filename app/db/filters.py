class Filter:
    def __init__(self, f: 'Filter'):
        self.filter = f

    def to_str(self):
        pass


class ColumnFilter(Filter):
    def __init__(self, name: str, value: any):
        self.name = name
        self.value = value


class AndFilter(Filter):
    pass


class OrFilter(Filter):
    pass


class DateFilter(Filter):
    pass
