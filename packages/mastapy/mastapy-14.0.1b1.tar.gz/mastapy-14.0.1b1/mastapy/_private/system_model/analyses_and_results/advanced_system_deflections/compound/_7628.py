"""InterMountableComponentConnectionCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7598,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "InterMountableComponentConnectionCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7495,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7568,
        _7572,
        _7575,
        _7580,
        _7585,
        _7590,
        _7593,
        _7596,
        _7601,
        _7603,
        _7611,
        _7617,
        _7622,
        _7626,
        _7630,
        _7633,
        _7636,
        _7646,
        _7655,
        _7658,
        _7665,
        _7668,
        _7671,
        _7674,
        _7683,
        _7689,
        _7692,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7714,
    )

    Self = TypeVar(
        "Self",
        bound="InterMountableComponentConnectionCompoundAdvancedSystemDeflection",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundAdvancedSystemDeflection._Cast_InterMountableComponentConnectionCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundAdvancedSystemDeflection:
    """Special nested class for casting InterMountableComponentConnectionCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "InterMountableComponentConnectionCompoundAdvancedSystemDeflection"

    @property
    def connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7598.ConnectionCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(_7598.ConnectionCompoundAdvancedSystemDeflection)

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
    def inter_mountable_component_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundAdvancedSystemDeflection":
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
class InterMountableComponentConnectionCompoundAdvancedSystemDeflection(
    _7598.ConnectionCompoundAdvancedSystemDeflection
):
    """InterMountableComponentConnectionCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
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
    ) -> "List[_7495.InterMountableComponentConnectionAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.InterMountableComponentConnectionAdvancedSystemDeflection]

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
    ) -> "List[_7495.InterMountableComponentConnectionAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.InterMountableComponentConnectionAdvancedSystemDeflection]

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
    ) -> "_Cast_InterMountableComponentConnectionCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundAdvancedSystemDeflection
        """
        return _Cast_InterMountableComponentConnectionCompoundAdvancedSystemDeflection(
            self
        )
