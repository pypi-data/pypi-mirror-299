"""ConnectionCompoundAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714

_CONNECTION_COMPOUND_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases",
    "ConnectionCompoundAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7566,
        _7568,
        _7572,
        _7575,
        _7580,
        _7585,
        _7587,
        _7590,
        _7593,
        _7596,
        _7598,
        _7601,
        _7603,
        _7607,
        _7609,
        _7611,
        _7617,
        _7622,
        _7626,
        _7628,
        _7630,
        _7633,
        _7636,
        _7646,
        _7648,
        _7655,
        _7658,
        _7662,
        _7665,
        _7668,
        _7671,
        _7674,
        _7683,
        _7689,
        _7692,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
        _7297,
        _7299,
        _7303,
        _7306,
        _7311,
        _7316,
        _7318,
        _7321,
        _7324,
        _7327,
        _7329,
        _7332,
        _7334,
        _7338,
        _7340,
        _7342,
        _7348,
        _7353,
        _7357,
        _7359,
        _7361,
        _7364,
        _7367,
        _7377,
        _7379,
        _7386,
        _7389,
        _7393,
        _7396,
        _7399,
        _7402,
        _7405,
        _7414,
        _7420,
        _7423,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6825,
        _6827,
        _6831,
        _6834,
        _6839,
        _6844,
        _6846,
        _6849,
        _6852,
        _6855,
        _6857,
        _6860,
        _6862,
        _6866,
        _6868,
        _6870,
        _6876,
        _6881,
        _6885,
        _6887,
        _6889,
        _6892,
        _6895,
        _6905,
        _6907,
        _6914,
        _6917,
        _6921,
        _6924,
        _6927,
        _6930,
        _6933,
        _6942,
        _6948,
        _6951,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6554,
        _6556,
        _6560,
        _6563,
        _6568,
        _6573,
        _6575,
        _6578,
        _6581,
        _6584,
        _6586,
        _6589,
        _6591,
        _6595,
        _6597,
        _6599,
        _6605,
        _6610,
        _6614,
        _6616,
        _6618,
        _6621,
        _6624,
        _6634,
        _6636,
        _6643,
        _6646,
        _6650,
        _6653,
        _6656,
        _6659,
        _6662,
        _6671,
        _6677,
        _6680,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6017,
        _6019,
        _6023,
        _6026,
        _6031,
        _6036,
        _6038,
        _6041,
        _6044,
        _6047,
        _6049,
        _6052,
        _6054,
        _6058,
        _6060,
        _6062,
        _6068,
        _6073,
        _6077,
        _6079,
        _6081,
        _6084,
        _6087,
        _6097,
        _6099,
        _6106,
        _6109,
        _6113,
        _6116,
        _6119,
        _6122,
        _6125,
        _6134,
        _6140,
        _6143,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
        _6281,
        _6283,
        _6287,
        _6290,
        _6295,
        _6300,
        _6302,
        _6305,
        _6308,
        _6311,
        _6313,
        _6316,
        _6318,
        _6322,
        _6324,
        _6326,
        _6332,
        _6337,
        _6341,
        _6343,
        _6345,
        _6348,
        _6351,
        _6361,
        _6363,
        _6370,
        _6373,
        _6377,
        _6380,
        _6383,
        _6386,
        _6389,
        _6398,
        _6404,
        _6407,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5663,
        _5665,
        _5669,
        _5672,
        _5677,
        _5682,
        _5684,
        _5687,
        _5690,
        _5693,
        _5695,
        _5698,
        _5700,
        _5704,
        _5706,
        _5708,
        _5714,
        _5719,
        _5723,
        _5725,
        _5727,
        _5730,
        _5733,
        _5743,
        _5745,
        _5752,
        _5755,
        _5759,
        _5762,
        _5765,
        _5768,
        _5771,
        _5780,
        _5786,
        _5789,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4847,
        _4849,
        _4853,
        _4856,
        _4861,
        _4866,
        _4868,
        _4871,
        _4874,
        _4877,
        _4879,
        _4882,
        _4884,
        _4888,
        _4890,
        _4892,
        _4898,
        _4903,
        _4907,
        _4909,
        _4911,
        _4914,
        _4917,
        _4927,
        _4929,
        _4936,
        _4939,
        _4943,
        _4946,
        _4949,
        _4952,
        _4955,
        _4964,
        _4970,
        _4973,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5374,
        _5376,
        _5380,
        _5383,
        _5388,
        _5393,
        _5395,
        _5398,
        _5401,
        _5404,
        _5406,
        _5409,
        _5411,
        _5415,
        _5417,
        _5419,
        _5425,
        _5430,
        _5434,
        _5436,
        _5438,
        _5441,
        _5444,
        _5454,
        _5456,
        _5463,
        _5466,
        _5470,
        _5473,
        _5476,
        _5479,
        _5482,
        _5491,
        _5497,
        _5500,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5111,
        _5113,
        _5117,
        _5120,
        _5125,
        _5130,
        _5132,
        _5135,
        _5138,
        _5141,
        _5143,
        _5146,
        _5148,
        _5152,
        _5154,
        _5156,
        _5162,
        _5167,
        _5171,
        _5173,
        _5175,
        _5178,
        _5181,
        _5191,
        _5193,
        _5200,
        _5203,
        _5207,
        _5210,
        _5213,
        _5216,
        _5219,
        _5228,
        _5234,
        _5237,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4558,
        _4560,
        _4564,
        _4567,
        _4572,
        _4577,
        _4579,
        _4582,
        _4585,
        _4588,
        _4590,
        _4593,
        _4595,
        _4599,
        _4601,
        _4603,
        _4609,
        _4614,
        _4618,
        _4620,
        _4622,
        _4625,
        _4628,
        _4638,
        _4640,
        _4647,
        _4650,
        _4654,
        _4657,
        _4660,
        _4663,
        _4666,
        _4675,
        _4681,
        _4684,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4278,
        _4280,
        _4284,
        _4287,
        _4292,
        _4297,
        _4299,
        _4302,
        _4305,
        _4308,
        _4310,
        _4313,
        _4315,
        _4319,
        _4321,
        _4323,
        _4329,
        _4334,
        _4338,
        _4340,
        _4342,
        _4345,
        _4348,
        _4358,
        _4360,
        _4367,
        _4370,
        _4374,
        _4377,
        _4380,
        _4383,
        _4386,
        _4395,
        _4401,
        _4404,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4004,
        _4006,
        _4010,
        _4013,
        _4018,
        _4023,
        _4025,
        _4028,
        _4031,
        _4034,
        _4036,
        _4039,
        _4041,
        _4045,
        _4047,
        _4049,
        _4055,
        _4060,
        _4064,
        _4066,
        _4068,
        _4071,
        _4074,
        _4084,
        _4086,
        _4093,
        _4096,
        _4100,
        _4103,
        _4106,
        _4109,
        _4112,
        _4121,
        _4127,
        _4130,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3211,
        _3213,
        _3217,
        _3220,
        _3225,
        _3230,
        _3232,
        _3235,
        _3238,
        _3241,
        _3243,
        _3246,
        _3248,
        _3252,
        _3254,
        _3256,
        _3262,
        _3267,
        _3271,
        _3273,
        _3275,
        _3278,
        _3281,
        _3291,
        _3293,
        _3300,
        _3303,
        _3307,
        _3310,
        _3313,
        _3316,
        _3319,
        _3328,
        _3334,
        _3337,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
        _3737,
        _3739,
        _3743,
        _3746,
        _3751,
        _3756,
        _3758,
        _3761,
        _3764,
        _3767,
        _3769,
        _3772,
        _3774,
        _3778,
        _3780,
        _3782,
        _3788,
        _3793,
        _3797,
        _3799,
        _3801,
        _3804,
        _3807,
        _3817,
        _3819,
        _3826,
        _3829,
        _3833,
        _3836,
        _3839,
        _3842,
        _3845,
        _3854,
        _3860,
        _3863,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
        _3474,
        _3476,
        _3480,
        _3483,
        _3488,
        _3493,
        _3495,
        _3498,
        _3501,
        _3504,
        _3506,
        _3509,
        _3511,
        _3515,
        _3517,
        _3519,
        _3525,
        _3530,
        _3534,
        _3536,
        _3538,
        _3541,
        _3544,
        _3554,
        _3556,
        _3563,
        _3566,
        _3570,
        _3573,
        _3576,
        _3579,
        _3582,
        _3591,
        _3597,
        _3600,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2942,
        _2944,
        _2948,
        _2951,
        _2956,
        _2961,
        _2963,
        _2966,
        _2969,
        _2972,
        _2974,
        _2977,
        _2979,
        _2983,
        _2985,
        _2987,
        _2994,
        _2999,
        _3003,
        _3005,
        _3007,
        _3010,
        _3013,
        _3023,
        _3025,
        _3032,
        _3035,
        _3040,
        _3043,
        _3046,
        _3049,
        _3052,
        _3061,
        _3067,
        _3070,
    )

    Self = TypeVar("Self", bound="ConnectionCompoundAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ConnectionCompoundAnalysis._Cast_ConnectionCompoundAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCompoundAnalysis:
    """Special nested class for casting ConnectionCompoundAnalysis to subclasses."""

    __parent__: "ConnectionCompoundAnalysis"

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7714.DesignEntityCompoundAnalysis":
        return self.__parent__._cast(_7714.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2737.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2737

        return self.__parent__._cast(_2737.DesignEntityAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2942.AbstractShaftToMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2942,
        )

        return self.__parent__._cast(
            _2942.AbstractShaftToMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2944.AGMAGleasonConicalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2944,
        )

        return self.__parent__._cast(
            _2944.AGMAGleasonConicalGearMeshCompoundSystemDeflection
        )

    @property
    def belt_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2948.BeltConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2948,
        )

        return self.__parent__._cast(_2948.BeltConnectionCompoundSystemDeflection)

    @property
    def bevel_differential_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2951.BevelDifferentialGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2951,
        )

        return self.__parent__._cast(
            _2951.BevelDifferentialGearMeshCompoundSystemDeflection
        )

    @property
    def bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2956.BevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2956,
        )

        return self.__parent__._cast(_2956.BevelGearMeshCompoundSystemDeflection)

    @property
    def clutch_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2961.ClutchConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2961,
        )

        return self.__parent__._cast(_2961.ClutchConnectionCompoundSystemDeflection)

    @property
    def coaxial_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2963.CoaxialConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2963,
        )

        return self.__parent__._cast(_2963.CoaxialConnectionCompoundSystemDeflection)

    @property
    def concept_coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2966.ConceptCouplingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2966,
        )

        return self.__parent__._cast(
            _2966.ConceptCouplingConnectionCompoundSystemDeflection
        )

    @property
    def concept_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2969.ConceptGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2969,
        )

        return self.__parent__._cast(_2969.ConceptGearMeshCompoundSystemDeflection)

    @property
    def conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2972.ConicalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2972,
        )

        return self.__parent__._cast(_2972.ConicalGearMeshCompoundSystemDeflection)

    @property
    def connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2974.ConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2974,
        )

        return self.__parent__._cast(_2974.ConnectionCompoundSystemDeflection)

    @property
    def coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2977.CouplingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2977,
        )

        return self.__parent__._cast(_2977.CouplingConnectionCompoundSystemDeflection)

    @property
    def cvt_belt_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2979.CVTBeltConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2979,
        )

        return self.__parent__._cast(_2979.CVTBeltConnectionCompoundSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2983.CycloidalDiscCentralBearingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2983,
        )

        return self.__parent__._cast(
            _2983.CycloidalDiscCentralBearingConnectionCompoundSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2985.CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2985,
        )

        return self.__parent__._cast(
            _2985.CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection
        )

    @property
    def cylindrical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2987.CylindricalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2987,
        )

        return self.__parent__._cast(_2987.CylindricalGearMeshCompoundSystemDeflection)

    @property
    def face_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2994.FaceGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2994,
        )

        return self.__parent__._cast(_2994.FaceGearMeshCompoundSystemDeflection)

    @property
    def gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2999.GearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2999,
        )

        return self.__parent__._cast(_2999.GearMeshCompoundSystemDeflection)

    @property
    def hypoid_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3003.HypoidGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3003,
        )

        return self.__parent__._cast(_3003.HypoidGearMeshCompoundSystemDeflection)

    @property
    def inter_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3005.InterMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3005,
        )

        return self.__parent__._cast(
            _3005.InterMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3007.KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3007,
        )

        return self.__parent__._cast(
            _3007.KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3010.KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3010,
        )

        return self.__parent__._cast(
            _3010.KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3013.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3013,
        )

        return self.__parent__._cast(
            _3013.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3023.PartToPartShearCouplingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3023,
        )

        return self.__parent__._cast(
            _3023.PartToPartShearCouplingConnectionCompoundSystemDeflection
        )

    @property
    def planetary_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3025.PlanetaryConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3025,
        )

        return self.__parent__._cast(_3025.PlanetaryConnectionCompoundSystemDeflection)

    @property
    def ring_pins_to_disc_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3032.RingPinsToDiscConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3032,
        )

        return self.__parent__._cast(
            _3032.RingPinsToDiscConnectionCompoundSystemDeflection
        )

    @property
    def rolling_ring_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3035.RollingRingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3035,
        )

        return self.__parent__._cast(
            _3035.RollingRingConnectionCompoundSystemDeflection
        )

    @property
    def shaft_to_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3040.ShaftToMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3040,
        )

        return self.__parent__._cast(
            _3040.ShaftToMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3043.SpiralBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3043,
        )

        return self.__parent__._cast(_3043.SpiralBevelGearMeshCompoundSystemDeflection)

    @property
    def spring_damper_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3046.SpringDamperConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3046,
        )

        return self.__parent__._cast(
            _3046.SpringDamperConnectionCompoundSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3049.StraightBevelDiffGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3049,
        )

        return self.__parent__._cast(
            _3049.StraightBevelDiffGearMeshCompoundSystemDeflection
        )

    @property
    def straight_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3052.StraightBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3052,
        )

        return self.__parent__._cast(
            _3052.StraightBevelGearMeshCompoundSystemDeflection
        )

    @property
    def torque_converter_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3061.TorqueConverterConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3061,
        )

        return self.__parent__._cast(
            _3061.TorqueConverterConnectionCompoundSystemDeflection
        )

    @property
    def worm_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3067.WormGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3067,
        )

        return self.__parent__._cast(_3067.WormGearMeshCompoundSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3070.ZerolBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3070,
        )

        return self.__parent__._cast(_3070.ZerolBevelGearMeshCompoundSystemDeflection)

    @property
    def abstract_shaft_to_mountable_component_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3211.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3211,
        )

        return self.__parent__._cast(
            _3211.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3213.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3213,
        )

        return self.__parent__._cast(
            _3213.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def belt_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3217.BeltConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3217,
        )

        return self.__parent__._cast(
            _3217.BeltConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3220.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3220,
        )

        return self.__parent__._cast(
            _3220.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3225.BevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3225,
        )

        return self.__parent__._cast(
            _3225.BevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def clutch_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3230.ClutchConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3230,
        )

        return self.__parent__._cast(
            _3230.ClutchConnectionCompoundSteadyStateSynchronousResponse
        )

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
    def concept_coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3235.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3235,
        )

        return self.__parent__._cast(
            _3235.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def concept_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3238.ConceptGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3238,
        )

        return self.__parent__._cast(
            _3238.ConceptGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3241.ConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3241,
        )

        return self.__parent__._cast(
            _3241.ConicalGearMeshCompoundSteadyStateSynchronousResponse
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
    def coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3246.CouplingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3246,
        )

        return self.__parent__._cast(
            _3246.CouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def cvt_belt_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3248.CVTBeltConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3248,
        )

        return self.__parent__._cast(
            _3248.CVTBeltConnectionCompoundSteadyStateSynchronousResponse
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
    def cycloidal_disc_planetary_bearing_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3254.CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3254,
        )

        return self.__parent__._cast(
            _3254.CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3256.CylindricalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3256,
        )

        return self.__parent__._cast(
            _3256.CylindricalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def face_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3262.FaceGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3262,
        )

        return self.__parent__._cast(
            _3262.FaceGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3267.GearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3267,
        )

        return self.__parent__._cast(
            _3267.GearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def hypoid_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3271.HypoidGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3271,
        )

        return self.__parent__._cast(
            _3271.HypoidGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def inter_mountable_component_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> (
        "_3273.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3273,
        )

        return self.__parent__._cast(
            _3273.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3275.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3275,
        )

        return self.__parent__._cast(
            _3275.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3278.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3278,
        )

        return self.__parent__._cast(
            _3278.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3281.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3281,
        )

        return self.__parent__._cast(
            _3281.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def part_to_part_shear_coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> (
        "_3291.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3291,
        )

        return self.__parent__._cast(
            _3291.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse
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
    def ring_pins_to_disc_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3300.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3300,
        )

        return self.__parent__._cast(
            _3300.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def rolling_ring_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3303.RollingRingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3303,
        )

        return self.__parent__._cast(
            _3303.RollingRingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def shaft_to_mountable_component_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3307.ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3307,
        )

        return self.__parent__._cast(
            _3307.ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3310.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3310,
        )

        return self.__parent__._cast(
            _3310.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def spring_damper_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3313.SpringDamperConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3313,
        )

        return self.__parent__._cast(
            _3313.SpringDamperConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3316.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3316,
        )

        return self.__parent__._cast(
            _3316.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3319.StraightBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3319,
        )

        return self.__parent__._cast(
            _3319.StraightBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3328.TorqueConverterConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3328,
        )

        return self.__parent__._cast(
            _3328.TorqueConverterConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def worm_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3334.WormGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3334,
        )

        return self.__parent__._cast(
            _3334.WormGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def zerol_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3337.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3337,
        )

        return self.__parent__._cast(
            _3337.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3474.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3474,
        )

        return self.__parent__._cast(
            _3474.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3476.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3476,
        )

        return self.__parent__._cast(
            _3476.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def belt_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3480.BeltConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3480,
        )

        return self.__parent__._cast(
            _3480.BeltConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3483.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3483,
        )

        return self.__parent__._cast(
            _3483.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3488.BevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3488,
        )

        return self.__parent__._cast(
            _3488.BevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def clutch_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3493.ClutchConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3493,
        )

        return self.__parent__._cast(
            _3493.ClutchConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coaxial_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3495.CoaxialConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3495,
        )

        return self.__parent__._cast(
            _3495.CoaxialConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_coupling_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3498.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3498,
        )

        return self.__parent__._cast(
            _3498.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3501.ConceptGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3501,
        )

        return self.__parent__._cast(
            _3501.ConceptGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3504.ConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3504,
        )

        return self.__parent__._cast(
            _3504.ConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3506.ConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3506,
        )

        return self.__parent__._cast(
            _3506.ConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coupling_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3509.CouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3509,
        )

        return self.__parent__._cast(
            _3509.CouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cvt_belt_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3511.CVTBeltConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3511,
        )

        return self.__parent__._cast(
            _3511.CVTBeltConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3515.CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3515,
        )

        return self.__parent__._cast(
            _3515.CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3517.CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3517,
        )

        return self.__parent__._cast(
            _3517.CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3519.CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3519,
        )

        return self.__parent__._cast(
            _3519.CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def face_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3525.FaceGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3525,
        )

        return self.__parent__._cast(
            _3525.FaceGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3530.GearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3530,
        )

        return self.__parent__._cast(
            _3530.GearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def hypoid_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3534.HypoidGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3534,
        )

        return self.__parent__._cast(
            _3534.HypoidGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def inter_mountable_component_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3536.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3536,
        )

        return self.__parent__._cast(
            _3536.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3538.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3538,
        )

        return self.__parent__._cast(
            _3538.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3541.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3541,
        )

        return self.__parent__._cast(
            _3541.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3544.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3544,
        )

        return self.__parent__._cast(
            _3544.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_to_part_shear_coupling_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3554.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3554,
        )

        return self.__parent__._cast(
            _3554.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def planetary_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3556.PlanetaryConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3556,
        )

        return self.__parent__._cast(
            _3556.PlanetaryConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def ring_pins_to_disc_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3563.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3563,
        )

        return self.__parent__._cast(
            _3563.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def rolling_ring_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3566.RollingRingConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3566,
        )

        return self.__parent__._cast(
            _3566.RollingRingConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def shaft_to_mountable_component_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3570.ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3570,
        )

        return self.__parent__._cast(
            _3570.ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3573.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3573,
        )

        return self.__parent__._cast(
            _3573.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spring_damper_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3576.SpringDamperConnectionCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3576,
        )

        return self.__parent__._cast(
            _3576.SpringDamperConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3579.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3579,
        )

        return self.__parent__._cast(
            _3579.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3582.StraightBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3582,
        )

        return self.__parent__._cast(
            _3582.StraightBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_connection_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3591.TorqueConverterConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3591,
        )

        return self.__parent__._cast(
            _3591.TorqueConverterConnectionCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def worm_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3597.WormGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3597,
        )

        return self.__parent__._cast(
            _3597.WormGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_mesh_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3600.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3600,
        )

        return self.__parent__._cast(
            _3600.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3737.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3737,
        )

        return self.__parent__._cast(
            _3737.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3739.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3739,
        )

        return self.__parent__._cast(
            _3739.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def belt_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3743.BeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3743,
        )

        return self.__parent__._cast(
            _3743.BeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3746.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3746,
        )

        return self.__parent__._cast(
            _3746.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3751.BevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3751,
        )

        return self.__parent__._cast(
            _3751.BevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def clutch_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3756.ClutchConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3756,
        )

        return self.__parent__._cast(
            _3756.ClutchConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coaxial_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3758.CoaxialConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3758,
        )

        return self.__parent__._cast(
            _3758.CoaxialConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3761.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3761,
        )

        return self.__parent__._cast(
            _3761.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3764.ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3764,
        )

        return self.__parent__._cast(
            _3764.ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3767.ConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3767,
        )

        return self.__parent__._cast(
            _3767.ConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3769.ConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3769,
        )

        return self.__parent__._cast(
            _3769.ConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3772.CouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3772,
        )

        return self.__parent__._cast(
            _3772.CouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cvt_belt_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3774.CVTBeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3774,
        )

        return self.__parent__._cast(
            _3774.CVTBeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3778.CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3778,
        )

        return self.__parent__._cast(
            _3778.CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3780.CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3780,
        )

        return self.__parent__._cast(
            _3780.CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3782.CylindricalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3782,
        )

        return self.__parent__._cast(
            _3782.CylindricalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def face_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3788.FaceGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3788,
        )

        return self.__parent__._cast(
            _3788.FaceGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3793.GearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3793,
        )

        return self.__parent__._cast(
            _3793.GearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def hypoid_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3797.HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3797,
        )

        return self.__parent__._cast(
            _3797.HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def inter_mountable_component_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3799.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3799,
        )

        return self.__parent__._cast(
            _3799.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3801.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3801,
        )

        return self.__parent__._cast(
            _3801.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3804.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3804,
        )

        return self.__parent__._cast(
            _3804.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3807.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3807,
        )

        return self.__parent__._cast(
            _3807.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_to_part_shear_coupling_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3817.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3817,
        )

        return self.__parent__._cast(
            _3817.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def planetary_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3819.PlanetaryConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3819,
        )

        return self.__parent__._cast(
            _3819.PlanetaryConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def ring_pins_to_disc_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3826.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3826,
        )

        return self.__parent__._cast(
            _3826.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def rolling_ring_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3829.RollingRingConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3829,
        )

        return self.__parent__._cast(
            _3829.RollingRingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def shaft_to_mountable_component_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3833.ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3833,
        )

        return self.__parent__._cast(
            _3833.ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spiral_bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3836.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3836,
        )

        return self.__parent__._cast(
            _3836.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3839.SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3839,
        )

        return self.__parent__._cast(
            _3839.SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3842.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3842,
        )

        return self.__parent__._cast(
            _3842.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3845.StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3845,
        )

        return self.__parent__._cast(
            _3845.StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3854.TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3854,
        )

        return self.__parent__._cast(
            _3854.TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def worm_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3860.WormGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3860,
        )

        return self.__parent__._cast(
            _3860.WormGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def zerol_bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3863.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3863,
        )

        return self.__parent__._cast(
            _3863.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4004.AbstractShaftToMountableComponentConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4004,
        )

        return self.__parent__._cast(
            _4004.AbstractShaftToMountableComponentConnectionCompoundStabilityAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4006.AGMAGleasonConicalGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4006,
        )

        return self.__parent__._cast(
            _4006.AGMAGleasonConicalGearMeshCompoundStabilityAnalysis
        )

    @property
    def belt_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4010.BeltConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4010,
        )

        return self.__parent__._cast(_4010.BeltConnectionCompoundStabilityAnalysis)

    @property
    def bevel_differential_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4013.BevelDifferentialGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4013,
        )

        return self.__parent__._cast(
            _4013.BevelDifferentialGearMeshCompoundStabilityAnalysis
        )

    @property
    def bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4018.BevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4018,
        )

        return self.__parent__._cast(_4018.BevelGearMeshCompoundStabilityAnalysis)

    @property
    def clutch_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4023.ClutchConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4023,
        )

        return self.__parent__._cast(_4023.ClutchConnectionCompoundStabilityAnalysis)

    @property
    def coaxial_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4025.CoaxialConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4025,
        )

        return self.__parent__._cast(_4025.CoaxialConnectionCompoundStabilityAnalysis)

    @property
    def concept_coupling_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4028.ConceptCouplingConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4028,
        )

        return self.__parent__._cast(
            _4028.ConceptCouplingConnectionCompoundStabilityAnalysis
        )

    @property
    def concept_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4031.ConceptGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4031,
        )

        return self.__parent__._cast(_4031.ConceptGearMeshCompoundStabilityAnalysis)

    @property
    def conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4034.ConicalGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4034,
        )

        return self.__parent__._cast(_4034.ConicalGearMeshCompoundStabilityAnalysis)

    @property
    def connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4036.ConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4036,
        )

        return self.__parent__._cast(_4036.ConnectionCompoundStabilityAnalysis)

    @property
    def coupling_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4039.CouplingConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4039,
        )

        return self.__parent__._cast(_4039.CouplingConnectionCompoundStabilityAnalysis)

    @property
    def cvt_belt_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4041.CVTBeltConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4041,
        )

        return self.__parent__._cast(_4041.CVTBeltConnectionCompoundStabilityAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4045.CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4045,
        )

        return self.__parent__._cast(
            _4045.CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4047.CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4047,
        )

        return self.__parent__._cast(
            _4047.CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis
        )

    @property
    def cylindrical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4049.CylindricalGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4049,
        )

        return self.__parent__._cast(_4049.CylindricalGearMeshCompoundStabilityAnalysis)

    @property
    def face_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4055.FaceGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4055,
        )

        return self.__parent__._cast(_4055.FaceGearMeshCompoundStabilityAnalysis)

    @property
    def gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4060.GearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4060,
        )

        return self.__parent__._cast(_4060.GearMeshCompoundStabilityAnalysis)

    @property
    def hypoid_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4064.HypoidGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4064,
        )

        return self.__parent__._cast(_4064.HypoidGearMeshCompoundStabilityAnalysis)

    @property
    def inter_mountable_component_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4066.InterMountableComponentConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4066,
        )

        return self.__parent__._cast(
            _4066.InterMountableComponentConnectionCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4068.KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4068,
        )

        return self.__parent__._cast(
            _4068.KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4071.KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4071,
        )

        return self.__parent__._cast(
            _4071.KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4074.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4074,
        )

        return self.__parent__._cast(
            _4074.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4084.PartToPartShearCouplingConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4084,
        )

        return self.__parent__._cast(
            _4084.PartToPartShearCouplingConnectionCompoundStabilityAnalysis
        )

    @property
    def planetary_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4086.PlanetaryConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4086,
        )

        return self.__parent__._cast(_4086.PlanetaryConnectionCompoundStabilityAnalysis)

    @property
    def ring_pins_to_disc_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4093.RingPinsToDiscConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4093,
        )

        return self.__parent__._cast(
            _4093.RingPinsToDiscConnectionCompoundStabilityAnalysis
        )

    @property
    def rolling_ring_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4096.RollingRingConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4096,
        )

        return self.__parent__._cast(
            _4096.RollingRingConnectionCompoundStabilityAnalysis
        )

    @property
    def shaft_to_mountable_component_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4100.ShaftToMountableComponentConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4100,
        )

        return self.__parent__._cast(
            _4100.ShaftToMountableComponentConnectionCompoundStabilityAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4103.SpiralBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4103,
        )

        return self.__parent__._cast(_4103.SpiralBevelGearMeshCompoundStabilityAnalysis)

    @property
    def spring_damper_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4106.SpringDamperConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4106,
        )

        return self.__parent__._cast(
            _4106.SpringDamperConnectionCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4109.StraightBevelDiffGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4109,
        )

        return self.__parent__._cast(
            _4109.StraightBevelDiffGearMeshCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4112.StraightBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4112,
        )

        return self.__parent__._cast(
            _4112.StraightBevelGearMeshCompoundStabilityAnalysis
        )

    @property
    def torque_converter_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4121.TorqueConverterConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4121,
        )

        return self.__parent__._cast(
            _4121.TorqueConverterConnectionCompoundStabilityAnalysis
        )

    @property
    def worm_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4127.WormGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4127,
        )

        return self.__parent__._cast(_4127.WormGearMeshCompoundStabilityAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4130.ZerolBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4130,
        )

        return self.__parent__._cast(_4130.ZerolBevelGearMeshCompoundStabilityAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4278.AbstractShaftToMountableComponentConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4278,
        )

        return self.__parent__._cast(
            _4278.AbstractShaftToMountableComponentConnectionCompoundPowerFlow
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4280.AGMAGleasonConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4280,
        )

        return self.__parent__._cast(_4280.AGMAGleasonConicalGearMeshCompoundPowerFlow)

    @property
    def belt_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4284.BeltConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4284,
        )

        return self.__parent__._cast(_4284.BeltConnectionCompoundPowerFlow)

    @property
    def bevel_differential_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4287.BevelDifferentialGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4287,
        )

        return self.__parent__._cast(_4287.BevelDifferentialGearMeshCompoundPowerFlow)

    @property
    def bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4292.BevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4292,
        )

        return self.__parent__._cast(_4292.BevelGearMeshCompoundPowerFlow)

    @property
    def clutch_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4297.ClutchConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4297,
        )

        return self.__parent__._cast(_4297.ClutchConnectionCompoundPowerFlow)

    @property
    def coaxial_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4299.CoaxialConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4299,
        )

        return self.__parent__._cast(_4299.CoaxialConnectionCompoundPowerFlow)

    @property
    def concept_coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4302.ConceptCouplingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4302,
        )

        return self.__parent__._cast(_4302.ConceptCouplingConnectionCompoundPowerFlow)

    @property
    def concept_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4305.ConceptGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4305,
        )

        return self.__parent__._cast(_4305.ConceptGearMeshCompoundPowerFlow)

    @property
    def conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4308.ConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4308,
        )

        return self.__parent__._cast(_4308.ConicalGearMeshCompoundPowerFlow)

    @property
    def connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4310.ConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4310,
        )

        return self.__parent__._cast(_4310.ConnectionCompoundPowerFlow)

    @property
    def coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4313.CouplingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4313,
        )

        return self.__parent__._cast(_4313.CouplingConnectionCompoundPowerFlow)

    @property
    def cvt_belt_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4315.CVTBeltConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4315,
        )

        return self.__parent__._cast(_4315.CVTBeltConnectionCompoundPowerFlow)

    @property
    def cycloidal_disc_central_bearing_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4319.CycloidalDiscCentralBearingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4319,
        )

        return self.__parent__._cast(
            _4319.CycloidalDiscCentralBearingConnectionCompoundPowerFlow
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4321.CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4321,
        )

        return self.__parent__._cast(
            _4321.CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow
        )

    @property
    def cylindrical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4323.CylindricalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4323,
        )

        return self.__parent__._cast(_4323.CylindricalGearMeshCompoundPowerFlow)

    @property
    def face_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4329.FaceGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4329,
        )

        return self.__parent__._cast(_4329.FaceGearMeshCompoundPowerFlow)

    @property
    def gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4334.GearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4334,
        )

        return self.__parent__._cast(_4334.GearMeshCompoundPowerFlow)

    @property
    def hypoid_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4338.HypoidGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4338,
        )

        return self.__parent__._cast(_4338.HypoidGearMeshCompoundPowerFlow)

    @property
    def inter_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4340.InterMountableComponentConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4340,
        )

        return self.__parent__._cast(
            _4340.InterMountableComponentConnectionCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4342.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4342,
        )

        return self.__parent__._cast(
            _4342.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4345.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4345,
        )

        return self.__parent__._cast(
            _4345.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4348.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4348,
        )

        return self.__parent__._cast(
            _4348.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow
        )

    @property
    def part_to_part_shear_coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4358.PartToPartShearCouplingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4358,
        )

        return self.__parent__._cast(
            _4358.PartToPartShearCouplingConnectionCompoundPowerFlow
        )

    @property
    def planetary_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4360.PlanetaryConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4360,
        )

        return self.__parent__._cast(_4360.PlanetaryConnectionCompoundPowerFlow)

    @property
    def ring_pins_to_disc_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4367.RingPinsToDiscConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4367,
        )

        return self.__parent__._cast(_4367.RingPinsToDiscConnectionCompoundPowerFlow)

    @property
    def rolling_ring_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4370.RollingRingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4370,
        )

        return self.__parent__._cast(_4370.RollingRingConnectionCompoundPowerFlow)

    @property
    def shaft_to_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4374.ShaftToMountableComponentConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4374,
        )

        return self.__parent__._cast(
            _4374.ShaftToMountableComponentConnectionCompoundPowerFlow
        )

    @property
    def spiral_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4377.SpiralBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4377,
        )

        return self.__parent__._cast(_4377.SpiralBevelGearMeshCompoundPowerFlow)

    @property
    def spring_damper_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4380.SpringDamperConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4380,
        )

        return self.__parent__._cast(_4380.SpringDamperConnectionCompoundPowerFlow)

    @property
    def straight_bevel_diff_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4383.StraightBevelDiffGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4383,
        )

        return self.__parent__._cast(_4383.StraightBevelDiffGearMeshCompoundPowerFlow)

    @property
    def straight_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4386.StraightBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4386,
        )

        return self.__parent__._cast(_4386.StraightBevelGearMeshCompoundPowerFlow)

    @property
    def torque_converter_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4395.TorqueConverterConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4395,
        )

        return self.__parent__._cast(_4395.TorqueConverterConnectionCompoundPowerFlow)

    @property
    def worm_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4401.WormGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4401,
        )

        return self.__parent__._cast(_4401.WormGearMeshCompoundPowerFlow)

    @property
    def zerol_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4404.ZerolBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4404,
        )

        return self.__parent__._cast(_4404.ZerolBevelGearMeshCompoundPowerFlow)

    @property
    def abstract_shaft_to_mountable_component_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4558.AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4558,
        )

        return self.__parent__._cast(
            _4558.AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4560.AGMAGleasonConicalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4560,
        )

        return self.__parent__._cast(
            _4560.AGMAGleasonConicalGearMeshCompoundParametricStudyTool
        )

    @property
    def belt_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4564.BeltConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4564,
        )

        return self.__parent__._cast(_4564.BeltConnectionCompoundParametricStudyTool)

    @property
    def bevel_differential_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4567.BevelDifferentialGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4567,
        )

        return self.__parent__._cast(
            _4567.BevelDifferentialGearMeshCompoundParametricStudyTool
        )

    @property
    def bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4572.BevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4572,
        )

        return self.__parent__._cast(_4572.BevelGearMeshCompoundParametricStudyTool)

    @property
    def clutch_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4577.ClutchConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4577,
        )

        return self.__parent__._cast(_4577.ClutchConnectionCompoundParametricStudyTool)

    @property
    def coaxial_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4579.CoaxialConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4579,
        )

        return self.__parent__._cast(_4579.CoaxialConnectionCompoundParametricStudyTool)

    @property
    def concept_coupling_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4582.ConceptCouplingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4582,
        )

        return self.__parent__._cast(
            _4582.ConceptCouplingConnectionCompoundParametricStudyTool
        )

    @property
    def concept_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4585.ConceptGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4585,
        )

        return self.__parent__._cast(_4585.ConceptGearMeshCompoundParametricStudyTool)

    @property
    def conical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4588.ConicalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4588,
        )

        return self.__parent__._cast(_4588.ConicalGearMeshCompoundParametricStudyTool)

    @property
    def connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4590.ConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4590,
        )

        return self.__parent__._cast(_4590.ConnectionCompoundParametricStudyTool)

    @property
    def coupling_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4593.CouplingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4593,
        )

        return self.__parent__._cast(
            _4593.CouplingConnectionCompoundParametricStudyTool
        )

    @property
    def cvt_belt_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4595.CVTBeltConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4595,
        )

        return self.__parent__._cast(_4595.CVTBeltConnectionCompoundParametricStudyTool)

    @property
    def cycloidal_disc_central_bearing_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4599.CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4599,
        )

        return self.__parent__._cast(
            _4599.CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4601.CycloidalDiscPlanetaryBearingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4601,
        )

        return self.__parent__._cast(
            _4601.CycloidalDiscPlanetaryBearingConnectionCompoundParametricStudyTool
        )

    @property
    def cylindrical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4603.CylindricalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4603,
        )

        return self.__parent__._cast(
            _4603.CylindricalGearMeshCompoundParametricStudyTool
        )

    @property
    def face_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4609.FaceGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4609,
        )

        return self.__parent__._cast(_4609.FaceGearMeshCompoundParametricStudyTool)

    @property
    def gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4614.GearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4614,
        )

        return self.__parent__._cast(_4614.GearMeshCompoundParametricStudyTool)

    @property
    def hypoid_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4618.HypoidGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4618,
        )

        return self.__parent__._cast(_4618.HypoidGearMeshCompoundParametricStudyTool)

    @property
    def inter_mountable_component_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4620.InterMountableComponentConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4620,
        )

        return self.__parent__._cast(
            _4620.InterMountableComponentConnectionCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4622.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4622,
        )

        return self.__parent__._cast(
            _4622.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4625.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4625,
        )

        return self.__parent__._cast(
            _4625.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4628.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4628,
        )

        return self.__parent__._cast(
            _4628.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def part_to_part_shear_coupling_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4638.PartToPartShearCouplingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4638,
        )

        return self.__parent__._cast(
            _4638.PartToPartShearCouplingConnectionCompoundParametricStudyTool
        )

    @property
    def planetary_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4640.PlanetaryConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4640,
        )

        return self.__parent__._cast(
            _4640.PlanetaryConnectionCompoundParametricStudyTool
        )

    @property
    def ring_pins_to_disc_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4647.RingPinsToDiscConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4647,
        )

        return self.__parent__._cast(
            _4647.RingPinsToDiscConnectionCompoundParametricStudyTool
        )

    @property
    def rolling_ring_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4650.RollingRingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4650,
        )

        return self.__parent__._cast(
            _4650.RollingRingConnectionCompoundParametricStudyTool
        )

    @property
    def shaft_to_mountable_component_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4654.ShaftToMountableComponentConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4654,
        )

        return self.__parent__._cast(
            _4654.ShaftToMountableComponentConnectionCompoundParametricStudyTool
        )

    @property
    def spiral_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4657.SpiralBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4657,
        )

        return self.__parent__._cast(
            _4657.SpiralBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def spring_damper_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4660.SpringDamperConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4660,
        )

        return self.__parent__._cast(
            _4660.SpringDamperConnectionCompoundParametricStudyTool
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4663.StraightBevelDiffGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4663,
        )

        return self.__parent__._cast(
            _4663.StraightBevelDiffGearMeshCompoundParametricStudyTool
        )

    @property
    def straight_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4666.StraightBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4666,
        )

        return self.__parent__._cast(
            _4666.StraightBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def torque_converter_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4675.TorqueConverterConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4675,
        )

        return self.__parent__._cast(
            _4675.TorqueConverterConnectionCompoundParametricStudyTool
        )

    @property
    def worm_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4681.WormGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4681,
        )

        return self.__parent__._cast(_4681.WormGearMeshCompoundParametricStudyTool)

    @property
    def zerol_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4684.ZerolBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4684,
        )

        return self.__parent__._cast(
            _4684.ZerolBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4847.AbstractShaftToMountableComponentConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4847,
        )

        return self.__parent__._cast(
            _4847.AbstractShaftToMountableComponentConnectionCompoundModalAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4849.AGMAGleasonConicalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4849,
        )

        return self.__parent__._cast(
            _4849.AGMAGleasonConicalGearMeshCompoundModalAnalysis
        )

    @property
    def belt_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4853.BeltConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4853,
        )

        return self.__parent__._cast(_4853.BeltConnectionCompoundModalAnalysis)

    @property
    def bevel_differential_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4856.BevelDifferentialGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4856,
        )

        return self.__parent__._cast(
            _4856.BevelDifferentialGearMeshCompoundModalAnalysis
        )

    @property
    def bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4861.BevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4861,
        )

        return self.__parent__._cast(_4861.BevelGearMeshCompoundModalAnalysis)

    @property
    def clutch_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4866.ClutchConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4866,
        )

        return self.__parent__._cast(_4866.ClutchConnectionCompoundModalAnalysis)

    @property
    def coaxial_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4868.CoaxialConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4868,
        )

        return self.__parent__._cast(_4868.CoaxialConnectionCompoundModalAnalysis)

    @property
    def concept_coupling_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4871.ConceptCouplingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4871,
        )

        return self.__parent__._cast(
            _4871.ConceptCouplingConnectionCompoundModalAnalysis
        )

    @property
    def concept_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4874.ConceptGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4874,
        )

        return self.__parent__._cast(_4874.ConceptGearMeshCompoundModalAnalysis)

    @property
    def conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4877.ConicalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4877,
        )

        return self.__parent__._cast(_4877.ConicalGearMeshCompoundModalAnalysis)

    @property
    def connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4879.ConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4879,
        )

        return self.__parent__._cast(_4879.ConnectionCompoundModalAnalysis)

    @property
    def coupling_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4882.CouplingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4882,
        )

        return self.__parent__._cast(_4882.CouplingConnectionCompoundModalAnalysis)

    @property
    def cvt_belt_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4884.CVTBeltConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4884,
        )

        return self.__parent__._cast(_4884.CVTBeltConnectionCompoundModalAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4888.CycloidalDiscCentralBearingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4888,
        )

        return self.__parent__._cast(
            _4888.CycloidalDiscCentralBearingConnectionCompoundModalAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4890.CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4890,
        )

        return self.__parent__._cast(
            _4890.CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysis
        )

    @property
    def cylindrical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4892.CylindricalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4892,
        )

        return self.__parent__._cast(_4892.CylindricalGearMeshCompoundModalAnalysis)

    @property
    def face_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4898.FaceGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4898,
        )

        return self.__parent__._cast(_4898.FaceGearMeshCompoundModalAnalysis)

    @property
    def gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4903.GearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4903,
        )

        return self.__parent__._cast(_4903.GearMeshCompoundModalAnalysis)

    @property
    def hypoid_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4907.HypoidGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4907,
        )

        return self.__parent__._cast(_4907.HypoidGearMeshCompoundModalAnalysis)

    @property
    def inter_mountable_component_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4909.InterMountableComponentConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4909,
        )

        return self.__parent__._cast(
            _4909.InterMountableComponentConnectionCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4911.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4911,
        )

        return self.__parent__._cast(
            _4911.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4914.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4914,
        )

        return self.__parent__._cast(
            _4914.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4917.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4917,
        )

        return self.__parent__._cast(
            _4917.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4927.PartToPartShearCouplingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4927,
        )

        return self.__parent__._cast(
            _4927.PartToPartShearCouplingConnectionCompoundModalAnalysis
        )

    @property
    def planetary_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4929.PlanetaryConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4929,
        )

        return self.__parent__._cast(_4929.PlanetaryConnectionCompoundModalAnalysis)

    @property
    def ring_pins_to_disc_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4936.RingPinsToDiscConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4936,
        )

        return self.__parent__._cast(
            _4936.RingPinsToDiscConnectionCompoundModalAnalysis
        )

    @property
    def rolling_ring_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4939.RollingRingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4939,
        )

        return self.__parent__._cast(_4939.RollingRingConnectionCompoundModalAnalysis)

    @property
    def shaft_to_mountable_component_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4943.ShaftToMountableComponentConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4943,
        )

        return self.__parent__._cast(
            _4943.ShaftToMountableComponentConnectionCompoundModalAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4946.SpiralBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4946,
        )

        return self.__parent__._cast(_4946.SpiralBevelGearMeshCompoundModalAnalysis)

    @property
    def spring_damper_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4949.SpringDamperConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4949,
        )

        return self.__parent__._cast(_4949.SpringDamperConnectionCompoundModalAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4952.StraightBevelDiffGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4952,
        )

        return self.__parent__._cast(
            _4952.StraightBevelDiffGearMeshCompoundModalAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4955.StraightBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4955,
        )

        return self.__parent__._cast(_4955.StraightBevelGearMeshCompoundModalAnalysis)

    @property
    def torque_converter_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4964.TorqueConverterConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4964,
        )

        return self.__parent__._cast(
            _4964.TorqueConverterConnectionCompoundModalAnalysis
        )

    @property
    def worm_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4970.WormGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4970,
        )

        return self.__parent__._cast(_4970.WormGearMeshCompoundModalAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4973.ZerolBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4973,
        )

        return self.__parent__._cast(_4973.ZerolBevelGearMeshCompoundModalAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5111.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5111,
        )

        return self.__parent__._cast(
            _5111.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5113.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5113,
        )

        return self.__parent__._cast(
            _5113.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def belt_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5117.BeltConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5117,
        )

        return self.__parent__._cast(
            _5117.BeltConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5120.BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5120,
        )

        return self.__parent__._cast(
            _5120.BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5125.BevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5125,
        )

        return self.__parent__._cast(
            _5125.BevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def clutch_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5130.ClutchConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5130,
        )

        return self.__parent__._cast(
            _5130.ClutchConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def coaxial_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5132.CoaxialConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5132,
        )

        return self.__parent__._cast(
            _5132.CoaxialConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def concept_coupling_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5135.ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5135,
        )

        return self.__parent__._cast(
            _5135.ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def concept_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5138.ConceptGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5138,
        )

        return self.__parent__._cast(
            _5138.ConceptGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def conical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5141.ConicalGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5141,
        )

        return self.__parent__._cast(
            _5141.ConicalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5143.ConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5143,
        )

        return self.__parent__._cast(_5143.ConnectionCompoundModalAnalysisAtAStiffness)

    @property
    def coupling_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5146.CouplingConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5146,
        )

        return self.__parent__._cast(
            _5146.CouplingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def cvt_belt_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5148.CVTBeltConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5148,
        )

        return self.__parent__._cast(
            _5148.CVTBeltConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5152.CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5152,
        )

        return self.__parent__._cast(
            _5152.CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> (
        "_5154.CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtAStiffness"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5154,
        )

        return self.__parent__._cast(
            _5154.CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def cylindrical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5156.CylindricalGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5156,
        )

        return self.__parent__._cast(
            _5156.CylindricalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def face_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5162.FaceGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5162,
        )

        return self.__parent__._cast(
            _5162.FaceGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5167.GearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5167,
        )

        return self.__parent__._cast(_5167.GearMeshCompoundModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5171.HypoidGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5171,
        )

        return self.__parent__._cast(
            _5171.HypoidGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def inter_mountable_component_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5173.InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5173,
        )

        return self.__parent__._cast(
            _5173.InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> (
        "_5175.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5175,
        )

        return self.__parent__._cast(
            _5175.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> (
        "_5178.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtAStiffness"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5178,
        )

        return self.__parent__._cast(
            _5178.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5181.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5181,
        )

        return self.__parent__._cast(
            _5181.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def part_to_part_shear_coupling_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5191.PartToPartShearCouplingConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5191,
        )

        return self.__parent__._cast(
            _5191.PartToPartShearCouplingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def planetary_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5193.PlanetaryConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5193,
        )

        return self.__parent__._cast(
            _5193.PlanetaryConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def ring_pins_to_disc_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5200.RingPinsToDiscConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5200,
        )

        return self.__parent__._cast(
            _5200.RingPinsToDiscConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def rolling_ring_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5203.RollingRingConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5203,
        )

        return self.__parent__._cast(
            _5203.RollingRingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def shaft_to_mountable_component_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5207.ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5207,
        )

        return self.__parent__._cast(
            _5207.ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def spiral_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5210.SpiralBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5210,
        )

        return self.__parent__._cast(
            _5210.SpiralBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def spring_damper_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5213.SpringDamperConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5213,
        )

        return self.__parent__._cast(
            _5213.SpringDamperConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5216.StraightBevelDiffGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5216,
        )

        return self.__parent__._cast(
            _5216.StraightBevelDiffGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5219.StraightBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5219,
        )

        return self.__parent__._cast(
            _5219.StraightBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def torque_converter_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5228.TorqueConverterConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5228,
        )

        return self.__parent__._cast(
            _5228.TorqueConverterConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def worm_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5234.WormGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5234,
        )

        return self.__parent__._cast(
            _5234.WormGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def zerol_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5237.ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5237,
        )

        return self.__parent__._cast(
            _5237.ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_5374.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5374,
        )

        return self.__parent__._cast(
            _5374.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5376.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5376,
        )

        return self.__parent__._cast(
            _5376.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def belt_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5380.BeltConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5380,
        )

        return self.__parent__._cast(_5380.BeltConnectionCompoundModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5383.BevelDifferentialGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5383,
        )

        return self.__parent__._cast(
            _5383.BevelDifferentialGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5388.BevelGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5388,
        )

        return self.__parent__._cast(_5388.BevelGearMeshCompoundModalAnalysisAtASpeed)

    @property
    def clutch_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5393.ClutchConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5393,
        )

        return self.__parent__._cast(
            _5393.ClutchConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def coaxial_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5395.CoaxialConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5395,
        )

        return self.__parent__._cast(
            _5395.CoaxialConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def concept_coupling_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5398.ConceptCouplingConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5398,
        )

        return self.__parent__._cast(
            _5398.ConceptCouplingConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def concept_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5401.ConceptGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5401,
        )

        return self.__parent__._cast(_5401.ConceptGearMeshCompoundModalAnalysisAtASpeed)

    @property
    def conical_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5404.ConicalGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5404,
        )

        return self.__parent__._cast(_5404.ConicalGearMeshCompoundModalAnalysisAtASpeed)

    @property
    def connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5406.ConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5406,
        )

        return self.__parent__._cast(_5406.ConnectionCompoundModalAnalysisAtASpeed)

    @property
    def coupling_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5409.CouplingConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5409,
        )

        return self.__parent__._cast(
            _5409.CouplingConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def cvt_belt_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5411.CVTBeltConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5411,
        )

        return self.__parent__._cast(
            _5411.CVTBeltConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5415.CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5415,
        )

        return self.__parent__._cast(
            _5415.CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5417.CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5417,
        )

        return self.__parent__._cast(
            _5417.CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def cylindrical_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5419.CylindricalGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5419,
        )

        return self.__parent__._cast(
            _5419.CylindricalGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def face_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5425.FaceGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5425,
        )

        return self.__parent__._cast(_5425.FaceGearMeshCompoundModalAnalysisAtASpeed)

    @property
    def gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5430.GearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5430,
        )

        return self.__parent__._cast(_5430.GearMeshCompoundModalAnalysisAtASpeed)

    @property
    def hypoid_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5434.HypoidGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5434,
        )

        return self.__parent__._cast(_5434.HypoidGearMeshCompoundModalAnalysisAtASpeed)

    @property
    def inter_mountable_component_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5436.InterMountableComponentConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5436,
        )

        return self.__parent__._cast(
            _5436.InterMountableComponentConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5438.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5438,
        )

        return self.__parent__._cast(
            _5438.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5441.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5441,
        )

        return self.__parent__._cast(
            _5441.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_5444.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5444,
        )

        return self.__parent__._cast(
            _5444.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def part_to_part_shear_coupling_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5454.PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5454,
        )

        return self.__parent__._cast(
            _5454.PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def planetary_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5456.PlanetaryConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5456,
        )

        return self.__parent__._cast(
            _5456.PlanetaryConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def ring_pins_to_disc_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5463.RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5463,
        )

        return self.__parent__._cast(
            _5463.RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def rolling_ring_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5466.RollingRingConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5466,
        )

        return self.__parent__._cast(
            _5466.RollingRingConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def shaft_to_mountable_component_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5470.ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5470,
        )

        return self.__parent__._cast(
            _5470.ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def spiral_bevel_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5473.SpiralBevelGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5473,
        )

        return self.__parent__._cast(
            _5473.SpiralBevelGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def spring_damper_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5476.SpringDamperConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5476,
        )

        return self.__parent__._cast(
            _5476.SpringDamperConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5479.StraightBevelDiffGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5479,
        )

        return self.__parent__._cast(
            _5479.StraightBevelDiffGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5482.StraightBevelGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5482,
        )

        return self.__parent__._cast(
            _5482.StraightBevelGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def torque_converter_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5491.TorqueConverterConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5491,
        )

        return self.__parent__._cast(
            _5491.TorqueConverterConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def worm_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5497.WormGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5497,
        )

        return self.__parent__._cast(_5497.WormGearMeshCompoundModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5500.ZerolBevelGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5500,
        )

        return self.__parent__._cast(
            _5500.ZerolBevelGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5663.AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5663,
        )

        return self.__parent__._cast(
            _5663.AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5665.AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5665,
        )

        return self.__parent__._cast(
            _5665.AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def belt_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5669.BeltConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5669,
        )

        return self.__parent__._cast(
            _5669.BeltConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5672.BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5672,
        )

        return self.__parent__._cast(
            _5672.BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5677.BevelGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5677,
        )

        return self.__parent__._cast(
            _5677.BevelGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def clutch_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5682.ClutchConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5682,
        )

        return self.__parent__._cast(
            _5682.ClutchConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def coaxial_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5684.CoaxialConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5684,
        )

        return self.__parent__._cast(
            _5684.CoaxialConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def concept_coupling_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5687.ConceptCouplingConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5687,
        )

        return self.__parent__._cast(
            _5687.ConceptCouplingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def concept_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5690.ConceptGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5690,
        )

        return self.__parent__._cast(
            _5690.ConceptGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def conical_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5693.ConicalGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5693,
        )

        return self.__parent__._cast(
            _5693.ConicalGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5695.ConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5695,
        )

        return self.__parent__._cast(_5695.ConnectionCompoundMultibodyDynamicsAnalysis)

    @property
    def coupling_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5698.CouplingConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5698,
        )

        return self.__parent__._cast(
            _5698.CouplingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def cvt_belt_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5700.CVTBeltConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5700,
        )

        return self.__parent__._cast(
            _5700.CVTBeltConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5704.CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5704,
        )

        return self.__parent__._cast(
            _5704.CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> (
        "_5706.CycloidalDiscPlanetaryBearingConnectionCompoundMultibodyDynamicsAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5706,
        )

        return self.__parent__._cast(
            _5706.CycloidalDiscPlanetaryBearingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def cylindrical_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5708.CylindricalGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5708,
        )

        return self.__parent__._cast(
            _5708.CylindricalGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def face_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5714.FaceGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5714,
        )

        return self.__parent__._cast(
            _5714.FaceGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5719.GearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5719,
        )

        return self.__parent__._cast(_5719.GearMeshCompoundMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5723.HypoidGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5723,
        )

        return self.__parent__._cast(
            _5723.HypoidGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def inter_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5725.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5725,
        )

        return self.__parent__._cast(
            _5725.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> (
        "_5727.KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5727,
        )

        return self.__parent__._cast(
            _5727.KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> (
        "_5730.KlingelnbergCycloPalloidHypoidGearMeshCompoundMultibodyDynamicsAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5730,
        )

        return self.__parent__._cast(
            _5730.KlingelnbergCycloPalloidHypoidGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5733.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5733,
        )

        return self.__parent__._cast(
            _5733.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5743.PartToPartShearCouplingConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5743,
        )

        return self.__parent__._cast(
            _5743.PartToPartShearCouplingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def planetary_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5745.PlanetaryConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5745,
        )

        return self.__parent__._cast(
            _5745.PlanetaryConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def ring_pins_to_disc_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5752.RingPinsToDiscConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5752,
        )

        return self.__parent__._cast(
            _5752.RingPinsToDiscConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def rolling_ring_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5755.RollingRingConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5755,
        )

        return self.__parent__._cast(
            _5755.RollingRingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def shaft_to_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5759.ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5759,
        )

        return self.__parent__._cast(
            _5759.ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5762.SpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5762,
        )

        return self.__parent__._cast(
            _5762.SpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def spring_damper_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5765.SpringDamperConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5765,
        )

        return self.__parent__._cast(
            _5765.SpringDamperConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5768.StraightBevelDiffGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5768,
        )

        return self.__parent__._cast(
            _5768.StraightBevelDiffGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5771.StraightBevelGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5771,
        )

        return self.__parent__._cast(
            _5771.StraightBevelGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def torque_converter_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5780.TorqueConverterConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5780,
        )

        return self.__parent__._cast(
            _5780.TorqueConverterConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def worm_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5786.WormGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5786,
        )

        return self.__parent__._cast(
            _5786.WormGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def zerol_bevel_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5789.ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5789,
        )

        return self.__parent__._cast(
            _5789.ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6017.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6017,
        )

        return self.__parent__._cast(
            _6017.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6019.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6019,
        )

        return self.__parent__._cast(
            _6019.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis
        )

    @property
    def belt_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6023.BeltConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6023,
        )

        return self.__parent__._cast(_6023.BeltConnectionCompoundHarmonicAnalysis)

    @property
    def bevel_differential_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6026.BevelDifferentialGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6026,
        )

        return self.__parent__._cast(
            _6026.BevelDifferentialGearMeshCompoundHarmonicAnalysis
        )

    @property
    def bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6031.BevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6031,
        )

        return self.__parent__._cast(_6031.BevelGearMeshCompoundHarmonicAnalysis)

    @property
    def clutch_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6036.ClutchConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6036,
        )

        return self.__parent__._cast(_6036.ClutchConnectionCompoundHarmonicAnalysis)

    @property
    def coaxial_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6038.CoaxialConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6038,
        )

        return self.__parent__._cast(_6038.CoaxialConnectionCompoundHarmonicAnalysis)

    @property
    def concept_coupling_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6041.ConceptCouplingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6041,
        )

        return self.__parent__._cast(
            _6041.ConceptCouplingConnectionCompoundHarmonicAnalysis
        )

    @property
    def concept_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6044.ConceptGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6044,
        )

        return self.__parent__._cast(_6044.ConceptGearMeshCompoundHarmonicAnalysis)

    @property
    def conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6047.ConicalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6047,
        )

        return self.__parent__._cast(_6047.ConicalGearMeshCompoundHarmonicAnalysis)

    @property
    def connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6049.ConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6049,
        )

        return self.__parent__._cast(_6049.ConnectionCompoundHarmonicAnalysis)

    @property
    def coupling_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6052.CouplingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6052,
        )

        return self.__parent__._cast(_6052.CouplingConnectionCompoundHarmonicAnalysis)

    @property
    def cvt_belt_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6054.CVTBeltConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6054,
        )

        return self.__parent__._cast(_6054.CVTBeltConnectionCompoundHarmonicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6058.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6058,
        )

        return self.__parent__._cast(
            _6058.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6060.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6060,
        )

        return self.__parent__._cast(
            _6060.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysis
        )

    @property
    def cylindrical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6062.CylindricalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6062,
        )

        return self.__parent__._cast(_6062.CylindricalGearMeshCompoundHarmonicAnalysis)

    @property
    def face_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6068.FaceGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6068,
        )

        return self.__parent__._cast(_6068.FaceGearMeshCompoundHarmonicAnalysis)

    @property
    def gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6073.GearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6073,
        )

        return self.__parent__._cast(_6073.GearMeshCompoundHarmonicAnalysis)

    @property
    def hypoid_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6077.HypoidGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6077,
        )

        return self.__parent__._cast(_6077.HypoidGearMeshCompoundHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6079.InterMountableComponentConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6079,
        )

        return self.__parent__._cast(
            _6079.InterMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6081.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6081,
        )

        return self.__parent__._cast(
            _6081.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6084.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6084,
        )

        return self.__parent__._cast(
            _6084.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6087.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6087,
        )

        return self.__parent__._cast(
            _6087.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6097.PartToPartShearCouplingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6097,
        )

        return self.__parent__._cast(
            _6097.PartToPartShearCouplingConnectionCompoundHarmonicAnalysis
        )

    @property
    def planetary_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6099.PlanetaryConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6099,
        )

        return self.__parent__._cast(_6099.PlanetaryConnectionCompoundHarmonicAnalysis)

    @property
    def ring_pins_to_disc_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6106.RingPinsToDiscConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6106,
        )

        return self.__parent__._cast(
            _6106.RingPinsToDiscConnectionCompoundHarmonicAnalysis
        )

    @property
    def rolling_ring_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6109.RollingRingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6109,
        )

        return self.__parent__._cast(
            _6109.RollingRingConnectionCompoundHarmonicAnalysis
        )

    @property
    def shaft_to_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6113.ShaftToMountableComponentConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6113,
        )

        return self.__parent__._cast(
            _6113.ShaftToMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6116.SpiralBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6116,
        )

        return self.__parent__._cast(_6116.SpiralBevelGearMeshCompoundHarmonicAnalysis)

    @property
    def spring_damper_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6119.SpringDamperConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6119,
        )

        return self.__parent__._cast(
            _6119.SpringDamperConnectionCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6122.StraightBevelDiffGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6122,
        )

        return self.__parent__._cast(
            _6122.StraightBevelDiffGearMeshCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6125.StraightBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6125,
        )

        return self.__parent__._cast(
            _6125.StraightBevelGearMeshCompoundHarmonicAnalysis
        )

    @property
    def torque_converter_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6134.TorqueConverterConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6134,
        )

        return self.__parent__._cast(
            _6134.TorqueConverterConnectionCompoundHarmonicAnalysis
        )

    @property
    def worm_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6140.WormGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6140,
        )

        return self.__parent__._cast(_6140.WormGearMeshCompoundHarmonicAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6143.ZerolBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6143,
        )

        return self.__parent__._cast(_6143.ZerolBevelGearMeshCompoundHarmonicAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6281.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6281,
        )

        return self.__parent__._cast(
            _6281.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6283.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6283,
        )

        return self.__parent__._cast(
            _6283.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def belt_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6287.BeltConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6287,
        )

        return self.__parent__._cast(
            _6287.BeltConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6290.BevelDifferentialGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6290,
        )

        return self.__parent__._cast(
            _6290.BevelDifferentialGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6295.BevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6295,
        )

        return self.__parent__._cast(
            _6295.BevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def clutch_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6300.ClutchConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6300,
        )

        return self.__parent__._cast(
            _6300.ClutchConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coaxial_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6302.CoaxialConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6302,
        )

        return self.__parent__._cast(
            _6302.CoaxialConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_coupling_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6305.ConceptCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6305,
        )

        return self.__parent__._cast(
            _6305.ConceptCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6308.ConceptGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6308,
        )

        return self.__parent__._cast(
            _6308.ConceptGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6311.ConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6311,
        )

        return self.__parent__._cast(
            _6311.ConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6313.ConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6313,
        )

        return self.__parent__._cast(
            _6313.ConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coupling_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6316.CouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6316,
        )

        return self.__parent__._cast(
            _6316.CouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cvt_belt_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6318.CVTBeltConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6318,
        )

        return self.__parent__._cast(
            _6318.CVTBeltConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6322.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6322,
        )

        return self.__parent__._cast(
            _6322.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6324.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6324,
        )

        return self.__parent__._cast(
            _6324.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6326.CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6326,
        )

        return self.__parent__._cast(
            _6326.CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def face_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6332.FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6332,
        )

        return self.__parent__._cast(
            _6332.FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6337.GearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6337,
        )

        return self.__parent__._cast(
            _6337.GearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def hypoid_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6341.HypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6341,
        )

        return self.__parent__._cast(
            _6341.HypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def inter_mountable_component_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6343.InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6343,
        )

        return self.__parent__._cast(
            _6343.InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6345.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6345,
        )

        return self.__parent__._cast(
            _6345.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6348.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6348,
        )

        return self.__parent__._cast(
            _6348.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6351.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6351,
        )

        return self.__parent__._cast(
            _6351.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_to_part_shear_coupling_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6361.PartToPartShearCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6361,
        )

        return self.__parent__._cast(
            _6361.PartToPartShearCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planetary_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6363.PlanetaryConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6363,
        )

        return self.__parent__._cast(
            _6363.PlanetaryConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def ring_pins_to_disc_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6370.RingPinsToDiscConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6370,
        )

        return self.__parent__._cast(
            _6370.RingPinsToDiscConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def rolling_ring_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6373.RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6373,
        )

        return self.__parent__._cast(
            _6373.RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def shaft_to_mountable_component_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6377.ShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6377,
        )

        return self.__parent__._cast(
            _6377.ShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6380.SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6380,
        )

        return self.__parent__._cast(
            _6380.SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6383.SpringDamperConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6383,
        )

        return self.__parent__._cast(
            _6383.SpringDamperConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6386.StraightBevelDiffGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6386,
        )

        return self.__parent__._cast(
            _6386.StraightBevelDiffGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6389.StraightBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6389,
        )

        return self.__parent__._cast(
            _6389.StraightBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6398.TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6398,
        )

        return self.__parent__._cast(
            _6398.TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def worm_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6404.WormGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6404,
        )

        return self.__parent__._cast(
            _6404.WormGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6407.ZerolBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6407,
        )

        return self.__parent__._cast(
            _6407.ZerolBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6554.AbstractShaftToMountableComponentConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6554,
        )

        return self.__parent__._cast(
            _6554.AbstractShaftToMountableComponentConnectionCompoundDynamicAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6556.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6556,
        )

        return self.__parent__._cast(
            _6556.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis
        )

    @property
    def belt_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6560.BeltConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6560,
        )

        return self.__parent__._cast(_6560.BeltConnectionCompoundDynamicAnalysis)

    @property
    def bevel_differential_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6563.BevelDifferentialGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6563,
        )

        return self.__parent__._cast(
            _6563.BevelDifferentialGearMeshCompoundDynamicAnalysis
        )

    @property
    def bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6568.BevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6568,
        )

        return self.__parent__._cast(_6568.BevelGearMeshCompoundDynamicAnalysis)

    @property
    def clutch_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6573.ClutchConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6573,
        )

        return self.__parent__._cast(_6573.ClutchConnectionCompoundDynamicAnalysis)

    @property
    def coaxial_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6575.CoaxialConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6575,
        )

        return self.__parent__._cast(_6575.CoaxialConnectionCompoundDynamicAnalysis)

    @property
    def concept_coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6578.ConceptCouplingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6578,
        )

        return self.__parent__._cast(
            _6578.ConceptCouplingConnectionCompoundDynamicAnalysis
        )

    @property
    def concept_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6581.ConceptGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6581,
        )

        return self.__parent__._cast(_6581.ConceptGearMeshCompoundDynamicAnalysis)

    @property
    def conical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6584.ConicalGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6584,
        )

        return self.__parent__._cast(_6584.ConicalGearMeshCompoundDynamicAnalysis)

    @property
    def connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6586.ConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6586,
        )

        return self.__parent__._cast(_6586.ConnectionCompoundDynamicAnalysis)

    @property
    def coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6589.CouplingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6589,
        )

        return self.__parent__._cast(_6589.CouplingConnectionCompoundDynamicAnalysis)

    @property
    def cvt_belt_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6591.CVTBeltConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6591,
        )

        return self.__parent__._cast(_6591.CVTBeltConnectionCompoundDynamicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6595.CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6595,
        )

        return self.__parent__._cast(
            _6595.CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6597.CycloidalDiscPlanetaryBearingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6597,
        )

        return self.__parent__._cast(
            _6597.CycloidalDiscPlanetaryBearingConnectionCompoundDynamicAnalysis
        )

    @property
    def cylindrical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6599.CylindricalGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6599,
        )

        return self.__parent__._cast(_6599.CylindricalGearMeshCompoundDynamicAnalysis)

    @property
    def face_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6605.FaceGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6605,
        )

        return self.__parent__._cast(_6605.FaceGearMeshCompoundDynamicAnalysis)

    @property
    def gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6610.GearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6610,
        )

        return self.__parent__._cast(_6610.GearMeshCompoundDynamicAnalysis)

    @property
    def hypoid_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6614.HypoidGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6614,
        )

        return self.__parent__._cast(_6614.HypoidGearMeshCompoundDynamicAnalysis)

    @property
    def inter_mountable_component_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6616.InterMountableComponentConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6616,
        )

        return self.__parent__._cast(
            _6616.InterMountableComponentConnectionCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6618.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6618,
        )

        return self.__parent__._cast(
            _6618.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6621.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6621,
        )

        return self.__parent__._cast(
            _6621.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6624.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6624,
        )

        return self.__parent__._cast(
            _6624.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6634.PartToPartShearCouplingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6634,
        )

        return self.__parent__._cast(
            _6634.PartToPartShearCouplingConnectionCompoundDynamicAnalysis
        )

    @property
    def planetary_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6636.PlanetaryConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6636,
        )

        return self.__parent__._cast(_6636.PlanetaryConnectionCompoundDynamicAnalysis)

    @property
    def ring_pins_to_disc_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6643.RingPinsToDiscConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6643,
        )

        return self.__parent__._cast(
            _6643.RingPinsToDiscConnectionCompoundDynamicAnalysis
        )

    @property
    def rolling_ring_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6646.RollingRingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6646,
        )

        return self.__parent__._cast(_6646.RollingRingConnectionCompoundDynamicAnalysis)

    @property
    def shaft_to_mountable_component_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6650.ShaftToMountableComponentConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6650,
        )

        return self.__parent__._cast(
            _6650.ShaftToMountableComponentConnectionCompoundDynamicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6653.SpiralBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6653,
        )

        return self.__parent__._cast(_6653.SpiralBevelGearMeshCompoundDynamicAnalysis)

    @property
    def spring_damper_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6656.SpringDamperConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6656,
        )

        return self.__parent__._cast(
            _6656.SpringDamperConnectionCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6659.StraightBevelDiffGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6659,
        )

        return self.__parent__._cast(
            _6659.StraightBevelDiffGearMeshCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6662.StraightBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6662,
        )

        return self.__parent__._cast(_6662.StraightBevelGearMeshCompoundDynamicAnalysis)

    @property
    def torque_converter_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6671.TorqueConverterConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6671,
        )

        return self.__parent__._cast(
            _6671.TorqueConverterConnectionCompoundDynamicAnalysis
        )

    @property
    def worm_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6677.WormGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6677,
        )

        return self.__parent__._cast(_6677.WormGearMeshCompoundDynamicAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6680.ZerolBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6680,
        )

        return self.__parent__._cast(_6680.ZerolBevelGearMeshCompoundDynamicAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> (
        "_6825.AbstractShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6825,
        )

        return self.__parent__._cast(
            _6825.AbstractShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6827.AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6827,
        )

        return self.__parent__._cast(
            _6827.AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def belt_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6831.BeltConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6831,
        )

        return self.__parent__._cast(_6831.BeltConnectionCompoundCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6834.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6834,
        )

        return self.__parent__._cast(
            _6834.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6839.BevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6839,
        )

        return self.__parent__._cast(_6839.BevelGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def clutch_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6844.ClutchConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6844,
        )

        return self.__parent__._cast(
            _6844.ClutchConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def coaxial_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6846.CoaxialConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6846,
        )

        return self.__parent__._cast(
            _6846.CoaxialConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def concept_coupling_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6849.ConceptCouplingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6849,
        )

        return self.__parent__._cast(
            _6849.ConceptCouplingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def concept_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6852.ConceptGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6852,
        )

        return self.__parent__._cast(_6852.ConceptGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def conical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6855.ConicalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6855,
        )

        return self.__parent__._cast(_6855.ConicalGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6857.ConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6857,
        )

        return self.__parent__._cast(_6857.ConnectionCompoundCriticalSpeedAnalysis)

    @property
    def coupling_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6860.CouplingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6860,
        )

        return self.__parent__._cast(
            _6860.CouplingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def cvt_belt_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6862.CVTBeltConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6862,
        )

        return self.__parent__._cast(
            _6862.CVTBeltConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6866.CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6866,
        )

        return self.__parent__._cast(
            _6866.CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6868.CycloidalDiscPlanetaryBearingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6868,
        )

        return self.__parent__._cast(
            _6868.CycloidalDiscPlanetaryBearingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def cylindrical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6870.CylindricalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6870,
        )

        return self.__parent__._cast(
            _6870.CylindricalGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def face_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6876.FaceGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6876,
        )

        return self.__parent__._cast(_6876.FaceGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6881.GearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6881,
        )

        return self.__parent__._cast(_6881.GearMeshCompoundCriticalSpeedAnalysis)

    @property
    def hypoid_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6885.HypoidGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6885,
        )

        return self.__parent__._cast(_6885.HypoidGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def inter_mountable_component_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6887.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6887,
        )

        return self.__parent__._cast(
            _6887.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6889.KlingelnbergCycloPalloidConicalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6889,
        )

        return self.__parent__._cast(
            _6889.KlingelnbergCycloPalloidConicalGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6892.KlingelnbergCycloPalloidHypoidGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6892,
        )

        return self.__parent__._cast(
            _6892.KlingelnbergCycloPalloidHypoidGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> (
        "_6895.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6895,
        )

        return self.__parent__._cast(
            _6895.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6905.PartToPartShearCouplingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6905,
        )

        return self.__parent__._cast(
            _6905.PartToPartShearCouplingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def planetary_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6907.PlanetaryConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6907,
        )

        return self.__parent__._cast(
            _6907.PlanetaryConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def ring_pins_to_disc_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6914.RingPinsToDiscConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6914,
        )

        return self.__parent__._cast(
            _6914.RingPinsToDiscConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def rolling_ring_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6917.RollingRingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6917,
        )

        return self.__parent__._cast(
            _6917.RollingRingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def shaft_to_mountable_component_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6921.ShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6921,
        )

        return self.__parent__._cast(
            _6921.ShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6924.SpiralBevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6924,
        )

        return self.__parent__._cast(
            _6924.SpiralBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def spring_damper_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6927.SpringDamperConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6927,
        )

        return self.__parent__._cast(
            _6927.SpringDamperConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6930.StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6930,
        )

        return self.__parent__._cast(
            _6930.StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6933.StraightBevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6933,
        )

        return self.__parent__._cast(
            _6933.StraightBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def torque_converter_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6942.TorqueConverterConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6942,
        )

        return self.__parent__._cast(
            _6942.TorqueConverterConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def worm_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6948.WormGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6948,
        )

        return self.__parent__._cast(_6948.WormGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6951.ZerolBevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6951,
        )

        return self.__parent__._cast(
            _6951.ZerolBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7297.AbstractShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7297,
        )

        return self.__parent__._cast(
            _7297.AbstractShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7299.AGMAGleasonConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7299,
        )

        return self.__parent__._cast(
            _7299.AGMAGleasonConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def belt_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7303.BeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7303,
        )

        return self.__parent__._cast(
            _7303.BeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7306.BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7306,
        )

        return self.__parent__._cast(
            _7306.BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7311.BevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7311,
        )

        return self.__parent__._cast(
            _7311.BevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def clutch_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7316.ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7316,
        )

        return self.__parent__._cast(
            _7316.ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coaxial_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7318.CoaxialConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7318,
        )

        return self.__parent__._cast(
            _7318.CoaxialConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7321.ConceptCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7321,
        )

        return self.__parent__._cast(
            _7321.ConceptCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7324.ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7324,
        )

        return self.__parent__._cast(
            _7324.ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7327.ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7327,
        )

        return self.__parent__._cast(
            _7327.ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7329.ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7329,
        )

        return self.__parent__._cast(
            _7329.ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7332.CouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7332,
        )

        return self.__parent__._cast(
            _7332.CouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cvt_belt_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7334.CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7334,
        )

        return self.__parent__._cast(
            _7334.CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7338.CycloidalDiscCentralBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7338,
        )

        return self.__parent__._cast(
            _7338.CycloidalDiscCentralBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7340.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7340,
        )

        return self.__parent__._cast(
            _7340.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7342.CylindricalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7342,
        )

        return self.__parent__._cast(
            _7342.CylindricalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7348.FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7348,
        )

        return self.__parent__._cast(
            _7348.FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7353.GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7353,
        )

        return self.__parent__._cast(
            _7353.GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7357.HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7357,
        )

        return self.__parent__._cast(
            _7357.HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def inter_mountable_component_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7359.InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7359,
        )

        return self.__parent__._cast(
            _7359.InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7361.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7361,
        )

        return self.__parent__._cast(
            _7361.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7364.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7364,
        )

        return self.__parent__._cast(
            _7364.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7367.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7367,
        )

        return self.__parent__._cast(
            _7367.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7377.PartToPartShearCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7377,
        )

        return self.__parent__._cast(
            _7377.PartToPartShearCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planetary_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7379.PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7379,
        )

        return self.__parent__._cast(
            _7379.PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def ring_pins_to_disc_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7386.RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7386,
        )

        return self.__parent__._cast(
            _7386.RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7389.RollingRingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7389,
        )

        return self.__parent__._cast(
            _7389.RollingRingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_to_mountable_component_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7393.ShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7393,
        )

        return self.__parent__._cast(
            _7393.ShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7396.SpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7396,
        )

        return self.__parent__._cast(
            _7396.SpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> (
        "_7399.SpringDamperConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7399,
        )

        return self.__parent__._cast(
            _7399.SpringDamperConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7402.StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7402,
        )

        return self.__parent__._cast(
            _7402.StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7405.StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7405,
        )

        return self.__parent__._cast(
            _7405.StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7414.TorqueConverterConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7414,
        )

        return self.__parent__._cast(
            _7414.TorqueConverterConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7420.WormGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7420,
        )

        return self.__parent__._cast(
            _7420.WormGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7423.ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7423,
        )

        return self.__parent__._cast(
            _7423.ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7566.AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7566,
        )

        return self.__parent__._cast(
            _7566.AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7568.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7568,
        )

        return self.__parent__._cast(
            _7568.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def belt_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7572.BeltConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7572,
        )

        return self.__parent__._cast(
            _7572.BeltConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_differential_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7575.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7575,
        )

        return self.__parent__._cast(
            _7575.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7580.BevelGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7580,
        )

        return self.__parent__._cast(
            _7580.BevelGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def clutch_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7585.ClutchConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7585,
        )

        return self.__parent__._cast(
            _7585.ClutchConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def coaxial_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7587.CoaxialConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7587,
        )

        return self.__parent__._cast(
            _7587.CoaxialConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def concept_coupling_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7590.ConceptCouplingConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7590,
        )

        return self.__parent__._cast(
            _7590.ConceptCouplingConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def concept_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7593.ConceptGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7593,
        )

        return self.__parent__._cast(
            _7593.ConceptGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def conical_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7596.ConicalGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7596,
        )

        return self.__parent__._cast(
            _7596.ConicalGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7598.ConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7598,
        )

        return self.__parent__._cast(_7598.ConnectionCompoundAdvancedSystemDeflection)

    @property
    def coupling_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7601.CouplingConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7601,
        )

        return self.__parent__._cast(
            _7601.CouplingConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def cvt_belt_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7603.CVTBeltConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7603,
        )

        return self.__parent__._cast(
            _7603.CVTBeltConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7607.CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7607,
        )

        return self.__parent__._cast(
            _7607.CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> (
        "_7609.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7609,
        )

        return self.__parent__._cast(
            _7609.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def cylindrical_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7611.CylindricalGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7611,
        )

        return self.__parent__._cast(
            _7611.CylindricalGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def face_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7617.FaceGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7617,
        )

        return self.__parent__._cast(_7617.FaceGearMeshCompoundAdvancedSystemDeflection)

    @property
    def gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7622.GearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7622,
        )

        return self.__parent__._cast(_7622.GearMeshCompoundAdvancedSystemDeflection)

    @property
    def hypoid_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7626.HypoidGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7626,
        )

        return self.__parent__._cast(
            _7626.HypoidGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def inter_mountable_component_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7628.InterMountableComponentConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7628,
        )

        return self.__parent__._cast(
            _7628.InterMountableComponentConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> (
        "_7630.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7630,
        )

        return self.__parent__._cast(
            _7630.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7633.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7633,
        )

        return self.__parent__._cast(
            _7633.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7636.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7636,
        )

        return self.__parent__._cast(
            _7636.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7646.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7646,
        )

        return self.__parent__._cast(
            _7646.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def planetary_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7648.PlanetaryConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7648,
        )

        return self.__parent__._cast(
            _7648.PlanetaryConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def ring_pins_to_disc_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7655.RingPinsToDiscConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7655,
        )

        return self.__parent__._cast(
            _7655.RingPinsToDiscConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def rolling_ring_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7658.RollingRingConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7658,
        )

        return self.__parent__._cast(
            _7658.RollingRingConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def shaft_to_mountable_component_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7662.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7662,
        )

        return self.__parent__._cast(
            _7662.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7665.SpiralBevelGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7665,
        )

        return self.__parent__._cast(
            _7665.SpiralBevelGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def spring_damper_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7668.SpringDamperConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7668,
        )

        return self.__parent__._cast(
            _7668.SpringDamperConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7671.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7671,
        )

        return self.__parent__._cast(
            _7671.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7674.StraightBevelGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7674,
        )

        return self.__parent__._cast(
            _7674.StraightBevelGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def torque_converter_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7683.TorqueConverterConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7683,
        )

        return self.__parent__._cast(
            _7683.TorqueConverterConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def worm_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7689.WormGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7689,
        )

        return self.__parent__._cast(_7689.WormGearMeshCompoundAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7692.ZerolBevelGearMeshCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7692,
        )

        return self.__parent__._cast(
            _7692.ZerolBevelGearMeshCompoundAdvancedSystemDeflection
        )

    @property
    def connection_compound_analysis(self: "CastSelf") -> "ConnectionCompoundAnalysis":
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
class ConnectionCompoundAnalysis(_7714.DesignEntityCompoundAnalysis):
    """ConnectionCompoundAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_COMPOUND_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionCompoundAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCompoundAnalysis
        """
        return _Cast_ConnectionCompoundAnalysis(self)
