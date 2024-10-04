"""ConnectionCompoundHarmonicAnalysisOfSingleExcitation"""

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

_CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound",
    "ConnectionCompoundHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6180,
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

    Self = TypeVar("Self", bound="ConnectionCompoundHarmonicAnalysisOfSingleExcitation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionCompoundHarmonicAnalysisOfSingleExcitation._Cast_ConnectionCompoundHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCompoundHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting ConnectionCompoundHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "ConnectionCompoundHarmonicAnalysisOfSingleExcitation"

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
    def connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "ConnectionCompoundHarmonicAnalysisOfSingleExcitation":
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
class ConnectionCompoundHarmonicAnalysisOfSingleExcitation(
    _7710.ConnectionCompoundAnalysis
):
    """ConnectionCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6180.ConnectionHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.ConnectionHarmonicAnalysisOfSingleExcitation]

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
    ) -> "List[_6180.ConnectionHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.ConnectionHarmonicAnalysisOfSingleExcitation]

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
    ) -> "_Cast_ConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCompoundHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_ConnectionCompoundHarmonicAnalysisOfSingleExcitation(self)
