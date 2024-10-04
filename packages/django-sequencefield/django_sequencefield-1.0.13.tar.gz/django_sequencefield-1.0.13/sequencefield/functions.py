from django.db.models import CharField, DateField
from django.db.models.expressions import Func


class NextSeqVal(Func):
    template = ""
    arity = 0

    def __init__(self, sequence="", output_field=None):
        template = f"nextval('{sequence}')"
        super().__init__(output_field=output_field, template=template)


class ToChar(Func):
    template = ""
    arity = 1

    def __init__(self, *expressions, format="", output_field=None):
        template = f"to_char(%(expressions)s, '{format}')"
        super().__init__(
            *expressions, output_field=output_field or CharField(), template=template
        )


class LeftShift(Func):
    template = ""
    arity = 1

    def __init__(self, *expressions, bits: int, output_field=None):
        template = f"(%(expressions)s::bigint << {bits})"
        super().__init__(*expressions, output_field=output_field, template=template)


class RightShift(Func):
    template = ""
    arity = 1

    def __init__(self, *expressions, bits: int, output_field=None):
        template = f"(%(expressions)s >> {bits})"
        super().__init__(*expressions, output_field=output_field, template=template)


class DateFromId(Func):
    arity = 1
    template = ""

    def __init__(self, *expressions, output_field=None):
        template = "(to_timestamp((%(expressions)s >> 48)*86400)::date)"
        super().__init__(*expressions, output_field=DateField(), template=template)
