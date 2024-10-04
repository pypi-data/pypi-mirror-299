"""CouplingConnectionParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4478,
)

_COUPLING_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "CouplingConnectionParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2739
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7709
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4427,
        _4432,
        _4441,
        _4506,
        _4528,
        _4543,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2401

    Self = TypeVar("Self", bound="CouplingConnectionParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionParametricStudyTool:
    """Special nested class for casting CouplingConnectionParametricStudyTool to subclasses."""

    __parent__: "CouplingConnectionParametricStudyTool"

    @property
    def inter_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4478.InterMountableComponentConnectionParametricStudyTool":
        return self.__parent__._cast(
            _4478.InterMountableComponentConnectionParametricStudyTool
        )

    @property
    def connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4441.ConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4441,
        )

        return self.__parent__._cast(_4441.ConnectionParametricStudyTool)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7709.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7709,
        )

        return self.__parent__._cast(_7709.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2735.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.ConnectionAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2739.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2739

        return self.__parent__._cast(_2739.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2737.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2737

        return self.__parent__._cast(_2737.DesignEntityAnalysis)

    @property
    def clutch_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4427.ClutchConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4427,
        )

        return self.__parent__._cast(_4427.ClutchConnectionParametricStudyTool)

    @property
    def concept_coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4432.ConceptCouplingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4432,
        )

        return self.__parent__._cast(_4432.ConceptCouplingConnectionParametricStudyTool)

    @property
    def part_to_part_shear_coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4506.PartToPartShearCouplingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4506,
        )

        return self.__parent__._cast(
            _4506.PartToPartShearCouplingConnectionParametricStudyTool
        )

    @property
    def spring_damper_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4528.SpringDamperConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4528,
        )

        return self.__parent__._cast(_4528.SpringDamperConnectionParametricStudyTool)

    @property
    def torque_converter_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4543.TorqueConverterConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4543,
        )

        return self.__parent__._cast(_4543.TorqueConverterConnectionParametricStudyTool)

    @property
    def coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "CouplingConnectionParametricStudyTool":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class CouplingConnectionParametricStudyTool(
    _4478.InterMountableComponentConnectionParametricStudyTool
):
    """CouplingConnectionParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2401.CouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.CouplingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionParametricStudyTool
        """
        return _Cast_CouplingConnectionParametricStudyTool(self)
