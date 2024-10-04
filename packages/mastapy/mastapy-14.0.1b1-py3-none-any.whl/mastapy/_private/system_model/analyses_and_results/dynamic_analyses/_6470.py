"""DynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7715

_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses", "DynamicAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7706,
        _7721,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5865,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4739
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5027,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3918,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3125,
    )

    Self = TypeVar("Self", bound="DynamicAnalysis")
    CastSelf = TypeVar("CastSelf", bound="DynamicAnalysis._Cast_DynamicAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("DynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicAnalysis:
    """Special nested class for casting DynamicAnalysis to subclasses."""

    __parent__: "DynamicAnalysis"

    @property
    def fe_analysis(self: "CastSelf") -> "_7715.FEAnalysis":
        return self.__parent__._cast(_7715.FEAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7721.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7721,
        )

        return self.__parent__._cast(_7721.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7706.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7706,
        )

        return self.__parent__._cast(_7706.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2736.Context":
        from mastapy._private.system_model.analyses_and_results import _2736

        return self.__parent__._cast(_2736.Context)

    @property
    def dynamic_model_for_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3125.DynamicModelForSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3125,
        )

        return self.__parent__._cast(
            _3125.DynamicModelForSteadyStateSynchronousResponse
        )

    @property
    def dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "_3918.DynamicModelForStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3918,
        )

        return self.__parent__._cast(_3918.DynamicModelForStabilityAnalysis)

    @property
    def dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "_4739.DynamicModelForModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4739,
        )

        return self.__parent__._cast(_4739.DynamicModelForModalAnalysis)

    @property
    def dynamic_model_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5027.DynamicModelAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5027,
        )

        return self.__parent__._cast(_5027.DynamicModelAtAStiffness)

    @property
    def dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5865.DynamicModelForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5865,
        )

        return self.__parent__._cast(_5865.DynamicModelForHarmonicAnalysis)

    @property
    def dynamic_analysis(self: "CastSelf") -> "DynamicAnalysis":
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
class DynamicAnalysis(_7715.FEAnalysis):
    """DynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_DynamicAnalysis
        """
        return _Cast_DynamicAnalysis(self)
