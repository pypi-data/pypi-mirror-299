from abc import ABC
import asyncio
from typing import Callable
from functools import wraps
from itertools import chain
import json


class CallableTool(ABC):
    """A (fake) interface for any tool that can be invoked by the assistant."""

    in_thread: bool  # whether to run the function in a separate thread
    include_call_id: bool  # whether to include the call_id in the function arguments

    def __call__(args: dict) -> str: ...


class Tools(ABC):
    """A (fake) interface for any tool (function/ToolList/Toolkit) that can be used by the assistant."""

    tool_enabled: bool  # whether this tool is enabled
    schema: list[dict]  # list of OpenAI function schemas
    lookup: dict[str, CallableTool]  # dict of tool name to function implementation
    lookup_preview: dict[str, CallableTool]  # dict of tool name to preview function


class ToolList(Tools):
    """A simple collection of tools/toolkits"""

    def __init__(self, *tools: Tools, tool_enabled=True):
        self.tools = list(tools)
        self.tool_enabled = tool_enabled

    @property
    def schema(self) -> list[dict]:
        """list of OpenAI function schemas"""
        if not self.tool_enabled:
            return []

        return list(chain(*[t.schema for t in self.tools if t.tool_enabled]))

    @property
    def lookup(self) -> dict[str, CallableTool]:
        """dict of TOOL NAME to argument-validated function"""
        if not self.tool_enabled:
            return {}

        lookups = [t.lookup for t in self.tools if t.tool_enabled]
        assert len(set(chain(*[lookup.keys() for lookup in lookups]))) == sum(
            [len(lookup) for lookup in lookups]
        ), "Duplicate tool names detected!"
        return {k: v for lookup in lookups for k, v in lookup.items()}

    @property
    def lookup_preview(self) -> dict[str, CallableTool]:
        """dict of TOOL NAME to argument-validated function"""
        if not self.tool_enabled:
            return {}

        lookups = [t.lookup_preview for t in self.tools if t.tool_enabled]
        return {k: v for lookup in lookups for k, v in lookup.items()}


class Toolkit(Tools):
    """
    A base class for a collection of tools and their shared states.
    Simply inherit this class and mark your methods as tools with the `@function_tool` decorator.
    After instantiating your toolkit, you can either:
    - [Code]: Simply use the functions as normal, e.g. `toolkit.my_tool(**args)`
    - [Model]: Use the `toolkit.lookup` dict to call the function by name, e.g. `toolkit.lookup['my_tool'](args)`
    """

    def __init__(self):
        self.tool_enabled = True
        self.registered_tools = {}  # explicitly registered, i.e. dynamically defined tools

    def register_tool(self, tool):
        """Explicitly register a tool if it's not in the class definition"""
        self.registered_tools[tool.name] = tool

    @property
    def schema(self) -> list[dict]:
        """list of OpenAI function schemas"""
        return list(chain(*[tool.schema for tool in self._function_tools.values()]))

    @property
    def lookup(self) -> dict[str, CallableTool]:
        """dict of TOOL NAME to argument-validated function"""
        return {
            tool.name: self._with_self(tool.validate_and_call)
            for tool in self._function_tools.values()
        }

    @property
    def lookup_preview(self) -> dict[str, CallableTool]:
        """dict of TOOL NAME to argument-validated function"""
        return {
            tool.name: self._with_self(tool.lookup_preview[tool.name])
            for tool in self._function_tools.values()
            if tool.name in tool.lookup_preview
        }

    @property
    def _function_tools(self) -> dict[str, Callable]:
        """dict of RAW FUNCTION NAME to function"""
        return (
            self.registered_tools
            | {
                attr: getattr(self, attr)
                for attr in dir(type(self))
                if not isinstance(
                    getattr(type(self), attr), property
                )  # ignore properties to prevent infinite recursion
                and getattr(getattr(self, attr), "tool_enabled", False)
            }
            if self.tool_enabled
            else {}
        )

    # util to prevent late-binding of func in a dict comprehension
    def _with_self(self, func: Callable):
        """Make a function which automatically receives self as the first argument"""

        @wraps(func)
        def wrapper(kwargs: dict[str, any]):
            return func({"self": self, **kwargs})

        return wrapper


# ========== Model ========== #
async def call_requested_function(
    func_name: str,
    json_args: str,
    func_lookup: dict[str, CallableTool],
    call_id: str | None = None,
):
    """
    Call the requested function generated by the model.
    """
    # parse function call
    if func_name not in func_lookup:
        return f"Error: Function {func_name} does not exist."
    try:
        args = json.loads(json_args)
    except Exception as e:
        return f"Error: Failed to parse arguments, make sure your arguments is a valid JSON object: {e}"

    # call function
    f = func_lookup[func_name]

    if f.include_call_id:
        args = args | {"call_id": call_id}

    if not f.in_thread:
        return await f(args)
    else:
        return await asyncio.to_thread(f, args)


async def call_function_preview(
    func_name: str,
    args: dict,
    func_lookup_preview: dict[str, CallableTool],
    call_id: str | None = None,
):
    """
    Call the requested function preview from the *autocompleted* JSON of the partial arguments while being generated by the model.
    """
    # call function
    try:
        f = func_lookup_preview[func_name]

        if f.include_call_id:
            args = args | {"call_id": call_id}

        if not f.in_thread:
            return await f(args)
        else:
            return await asyncio.to_thread(f, args)
    except Exception:
        pass
