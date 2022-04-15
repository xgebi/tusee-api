class Column:
    """

    """
    def __init__(self, data_type: type, nullable: bool = False, primary_key: bool = False, value=None, default=None):
        """
        Constructor for Column class

        :param data_type:
        :param nullable:
        :param primary_key:
        :param value:
        :param default:
        """
        self.data_type = data_type
        self.nullable = nullable
        self.primary_key = primary_key
        self.default = default
        if not nullable and default is None and value is None:
            raise Exception('nullable needs to have a value or default value')
        elif default is not None and value is None:
            self.value = default
        else:
            self.value = value

    def set(self, value):
        if not self.nullable and value is None:
            raise Exception('column value cannot be NULL')
        self.value = value
