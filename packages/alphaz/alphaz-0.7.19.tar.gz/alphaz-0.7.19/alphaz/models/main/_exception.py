import re, traceback

EXCEPTIONS = {}


def get_message_from_name(name):
    if type(name) != str:
        name = str(name)
    name = name.replace("_", " ")
    return name[0].upper() + name[1:] if len(name) != 0 else name


class AlphaException(Exception):
    def __init__(
        self,
        name="exception",
        warning: bool = False,
        description=None,
        parameters: dict[str, object] = {},
        ex: Exception = None,
        traces_levels: int = 10,
    ):
        self.name = name if name is not None else "exception"
        self.warning = 1 if warning else 0
        if isinstance(name, Exception):
            self.name = "exception"

        if name in EXCEPTIONS:
            if not "text" in EXCEPTIONS[name]:
                raise AlphaException(
                    "wrong_exception_definition",
                    f"Wrong exception definition for {name}",
                )
            self.description = EXCEPTIONS[name]["text"]
        else:
            self.description = description or get_message_from_name(name)

        if ex is not None:
            self.description += f"\nex: {ex}"

        traces = traceback.format_stack()
        self.traces = [f"{tr}" for tr in traces[-(traces_levels + 1) : -1]]

        if len(parameters) != 0 and type(parameters) == dict:
            # parameters = re.findall(r'{[a-zA-Z_-]+',self.description)
            parameters_values = []
            for key, value in parameters.items():
                if "{%s" % key in self.description:
                    self.description = self.description.replace("{%s" % key, "{")
                    parameters_values.append(value)
            try:
                self.description = self.description.format(*parameters_values)
            except Exception as ex:
                raise AlphaException(
                    "wrong_exception_parameter",
                    "Wrong parameters for exception {name}",
                )

        super().__init__(self.description)
