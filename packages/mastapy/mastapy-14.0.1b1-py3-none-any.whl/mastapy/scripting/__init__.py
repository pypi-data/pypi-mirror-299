"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.scripting._7733 import ApiEnumForAttribute
    from mastapy._private.scripting._7734 import ApiVersion
    from mastapy._private.scripting._7735 import SMTBitmap
    from mastapy._private.scripting._7737 import MastaPropertyAttribute
    from mastapy._private.scripting._7738 import PythonCommand
    from mastapy._private.scripting._7739 import ScriptingCommand
    from mastapy._private.scripting._7740 import ScriptingExecutionCommand
    from mastapy._private.scripting._7741 import ScriptingObjectCommand
    from mastapy._private.scripting._7742 import ApiVersioning
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.scripting._7733": ["ApiEnumForAttribute"],
        "_private.scripting._7734": ["ApiVersion"],
        "_private.scripting._7735": ["SMTBitmap"],
        "_private.scripting._7737": ["MastaPropertyAttribute"],
        "_private.scripting._7738": ["PythonCommand"],
        "_private.scripting._7739": ["ScriptingCommand"],
        "_private.scripting._7740": ["ScriptingExecutionCommand"],
        "_private.scripting._7741": ["ScriptingObjectCommand"],
        "_private.scripting._7742": ["ApiVersioning"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ApiEnumForAttribute",
    "ApiVersion",
    "SMTBitmap",
    "MastaPropertyAttribute",
    "PythonCommand",
    "ScriptingCommand",
    "ScriptingExecutionCommand",
    "ScriptingObjectCommand",
    "ApiVersioning",
)
