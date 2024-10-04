"""ConnectionCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7710

_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "ConnectionCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6723,
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

    Self = TypeVar("Self", bound="ConnectionCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionCompoundCriticalSpeedAnalysis._Cast_ConnectionCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCompoundCriticalSpeedAnalysis:
    """Special nested class for casting ConnectionCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "ConnectionCompoundCriticalSpeedAnalysis"

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7710.ConnectionCompoundAnalysis":
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
    def connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "ConnectionCompoundCriticalSpeedAnalysis":
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
class ConnectionCompoundCriticalSpeedAnalysis(_7710.ConnectionCompoundAnalysis):
    """ConnectionCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6723.ConnectionCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.ConnectionCriticalSpeedAnalysis]

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
    ) -> "List[_6723.ConnectionCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.ConnectionCriticalSpeedAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ConnectionCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCompoundCriticalSpeedAnalysis
        """
        return _Cast_ConnectionCompoundCriticalSpeedAnalysis(self)
