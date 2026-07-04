from importlib import import_module
import re


def _validate_identifier(name: str, *, allow_dotted: bool = False) -> None:
    """Validate that `name` is a safe Python identifier.

    Args:
        name: The name to validate.
        allow_dotted: Whether dotted names (``a.b.c``) are permitted.

    Raises:
        ValueError: If the name contains unsafe characters.
    """
    if allow_dotted:
        parts = name.split(".")
        if not parts or not all(parts):
            msg = f"invalid module name {name!r}"
            raise ValueError(msg)
        for part in parts:
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part):
                msg = f"invalid module name {name!r}"
                raise ValueError(msg)
    else:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            msg = f"invalid attribute name {name!r}"
            raise ValueError(msg)


def import_attr(
    attr_name: str,
    module_name: str | None,
    package: str | None,
) -> object:
    """Import an attribute from a module located in a package.

    This utility function is used in custom `__getattr__` methods within `__init__.py`
    files to dynamically import attributes.

    Args:
        attr_name: The name of the attribute to import.
        module_name: The name of the module to import from.

            If `None`, the attribute is imported from the package itself.
        package: The name of the package where the module is located.

    Raises:
        ImportError: If the module cannot be found.
        AttributeError: If the attribute does not exist in the module or package.

    Returns:
        The imported attribute.
    """
    if module_name == "__module__" or module_name is None:
        _validate_identifier(attr_name)
        try:
            result = import_module(f".{attr_name}", package=package)
        except ModuleNotFoundError:
            msg = f"module '{package!r}' has no attribute {attr_name!r}"
            raise AttributeError(msg) from None
    else:
        _validate_identifier(module_name, allow_dotted=True)
        try:
            module = import_module(f".{module_name}", package=package)
        except ModuleNotFoundError as err:
            msg = f"module '{package!r}.{module_name!r}' not found ({err})"
            raise ImportError(msg) from None
        result = getattr(module, attr_name)
    return result
