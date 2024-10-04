"""ContourDrawStyle"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.geometry import _320

_CONTOUR_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "ContourDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6729,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6471,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5895,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5587
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4772
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4132
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3975,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3182,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2914,
    )
    from mastapy._private.system_model.drawing import _2307
    from mastapy._private.utility.enums import _1874
    from mastapy._private.utility_gui import _1904

    Self = TypeVar("Self", bound="ContourDrawStyle")
    CastSelf = TypeVar("CastSelf", bound="ContourDrawStyle._Cast_ContourDrawStyle")


__docformat__ = "restructuredtext en"
__all__ = ("ContourDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ContourDrawStyle:
    """Special nested class for casting ContourDrawStyle to subclasses."""

    __parent__: "ContourDrawStyle"

    @property
    def draw_style_base(self: "CastSelf") -> "_320.DrawStyleBase":
        return self.__parent__._cast(_320.DrawStyleBase)

    @property
    def system_deflection_draw_style(
        self: "CastSelf",
    ) -> "_2914.SystemDeflectionDrawStyle":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2914,
        )

        return self.__parent__._cast(_2914.SystemDeflectionDrawStyle)

    @property
    def steady_state_synchronous_response_draw_style(
        self: "CastSelf",
    ) -> "_3182.SteadyStateSynchronousResponseDrawStyle":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3182,
        )

        return self.__parent__._cast(_3182.SteadyStateSynchronousResponseDrawStyle)

    @property
    def stability_analysis_draw_style(
        self: "CastSelf",
    ) -> "_3975.StabilityAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3975,
        )

        return self.__parent__._cast(_3975.StabilityAnalysisDrawStyle)

    @property
    def rotor_dynamics_draw_style(self: "CastSelf") -> "_4132.RotorDynamicsDrawStyle":
        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4132,
        )

        return self.__parent__._cast(_4132.RotorDynamicsDrawStyle)

    @property
    def modal_analysis_draw_style(self: "CastSelf") -> "_4772.ModalAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4772,
        )

        return self.__parent__._cast(_4772.ModalAnalysisDrawStyle)

    @property
    def mbd_analysis_draw_style(self: "CastSelf") -> "_5587.MBDAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5587,
        )

        return self.__parent__._cast(_5587.MBDAnalysisDrawStyle)

    @property
    def harmonic_analysis_draw_style(
        self: "CastSelf",
    ) -> "_5895.HarmonicAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5895,
        )

        return self.__parent__._cast(_5895.HarmonicAnalysisDrawStyle)

    @property
    def dynamic_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6471.DynamicAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6471,
        )

        return self.__parent__._cast(_6471.DynamicAnalysisDrawStyle)

    @property
    def critical_speed_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6729.CriticalSpeedAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6729,
        )

        return self.__parent__._cast(_6729.CriticalSpeedAnalysisDrawStyle)

    @property
    def contour_draw_style(self: "CastSelf") -> "ContourDrawStyle":
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
class ContourDrawStyle(_320.DrawStyleBase):
    """ContourDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONTOUR_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def contour(self: "Self") -> "_1874.ThreeDViewContourOption":
        """mastapy.utility.enums.ThreeDViewContourOption"""
        temp = pythonnet_property_get(self.wrapped, "Contour")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Enums.ThreeDViewContourOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.enums._1874", "ThreeDViewContourOption"
        )(value)

    @contour.setter
    @enforce_parameter_types
    def contour(self: "Self", value: "_1874.ThreeDViewContourOption") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Enums.ThreeDViewContourOption"
        )
        pythonnet_property_set(self.wrapped, "Contour", value)

    @property
    def minimum_peak_value_displacement(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumPeakValueDisplacement")

        if temp is None:
            return 0.0

        return temp

    @minimum_peak_value_displacement.setter
    @enforce_parameter_types
    def minimum_peak_value_displacement(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumPeakValueDisplacement",
            float(value) if value is not None else 0.0,
        )

    @property
    def minimum_peak_value_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumPeakValueStress")

        if temp is None:
            return 0.0

        return temp

    @minimum_peak_value_stress.setter
    @enforce_parameter_types
    def minimum_peak_value_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumPeakValueStress",
            float(value) if value is not None else 0.0,
        )

    @property
    def show_local_maxima(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowLocalMaxima")

        if temp is None:
            return False

        return temp

    @show_local_maxima.setter
    @enforce_parameter_types
    def show_local_maxima(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowLocalMaxima", bool(value) if value is not None else False
        )

    @property
    def deflection_scaling(self: "Self") -> "_1904.ScalingDrawStyle":
        """mastapy.utility_gui.ScalingDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DeflectionScaling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def model_view_options(self: "Self") -> "_2307.ModelViewOptionsDrawStyle":
        """mastapy.system_model.drawing.ModelViewOptionsDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModelViewOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ContourDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_ContourDrawStyle
        """
        return _Cast_ContourDrawStyle(self)
