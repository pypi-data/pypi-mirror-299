"""GearCompoundSteadyStateSynchronousResponse"""

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
    _3287,
)

_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "GearCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3134,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3212,
        _3219,
        _3222,
        _3223,
        _3224,
        _3233,
        _3237,
        _3240,
        _3255,
        _3258,
        _3261,
        _3270,
        _3274,
        _3277,
        _3280,
        _3289,
        _3309,
        _3315,
        _3318,
        _3321,
        _3322,
        _3333,
        _3336,
    )

    Self = TypeVar("Self", bound="GearCompoundSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearCompoundSteadyStateSynchronousResponse._Cast_GearCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearCompoundSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting GearCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: "GearCompoundSteadyStateSynchronousResponse"

    @property
    def mountable_component_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3287.MountableComponentCompoundSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3287.MountableComponentCompoundSteadyStateSynchronousResponse
        )

    @property
    def component_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3233.ComponentCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3233,
        )

        return self.__parent__._cast(
            _3233.ComponentCompoundSteadyStateSynchronousResponse
        )

    @property
    def part_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3289.PartCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3289,
        )

        return self.__parent__._cast(_3289.PartCompoundSteadyStateSynchronousResponse)

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
    def agma_gleason_conical_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3212.AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3212,
        )

        return self.__parent__._cast(
            _3212.AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3219.BevelDifferentialGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3219,
        )

        return self.__parent__._cast(
            _3219.BevelDifferentialGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_planet_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3222.BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3222,
        )

        return self.__parent__._cast(
            _3222.BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_sun_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3223.BevelDifferentialSunGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3223,
        )

        return self.__parent__._cast(
            _3223.BevelDifferentialSunGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3224.BevelGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3224,
        )

        return self.__parent__._cast(
            _3224.BevelGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def concept_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3237.ConceptGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3237,
        )

        return self.__parent__._cast(
            _3237.ConceptGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3240.ConicalGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3240,
        )

        return self.__parent__._cast(
            _3240.ConicalGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3255.CylindricalGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3255,
        )

        return self.__parent__._cast(
            _3255.CylindricalGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_planet_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3258.CylindricalPlanetGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3258,
        )

        return self.__parent__._cast(
            _3258.CylindricalPlanetGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def face_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3261.FaceGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3261,
        )

        return self.__parent__._cast(
            _3261.FaceGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def hypoid_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3270.HypoidGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3270,
        )

        return self.__parent__._cast(
            _3270.HypoidGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3274.KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3274,
        )

        return self.__parent__._cast(
            _3274.KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> (
        "_3277.KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponse"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3277,
        )

        return self.__parent__._cast(
            _3277.KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3280.KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3280,
        )

        return self.__parent__._cast(
            _3280.KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3309.SpiralBevelGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3309,
        )

        return self.__parent__._cast(
            _3309.SpiralBevelGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3315.StraightBevelDiffGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3315,
        )

        return self.__parent__._cast(
            _3315.StraightBevelDiffGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3318.StraightBevelGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3318,
        )

        return self.__parent__._cast(
            _3318.StraightBevelGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_planet_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3321.StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3321,
        )

        return self.__parent__._cast(
            _3321.StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_sun_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3322.StraightBevelSunGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3322,
        )

        return self.__parent__._cast(
            _3322.StraightBevelSunGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def worm_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3333.WormGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3333,
        )

        return self.__parent__._cast(
            _3333.WormGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def zerol_bevel_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3336.ZerolBevelGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3336,
        )

        return self.__parent__._cast(
            _3336.ZerolBevelGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "GearCompoundSteadyStateSynchronousResponse":
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
class GearCompoundSteadyStateSynchronousResponse(
    _3287.MountableComponentCompoundSteadyStateSynchronousResponse
):
    """GearCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_3134.GearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.GearSteadyStateSynchronousResponse]

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3134.GearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.GearSteadyStateSynchronousResponse]

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
    def cast_to(self: "Self") -> "_Cast_GearCompoundSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_GearCompoundSteadyStateSynchronousResponse
        """
        return _Cast_GearCompoundSteadyStateSynchronousResponse(self)
