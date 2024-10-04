"""ConnectionCompoundParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7710

_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "ConnectionCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4441,
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
    from mastapy._private.utility_gui import _1903

    Self = TypeVar("Self", bound="ConnectionCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionCompoundParametricStudyTool._Cast_ConnectionCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCompoundParametricStudyTool:
    """Special nested class for casting ConnectionCompoundParametricStudyTool to subclasses."""

    __parent__: "ConnectionCompoundParametricStudyTool"

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
    def connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "ConnectionCompoundParametricStudyTool":
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
class ConnectionCompoundParametricStudyTool(_7710.ConnectionCompoundAnalysis):
    """ConnectionCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def data_logger(self: "Self") -> "_1903.DataLoggerWithCharts":
        """mastapy.utility_gui.DataLoggerWithCharts

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DataLogger")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4441.ConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectionParametricStudyTool]

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
    ) -> "List[_4441.ConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectionParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_ConnectionCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCompoundParametricStudyTool
        """
        return _Cast_ConnectionCompoundParametricStudyTool(self)
