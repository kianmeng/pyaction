from typing import Callable, Dict, get_type_hints

from pydantic import TypeAdapter

from pyaction import io
from pyaction.utils import check_parameters


class PyAction:
    @staticmethod
    def action(func: Callable):
        """action decorator

        Args:
            func (Callable): action function

        Examples:
            In the `main.py` file, use this decorator to define your action like this:

            >>> workflow = PyAction()
            >>> @workflow.action
            >>> def my_action(...): ...

            Define your action input parameters as the annotated action function arguments.

            >>> ...
            >>> def my_action(name: str, age: int): ...
        """

        check_parameters(func)

        def wrapper():
            params = {
                key: (type_, io.read(key))
                for key, type_ in get_type_hints(func).items()
                if key != "return"
            }

            retyped_params = {}

            for key, item in params.items():
                retyped_params[key] = TypeAdapter(item[0]).validate_python(item[1])

            return func(**retyped_params)

        return wrapper()

    @staticmethod
    def write(context: Dict[str, str]) -> None:
        """writes the `context` env var(s) into the streamline

        Args:
            context (Dict[str, str]): variables and values
        """

        io.write(context)  # pragma: no cover
