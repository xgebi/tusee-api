from typing import List


class FilterFactory:
    @staticmethod
    def new_and_filter():
        pass


class Filter:
    def __init__(self):
        self.conditions = []

    def collect_query_fragments(self) -> str:
        return self.conditions[0].to_query_string() if len(self.conditions) > 0 else ''

    def collect_values(self):
        return [item for sublist in self.conditions for item in sublist.query_values()]

    def add_condition(self, condition: 'Condition'):
        self.conditions.append(condition)


class TopFilter(Filter):
    def __init__(self, top_filter: Filter or 'Condition'):
        super(TopFilter, self).__init__()
        self.top_filter = top_filter


class AndFilter(Filter):
    def __init__(self):
        super(AndFilter, self).__init__()

    def collect_query_fragments(self):
        return " AND ".join([cond.to_query_string() for cond in self.conditions])


class OrFilter(Filter):
    def __init__(self):
        super(OrFilter, self).__init__()

    def collect_query_fragments(self):
        return " OR ".join([cond.to_query_string() for cond in self.conditions])


class Condition:
    def __init__(self, name: str, value, operator: str, secondary_value=None, not_condition: bool = False):
        if operator.lower() in [">", ">=", "=", "<", "<=", "<>", "!=", "is", "is not"]:
            self.operator = operator
        elif secondary_value and operator.lower() == "between":
            self.operator = operator
            self.secondary_value = secondary_value
        else:
            raise Exception("Unsupported operator")

        if name is not None:
            self.name = name
        else:
            raise Exception("name can't be missing")
        if value is not None:
            self.value = value
        else:
            raise Exception("value can't be missing")
        self.not_condition = not_condition

    def to_query_string(self) -> str:
        res = ""
        if self.not_condition:
            res = "NOT "
        if self.operator.lower() != "between":
            return f"{res}{self.name} {self.operator} %s"
        if self.operator.lower() == "between" and self.secondary_value:
            return f"{res}{self.name} BETWEEN %s AND %s"
        raise Exception("Unsupported operator")

    def query_values(self) -> List:
        res = [self.value]
        if "secondary_value" in dir(self):
            res.append(self.secondary_value)
        return res

