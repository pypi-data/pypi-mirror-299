"""WormGearMeshPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4199

_WORM_GEAR_MESH_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "WormGearMeshPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.worm import _386
    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2739
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7709,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4173,
        _4206,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7135
    from mastapy._private.system_model.connections_and_sockets.gears import _2384

    Self = TypeVar("Self", bound="WormGearMeshPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="WormGearMeshPowerFlow._Cast_WormGearMeshPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGearMeshPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearMeshPowerFlow:
    """Special nested class for casting WormGearMeshPowerFlow to subclasses."""

    __parent__: "WormGearMeshPowerFlow"

    @property
    def gear_mesh_power_flow(self: "CastSelf") -> "_4199.GearMeshPowerFlow":
        return self.__parent__._cast(_4199.GearMeshPowerFlow)

    @property
    def inter_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4206.InterMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4206

        return self.__parent__._cast(_4206.InterMountableComponentConnectionPowerFlow)

    @property
    def connection_power_flow(self: "CastSelf") -> "_4173.ConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4173

        return self.__parent__._cast(_4173.ConnectionPowerFlow)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7712.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConnectionStaticLoadAnalysisCase)

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
    def worm_gear_mesh_power_flow(self: "CastSelf") -> "WormGearMeshPowerFlow":
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
class WormGearMeshPowerFlow(_4199.GearMeshPowerFlow):
    """WormGearMeshPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_MESH_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rating(self: "Self") -> "_386.WormGearMeshRating":
        """mastapy.gears.rating.worm.WormGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_detailed_analysis(self: "Self") -> "_386.WormGearMeshRating":
        """mastapy.gears.rating.worm.WormGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2384.WormGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.WormGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_7135.WormGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearMeshPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_WormGearMeshPowerFlow
        """
        return _Cast_WormGearMeshPowerFlow(self)
