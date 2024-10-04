"""PartHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7719

_PART_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "PartHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737, _2739, _2743
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7716
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5899,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6145,
        _6146,
        _6147,
        _6149,
        _6151,
        _6152,
        _6153,
        _6155,
        _6156,
        _6158,
        _6159,
        _6160,
        _6161,
        _6163,
        _6164,
        _6165,
        _6167,
        _6168,
        _6170,
        _6172,
        _6173,
        _6174,
        _6176,
        _6177,
        _6179,
        _6181,
        _6183,
        _6184,
        _6186,
        _6187,
        _6188,
        _6190,
        _6192,
        _6194,
        _6195,
        _6196,
        _6197,
        _6198,
        _6200,
        _6201,
        _6202,
        _6203,
        _6205,
        _6206,
        _6207,
        _6208,
        _6210,
        _6212,
        _6214,
        _6215,
        _6217,
        _6218,
        _6220,
        _6221,
        _6222,
        _6223,
        _6224,
        _6226,
        _6227,
        _6230,
        _6231,
        _6233,
        _6234,
        _6235,
        _6236,
        _6237,
        _6238,
        _6240,
        _6242,
        _6243,
        _6244,
        _6245,
        _6247,
        _6248,
        _6250,
        _6252,
        _6253,
        _6254,
        _6256,
        _6257,
        _6259,
        _6260,
        _6261,
        _6262,
        _6263,
        _6264,
        _6265,
        _6267,
        _6268,
        _6269,
        _6270,
        _6271,
        _6272,
        _6274,
        _6275,
        _6277,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4778
    from mastapy._private.system_model.part_model import _2526

    Self = TypeVar("Self", bound="PartHarmonicAnalysisOfSingleExcitation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartHarmonicAnalysisOfSingleExcitation._Cast_PartHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting PartHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "PartHarmonicAnalysisOfSingleExcitation"

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7719.PartStaticLoadAnalysisCase":
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
    def abstract_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6145.AbstractAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6145,
        )

        return self.__parent__._cast(
            _6145.AbstractAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6146.AbstractShaftHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6146,
        )

        return self.__parent__._cast(
            _6146.AbstractShaftHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_or_housing_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6147.AbstractShaftOrHousingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6147,
        )

        return self.__parent__._cast(
            _6147.AbstractShaftOrHousingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6149.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6149,
        )

        return self.__parent__._cast(
            _6149.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6151.AGMAGleasonConicalGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6151,
        )

        return self.__parent__._cast(
            _6151.AGMAGleasonConicalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6152.AssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6152,
        )

        return self.__parent__._cast(_6152.AssemblyHarmonicAnalysisOfSingleExcitation)

    @property
    def bearing_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6153.BearingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6153,
        )

        return self.__parent__._cast(_6153.BearingHarmonicAnalysisOfSingleExcitation)

    @property
    def belt_drive_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6155.BeltDriveHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6155,
        )

        return self.__parent__._cast(_6155.BeltDriveHarmonicAnalysisOfSingleExcitation)

    @property
    def bevel_differential_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6156.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6156,
        )

        return self.__parent__._cast(
            _6156.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6158.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6158,
        )

        return self.__parent__._cast(
            _6158.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6159.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6159,
        )

        return self.__parent__._cast(
            _6159.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_sun_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6160.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6160,
        )

        return self.__parent__._cast(
            _6160.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6161.BevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6161,
        )

        return self.__parent__._cast(_6161.BevelGearHarmonicAnalysisOfSingleExcitation)

    @property
    def bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6163.BevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6163,
        )

        return self.__parent__._cast(
            _6163.BevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bolted_joint_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6164.BoltedJointHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6164,
        )

        return self.__parent__._cast(
            _6164.BoltedJointHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bolt_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6165.BoltHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6165,
        )

        return self.__parent__._cast(_6165.BoltHarmonicAnalysisOfSingleExcitation)

    @property
    def clutch_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6167.ClutchHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6167,
        )

        return self.__parent__._cast(_6167.ClutchHalfHarmonicAnalysisOfSingleExcitation)

    @property
    def clutch_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6168.ClutchHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6168,
        )

        return self.__parent__._cast(_6168.ClutchHarmonicAnalysisOfSingleExcitation)

    @property
    def component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6170.ComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6170,
        )

        return self.__parent__._cast(_6170.ComponentHarmonicAnalysisOfSingleExcitation)

    @property
    def concept_coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6172.ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6172,
        )

        return self.__parent__._cast(
            _6172.ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6173.ConceptCouplingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6173,
        )

        return self.__parent__._cast(
            _6173.ConceptCouplingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6174.ConceptGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6174,
        )

        return self.__parent__._cast(
            _6174.ConceptGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6176.ConceptGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6176,
        )

        return self.__parent__._cast(
            _6176.ConceptGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6177.ConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6177,
        )

        return self.__parent__._cast(
            _6177.ConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6179.ConicalGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6179,
        )

        return self.__parent__._cast(
            _6179.ConicalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def connector_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6181.ConnectorHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6181,
        )

        return self.__parent__._cast(_6181.ConnectorHarmonicAnalysisOfSingleExcitation)

    @property
    def coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6183.CouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6183,
        )

        return self.__parent__._cast(
            _6183.CouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6184.CouplingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6184,
        )

        return self.__parent__._cast(_6184.CouplingHarmonicAnalysisOfSingleExcitation)

    @property
    def cvt_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6186.CVTHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6186,
        )

        return self.__parent__._cast(_6186.CVTHarmonicAnalysisOfSingleExcitation)

    @property
    def cvt_pulley_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6187.CVTPulleyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6187,
        )

        return self.__parent__._cast(_6187.CVTPulleyHarmonicAnalysisOfSingleExcitation)

    @property
    def cycloidal_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6188.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6188,
        )

        return self.__parent__._cast(
            _6188.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6190.CycloidalDiscHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6190,
        )

        return self.__parent__._cast(
            _6190.CycloidalDiscHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6192.CylindricalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6192,
        )

        return self.__parent__._cast(
            _6192.CylindricalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6194.CylindricalGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6194,
        )

        return self.__parent__._cast(
            _6194.CylindricalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6195.CylindricalPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6195,
        )

        return self.__parent__._cast(
            _6195.CylindricalPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def datum_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6196.DatumHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6196,
        )

        return self.__parent__._cast(_6196.DatumHarmonicAnalysisOfSingleExcitation)

    @property
    def external_cad_model_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6197.ExternalCADModelHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6197,
        )

        return self.__parent__._cast(
            _6197.ExternalCADModelHarmonicAnalysisOfSingleExcitation
        )

    @property
    def face_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6198.FaceGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6198,
        )

        return self.__parent__._cast(_6198.FaceGearHarmonicAnalysisOfSingleExcitation)

    @property
    def face_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6200.FaceGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6200,
        )

        return self.__parent__._cast(
            _6200.FaceGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def fe_part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6201.FEPartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6201,
        )

        return self.__parent__._cast(_6201.FEPartHarmonicAnalysisOfSingleExcitation)

    @property
    def flexible_pin_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6202.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6202,
        )

        return self.__parent__._cast(
            _6202.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6203.GearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6203,
        )

        return self.__parent__._cast(_6203.GearHarmonicAnalysisOfSingleExcitation)

    @property
    def gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6205.GearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6205,
        )

        return self.__parent__._cast(_6205.GearSetHarmonicAnalysisOfSingleExcitation)

    @property
    def guide_dxf_model_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6206.GuideDxfModelHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6206,
        )

        return self.__parent__._cast(
            _6206.GuideDxfModelHarmonicAnalysisOfSingleExcitation
        )

    @property
    def hypoid_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6208.HypoidGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6208,
        )

        return self.__parent__._cast(_6208.HypoidGearHarmonicAnalysisOfSingleExcitation)

    @property
    def hypoid_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6210.HypoidGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6210,
        )

        return self.__parent__._cast(
            _6210.HypoidGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6212.KlingelnbergCycloPalloidConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6212,
        )

        return self.__parent__._cast(
            _6212.KlingelnbergCycloPalloidConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> (
        "_6214.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysisOfSingleExcitation"
    ):
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6214,
        )

        return self.__parent__._cast(
            _6214.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6215.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6215,
        )

        return self.__parent__._cast(
            _6215.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> (
        "_6217.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation"
    ):
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6217,
        )

        return self.__parent__._cast(
            _6217.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6218.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6218,
        )

        return self.__parent__._cast(
            _6218.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6220.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6220,
        )

        return self.__parent__._cast(
            _6220.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def mass_disc_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6221.MassDiscHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6221,
        )

        return self.__parent__._cast(_6221.MassDiscHarmonicAnalysisOfSingleExcitation)

    @property
    def measurement_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6222.MeasurementComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6222,
        )

        return self.__parent__._cast(
            _6222.MeasurementComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def microphone_array_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6223.MicrophoneArrayHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6223,
        )

        return self.__parent__._cast(
            _6223.MicrophoneArrayHarmonicAnalysisOfSingleExcitation
        )

    @property
    def microphone_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6224.MicrophoneHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6224,
        )

        return self.__parent__._cast(_6224.MicrophoneHarmonicAnalysisOfSingleExcitation)

    @property
    def mountable_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6226.MountableComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6226,
        )

        return self.__parent__._cast(
            _6226.MountableComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def oil_seal_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6227.OilSealHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6227,
        )

        return self.__parent__._cast(_6227.OilSealHarmonicAnalysisOfSingleExcitation)

    @property
    def part_to_part_shear_coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6230.PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6230,
        )

        return self.__parent__._cast(
            _6230.PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_to_part_shear_coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6231.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6231,
        )

        return self.__parent__._cast(
            _6231.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planetary_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6233.PlanetaryGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6233,
        )

        return self.__parent__._cast(
            _6233.PlanetaryGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planet_carrier_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6234.PlanetCarrierHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6234,
        )

        return self.__parent__._cast(
            _6234.PlanetCarrierHarmonicAnalysisOfSingleExcitation
        )

    @property
    def point_load_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6235.PointLoadHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6235,
        )

        return self.__parent__._cast(_6235.PointLoadHarmonicAnalysisOfSingleExcitation)

    @property
    def power_load_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6236.PowerLoadHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6236,
        )

        return self.__parent__._cast(_6236.PowerLoadHarmonicAnalysisOfSingleExcitation)

    @property
    def pulley_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6237.PulleyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6237,
        )

        return self.__parent__._cast(_6237.PulleyHarmonicAnalysisOfSingleExcitation)

    @property
    def ring_pins_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6238.RingPinsHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6238,
        )

        return self.__parent__._cast(_6238.RingPinsHarmonicAnalysisOfSingleExcitation)

    @property
    def rolling_ring_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6240.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6240,
        )

        return self.__parent__._cast(
            _6240.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def rolling_ring_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6242.RollingRingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6242,
        )

        return self.__parent__._cast(
            _6242.RollingRingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def root_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6243.RootAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6243,
        )

        return self.__parent__._cast(
            _6243.RootAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def shaft_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6244.ShaftHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6244,
        )

        return self.__parent__._cast(_6244.ShaftHarmonicAnalysisOfSingleExcitation)

    @property
    def shaft_hub_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6245.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6245,
        )

        return self.__parent__._cast(
            _6245.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def specialised_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6247.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6247,
        )

        return self.__parent__._cast(
            _6247.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6248.SpiralBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6248,
        )

        return self.__parent__._cast(
            _6248.SpiralBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6250.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6250,
        )

        return self.__parent__._cast(
            _6250.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6252.SpringDamperHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6252,
        )

        return self.__parent__._cast(
            _6252.SpringDamperHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6253.SpringDamperHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6253,
        )

        return self.__parent__._cast(
            _6253.SpringDamperHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6254.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6254,
        )

        return self.__parent__._cast(
            _6254.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6256.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6256,
        )

        return self.__parent__._cast(
            _6256.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6257.StraightBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6257,
        )

        return self.__parent__._cast(
            _6257.StraightBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6259.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6259,
        )

        return self.__parent__._cast(
            _6259.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6260.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6260,
        )

        return self.__parent__._cast(
            _6260.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_sun_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6261.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6261,
        )

        return self.__parent__._cast(
            _6261.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6262.SynchroniserHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6262,
        )

        return self.__parent__._cast(
            _6262.SynchroniserHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6263.SynchroniserHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6263,
        )

        return self.__parent__._cast(
            _6263.SynchroniserHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6264.SynchroniserPartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6264,
        )

        return self.__parent__._cast(
            _6264.SynchroniserPartHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_sleeve_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6265.SynchroniserSleeveHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6265,
        )

        return self.__parent__._cast(
            _6265.SynchroniserSleeveHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6267.TorqueConverterHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6267,
        )

        return self.__parent__._cast(
            _6267.TorqueConverterHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_pump_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6268.TorqueConverterPumpHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6268,
        )

        return self.__parent__._cast(
            _6268.TorqueConverterPumpHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_turbine_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6269.TorqueConverterTurbineHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6269,
        )

        return self.__parent__._cast(
            _6269.TorqueConverterTurbineHarmonicAnalysisOfSingleExcitation
        )

    @property
    def unbalanced_mass_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6270.UnbalancedMassHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6270,
        )

        return self.__parent__._cast(
            _6270.UnbalancedMassHarmonicAnalysisOfSingleExcitation
        )

    @property
    def virtual_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6271.VirtualComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6271,
        )

        return self.__parent__._cast(
            _6271.VirtualComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def worm_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6272.WormGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6272,
        )

        return self.__parent__._cast(_6272.WormGearHarmonicAnalysisOfSingleExcitation)

    @property
    def worm_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6274.WormGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6274,
        )

        return self.__parent__._cast(
            _6274.WormGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6275.ZerolBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6275,
        )

        return self.__parent__._cast(
            _6275.ZerolBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6277.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6277,
        )

        return self.__parent__._cast(
            _6277.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "PartHarmonicAnalysisOfSingleExcitation":
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
class PartHarmonicAnalysisOfSingleExcitation(_7719.PartStaticLoadAnalysisCase):
    """PartHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2526.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analysis_options(self: "Self") -> "_5899.HarmonicAnalysisOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analysis_of_single_excitation(
        self: "Self",
    ) -> "_6207.HarmonicAnalysisOfSingleExcitation":
        """mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.HarmonicAnalysisOfSingleExcitation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HarmonicAnalysisOfSingleExcitation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def uncoupled_modal_analysis(self: "Self") -> "_4778.PartModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PartModalAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UncoupledModalAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PartHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_PartHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_PartHarmonicAnalysisOfSingleExcitation(self)
