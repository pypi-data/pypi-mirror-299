"""PointLoadCompoundPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4399,
)

_POINT_LOAD_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "PointLoadCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4229
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4300,
        _4354,
        _4356,
    )
    from mastapy._private.system_model.part_model import _2529

    Self = TypeVar("Self", bound="PointLoadCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="PointLoadCompoundPowerFlow._Cast_PointLoadCompoundPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PointLoadCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PointLoadCompoundPowerFlow:
    """Special nested class for casting PointLoadCompoundPowerFlow to subclasses."""

    __parent__: "PointLoadCompoundPowerFlow"

    @property
    def virtual_component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4399.VirtualComponentCompoundPowerFlow":
        return self.__parent__._cast(_4399.VirtualComponentCompoundPowerFlow)

    @property
    def mountable_component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4354.MountableComponentCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4354,
        )

        return self.__parent__._cast(_4354.MountableComponentCompoundPowerFlow)

    @property
    def component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4300.ComponentCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4300,
        )

        return self.__parent__._cast(_4300.ComponentCompoundPowerFlow)

    @property
    def part_compound_power_flow(self: "CastSelf") -> "_4356.PartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4356,
        )

        return self.__parent__._cast(_4356.PartCompoundPowerFlow)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7717.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7714.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7714,
        )

        return self.__parent__._cast(_7714.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2737.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2737

        return self.__parent__._cast(_2737.DesignEntityAnalysis)

    @property
    def point_load_compound_power_flow(
        self: "CastSelf",
    ) -> "PointLoadCompoundPowerFlow":
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
class PointLoadCompoundPowerFlow(_4399.VirtualComponentCompoundPowerFlow):
    """PointLoadCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POINT_LOAD_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2529.PointLoad":
        """mastapy.system_model.part_model.PointLoad

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4229.PointLoadPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.PointLoadPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(self: "Self") -> "List[_4229.PointLoadPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.PointLoadPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PointLoadCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_PointLoadCompoundPowerFlow
        """
        return _Cast_PointLoadCompoundPowerFlow(self)
