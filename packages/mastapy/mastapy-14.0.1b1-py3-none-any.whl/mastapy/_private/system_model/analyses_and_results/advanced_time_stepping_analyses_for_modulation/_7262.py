"""ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7160,
)

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2739
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7186,
        _7197,
        _7207,
        _7248,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7709,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2893,
    )
    from mastapy._private.system_model.connections_and_sockets import _2350

    Self = TypeVar(
        "Self",
        bound="ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation._Cast_ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = (
    "ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation",
)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: (
        "ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation"
    )

    @property
    def abstract_shaft_to_mountable_component_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7160.AbstractShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7160.AbstractShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7197.ConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7197,
        )

        return self.__parent__._cast(
            _7197.ConnectionAdvancedTimeSteppingAnalysisForModulation
        )

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
    def coaxial_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7186.CoaxialConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7186,
        )

        return self.__parent__._cast(
            _7186.CoaxialConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_central_bearing_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7207.CycloidalDiscCentralBearingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7207,
        )

        return self.__parent__._cast(
            _7207.CycloidalDiscCentralBearingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planetary_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7248.PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7248,
        )

        return self.__parent__._cast(
            _7248.PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_to_mountable_component_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation":
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
class ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation(
    _7160.AbstractShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation
):
    """ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2350.ShaftToMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2893.ShaftToMountableComponentConnectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftToMountableComponentConnectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation(
            self
        )
