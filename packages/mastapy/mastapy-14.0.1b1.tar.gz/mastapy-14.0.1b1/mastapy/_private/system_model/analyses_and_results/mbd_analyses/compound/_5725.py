"""InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
    _5695,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
        "InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7714,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5576
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5665,
        _5669,
        _5672,
        _5677,
        _5682,
        _5687,
        _5690,
        _5693,
        _5698,
        _5700,
        _5708,
        _5714,
        _5719,
        _5723,
        _5727,
        _5730,
        _5733,
        _5743,
        _5752,
        _5755,
        _5762,
        _5765,
        _5768,
        _5771,
        _5780,
        _5786,
        _5789,
    )

    Self = TypeVar(
        "Self",
        bound="InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis._Cast_InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis"

    @property
    def connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5695.ConnectionCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5695.ConnectionCompoundMultibodyDynamicsAnalysis)

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
    def inter_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
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
class InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis(
    _5695.ConnectionCompoundMultibodyDynamicsAnalysis
):
    """InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS
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
    ) -> "List[_5576.InterMountableComponentConnectionMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.InterMountableComponentConnectionMultibodyDynamicsAnalysis]

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
    ) -> "List[_5576.InterMountableComponentConnectionMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.InterMountableComponentConnectionMultibodyDynamicsAnalysis]

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
    ) -> "_Cast_InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis(
            self
        )
