"""ComponentCompoundSteadyStateSynchronousResponse"""

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
    _3289,
)

_COMPONENT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "ComponentCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3098,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3209,
        _3210,
        _3212,
        _3216,
        _3219,
        _3222,
        _3223,
        _3224,
        _3227,
        _3231,
        _3236,
        _3237,
        _3240,
        _3244,
        _3247,
        _3250,
        _3253,
        _3255,
        _3258,
        _3259,
        _3260,
        _3261,
        _3264,
        _3266,
        _3269,
        _3270,
        _3274,
        _3277,
        _3280,
        _3283,
        _3284,
        _3286,
        _3287,
        _3288,
        _3292,
        _3295,
        _3296,
        _3297,
        _3298,
        _3299,
        _3302,
        _3305,
        _3306,
        _3309,
        _3314,
        _3315,
        _3318,
        _3321,
        _3322,
        _3324,
        _3325,
        _3326,
        _3329,
        _3330,
        _3331,
        _3332,
        _3333,
        _3336,
    )

    Self = TypeVar("Self", bound="ComponentCompoundSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentCompoundSteadyStateSynchronousResponse._Cast_ComponentCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentCompoundSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting ComponentCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: "ComponentCompoundSteadyStateSynchronousResponse"

    @property
    def part_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3289.PartCompoundSteadyStateSynchronousResponse":
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
    def abstract_shaft_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3209.AbstractShaftCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3209,
        )

        return self.__parent__._cast(
            _3209.AbstractShaftCompoundSteadyStateSynchronousResponse
        )

    @property
    def abstract_shaft_or_housing_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3210.AbstractShaftOrHousingCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3210,
        )

        return self.__parent__._cast(
            _3210.AbstractShaftOrHousingCompoundSteadyStateSynchronousResponse
        )

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
    def bearing_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3216.BearingCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3216,
        )

        return self.__parent__._cast(
            _3216.BearingCompoundSteadyStateSynchronousResponse
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
    def bolt_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3227.BoltCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3227,
        )

        return self.__parent__._cast(_3227.BoltCompoundSteadyStateSynchronousResponse)

    @property
    def clutch_half_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3231.ClutchHalfCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3231,
        )

        return self.__parent__._cast(
            _3231.ClutchHalfCompoundSteadyStateSynchronousResponse
        )

    @property
    def concept_coupling_half_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3236.ConceptCouplingHalfCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3236,
        )

        return self.__parent__._cast(
            _3236.ConceptCouplingHalfCompoundSteadyStateSynchronousResponse
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
    def connector_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3244.ConnectorCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3244,
        )

        return self.__parent__._cast(
            _3244.ConnectorCompoundSteadyStateSynchronousResponse
        )

    @property
    def coupling_half_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3247.CouplingHalfCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3247,
        )

        return self.__parent__._cast(
            _3247.CouplingHalfCompoundSteadyStateSynchronousResponse
        )

    @property
    def cvt_pulley_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3250.CVTPulleyCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3250,
        )

        return self.__parent__._cast(
            _3250.CVTPulleyCompoundSteadyStateSynchronousResponse
        )

    @property
    def cycloidal_disc_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3253.CycloidalDiscCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3253,
        )

        return self.__parent__._cast(
            _3253.CycloidalDiscCompoundSteadyStateSynchronousResponse
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
    def datum_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3259.DatumCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3259,
        )

        return self.__parent__._cast(_3259.DatumCompoundSteadyStateSynchronousResponse)

    @property
    def external_cad_model_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3260.ExternalCADModelCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3260,
        )

        return self.__parent__._cast(
            _3260.ExternalCADModelCompoundSteadyStateSynchronousResponse
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
    def fe_part_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3264.FEPartCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3264,
        )

        return self.__parent__._cast(_3264.FEPartCompoundSteadyStateSynchronousResponse)

    @property
    def gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3266.GearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3266,
        )

        return self.__parent__._cast(_3266.GearCompoundSteadyStateSynchronousResponse)

    @property
    def guide_dxf_model_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3269.GuideDxfModelCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3269,
        )

        return self.__parent__._cast(
            _3269.GuideDxfModelCompoundSteadyStateSynchronousResponse
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
    def mass_disc_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3283.MassDiscCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3283,
        )

        return self.__parent__._cast(
            _3283.MassDiscCompoundSteadyStateSynchronousResponse
        )

    @property
    def measurement_component_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3284.MeasurementComponentCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3284,
        )

        return self.__parent__._cast(
            _3284.MeasurementComponentCompoundSteadyStateSynchronousResponse
        )

    @property
    def microphone_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3286.MicrophoneCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3286,
        )

        return self.__parent__._cast(
            _3286.MicrophoneCompoundSteadyStateSynchronousResponse
        )

    @property
    def mountable_component_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3287.MountableComponentCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3287,
        )

        return self.__parent__._cast(
            _3287.MountableComponentCompoundSteadyStateSynchronousResponse
        )

    @property
    def oil_seal_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3288.OilSealCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3288,
        )

        return self.__parent__._cast(
            _3288.OilSealCompoundSteadyStateSynchronousResponse
        )

    @property
    def part_to_part_shear_coupling_half_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3292.PartToPartShearCouplingHalfCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3292,
        )

        return self.__parent__._cast(
            _3292.PartToPartShearCouplingHalfCompoundSteadyStateSynchronousResponse
        )

    @property
    def planet_carrier_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3295.PlanetCarrierCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3295,
        )

        return self.__parent__._cast(
            _3295.PlanetCarrierCompoundSteadyStateSynchronousResponse
        )

    @property
    def point_load_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3296.PointLoadCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3296,
        )

        return self.__parent__._cast(
            _3296.PointLoadCompoundSteadyStateSynchronousResponse
        )

    @property
    def power_load_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3297.PowerLoadCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3297,
        )

        return self.__parent__._cast(
            _3297.PowerLoadCompoundSteadyStateSynchronousResponse
        )

    @property
    def pulley_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3298.PulleyCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3298,
        )

        return self.__parent__._cast(_3298.PulleyCompoundSteadyStateSynchronousResponse)

    @property
    def ring_pins_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3299.RingPinsCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3299,
        )

        return self.__parent__._cast(
            _3299.RingPinsCompoundSteadyStateSynchronousResponse
        )

    @property
    def rolling_ring_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3302.RollingRingCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3302,
        )

        return self.__parent__._cast(
            _3302.RollingRingCompoundSteadyStateSynchronousResponse
        )

    @property
    def shaft_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3305.ShaftCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3305,
        )

        return self.__parent__._cast(_3305.ShaftCompoundSteadyStateSynchronousResponse)

    @property
    def shaft_hub_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3306.ShaftHubConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3306,
        )

        return self.__parent__._cast(
            _3306.ShaftHubConnectionCompoundSteadyStateSynchronousResponse
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
    def spring_damper_half_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3314.SpringDamperHalfCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3314,
        )

        return self.__parent__._cast(
            _3314.SpringDamperHalfCompoundSteadyStateSynchronousResponse
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
    def synchroniser_half_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3324.SynchroniserHalfCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3324,
        )

        return self.__parent__._cast(
            _3324.SynchroniserHalfCompoundSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_part_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3325.SynchroniserPartCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3325,
        )

        return self.__parent__._cast(
            _3325.SynchroniserPartCompoundSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_sleeve_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3326.SynchroniserSleeveCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3326,
        )

        return self.__parent__._cast(
            _3326.SynchroniserSleeveCompoundSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_pump_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3329.TorqueConverterPumpCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3329,
        )

        return self.__parent__._cast(
            _3329.TorqueConverterPumpCompoundSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_turbine_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3330.TorqueConverterTurbineCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3330,
        )

        return self.__parent__._cast(
            _3330.TorqueConverterTurbineCompoundSteadyStateSynchronousResponse
        )

    @property
    def unbalanced_mass_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3331.UnbalancedMassCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3331,
        )

        return self.__parent__._cast(
            _3331.UnbalancedMassCompoundSteadyStateSynchronousResponse
        )

    @property
    def virtual_component_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3332.VirtualComponentCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3332,
        )

        return self.__parent__._cast(
            _3332.VirtualComponentCompoundSteadyStateSynchronousResponse
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
    def component_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "ComponentCompoundSteadyStateSynchronousResponse":
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
class ComponentCompoundSteadyStateSynchronousResponse(
    _3289.PartCompoundSteadyStateSynchronousResponse
):
    """ComponentCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_3098.ComponentSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.ComponentSteadyStateSynchronousResponse]

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
    ) -> "List[_3098.ComponentSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.ComponentSteadyStateSynchronousResponse]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_ComponentCompoundSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_ComponentCompoundSteadyStateSynchronousResponse
        """
        return _Cast_ComponentCompoundSteadyStateSynchronousResponse(self)
