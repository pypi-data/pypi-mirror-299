"""VirtualComponentSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3153,
)

_VIRTUAL_COMPONENT_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "VirtualComponentSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737, _2739, _2743
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7716,
        _7719,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3098,
        _3149,
        _3150,
        _3155,
        _3162,
        _3163,
        _3200,
    )
    from mastapy._private.system_model.part_model import _2538

    Self = TypeVar("Self", bound="VirtualComponentSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentSteadyStateSynchronousResponse._Cast_VirtualComponentSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentSteadyStateSynchronousResponse:
    """Special nested class for casting VirtualComponentSteadyStateSynchronousResponse to subclasses."""

    __parent__: "VirtualComponentSteadyStateSynchronousResponse"

    @property
    def mountable_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3153.MountableComponentSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3153.MountableComponentSteadyStateSynchronousResponse
        )

    @property
    def component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3098.ComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3098,
        )

        return self.__parent__._cast(_3098.ComponentSteadyStateSynchronousResponse)

    @property
    def part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3155.PartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3155,
        )

        return self.__parent__._cast(_3155.PartSteadyStateSynchronousResponse)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7719.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7716.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7716,
        )

        return self.__parent__._cast(_7716.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2743.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2743

        return self.__parent__._cast(_2743.PartAnalysis)

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
    def mass_disc_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3149.MassDiscSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3149,
        )

        return self.__parent__._cast(_3149.MassDiscSteadyStateSynchronousResponse)

    @property
    def measurement_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3150.MeasurementComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3150,
        )

        return self.__parent__._cast(
            _3150.MeasurementComponentSteadyStateSynchronousResponse
        )

    @property
    def point_load_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3162.PointLoadSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3162,
        )

        return self.__parent__._cast(_3162.PointLoadSteadyStateSynchronousResponse)

    @property
    def power_load_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3163.PowerLoadSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3163,
        )

        return self.__parent__._cast(_3163.PowerLoadSteadyStateSynchronousResponse)

    @property
    def unbalanced_mass_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3200.UnbalancedMassSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3200,
        )

        return self.__parent__._cast(_3200.UnbalancedMassSteadyStateSynchronousResponse)

    @property
    def virtual_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "VirtualComponentSteadyStateSynchronousResponse":
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
class VirtualComponentSteadyStateSynchronousResponse(
    _3153.MountableComponentSteadyStateSynchronousResponse
):
    """VirtualComponentSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2538.VirtualComponent":
        """mastapy.system_model.part_model.VirtualComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualComponentSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentSteadyStateSynchronousResponse
        """
        return _Cast_VirtualComponentSteadyStateSynchronousResponse(self)
