"""ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3211,
)

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7714,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3173,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3232,
        _3243,
        _3252,
        _3293,
    )

    Self = TypeVar(
        "Self",
        bound="ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse._Cast_ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: (
        "ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse"
    )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3211.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3211.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3243.ConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3243,
        )

        return self.__parent__._cast(
            _3243.ConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7710.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConnectionCompoundAnalysis)

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
    def coaxial_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3232.CoaxialConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3232,
        )

        return self.__parent__._cast(
            _3232.CoaxialConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3252.CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3252,
        )

        return self.__parent__._cast(
            _3252.CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def planetary_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3293.PlanetaryConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3293,
        )

        return self.__parent__._cast(
            _3293.PlanetaryConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def shaft_to_mountable_component_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse":
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
class ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse(
    _3211.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse
):
    """ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> (
        "List[_3173.ShaftToMountableComponentConnectionSteadyStateSynchronousResponse]"
    ):
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.ShaftToMountableComponentConnectionSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> (
        "List[_3173.ShaftToMountableComponentConnectionSteadyStateSynchronousResponse]"
    ):
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.ShaftToMountableComponentConnectionSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse
        """
        return _Cast_ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse(
            self
        )
