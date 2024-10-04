"""CylindricalGearMeshSystemDeflectionWithLTCAResults"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2825

_CYLINDRICAL_GEAR_MESH_SYSTEM_DEFLECTION_WITH_LTCA_RESULTS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "CylindricalGearMeshSystemDeflectionWithLTCAResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca.cylindrical import _882
    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2739
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7709,
        _7711,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2813,
        _2845,
        _2853,
    )

    Self = TypeVar("Self", bound="CylindricalGearMeshSystemDeflectionWithLTCAResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshSystemDeflectionWithLTCAResults._Cast_CylindricalGearMeshSystemDeflectionWithLTCAResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshSystemDeflectionWithLTCAResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshSystemDeflectionWithLTCAResults:
    """Special nested class for casting CylindricalGearMeshSystemDeflectionWithLTCAResults to subclasses."""

    __parent__: "CylindricalGearMeshSystemDeflectionWithLTCAResults"

    @property
    def cylindrical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2825.CylindricalGearMeshSystemDeflection":
        return self.__parent__._cast(_2825.CylindricalGearMeshSystemDeflection)

    @property
    def gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2845.GearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2845,
        )

        return self.__parent__._cast(_2845.GearMeshSystemDeflection)

    @property
    def inter_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2853.InterMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2853,
        )

        return self.__parent__._cast(
            _2853.InterMountableComponentConnectionSystemDeflection
        )

    @property
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2813.ConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2813,
        )

        return self.__parent__._cast(_2813.ConnectionSystemDeflection)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7711.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7711,
        )

        return self.__parent__._cast(_7711.ConnectionFEAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7712.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7709.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7709,
        )

        return self.__parent__._cast(_7709.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2735.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.ConnectionAnalysis)

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
    def cylindrical_gear_mesh_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "CylindricalGearMeshSystemDeflectionWithLTCAResults":
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
class CylindricalGearMeshSystemDeflectionWithLTCAResults(
    _2825.CylindricalGearMeshSystemDeflection
):
    """CylindricalGearMeshSystemDeflectionWithLTCAResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_SYSTEM_DEFLECTION_WITH_LTCA_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def advanced_ltca_results(
        self: "Self",
    ) -> "_882.CylindricalGearMeshLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdvancedLTCAResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def advanced_ltca_results_only_first_planetary_mesh(
        self: "Self",
    ) -> "_882.CylindricalGearMeshLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AdvancedLTCAResultsOnlyFirstPlanetaryMesh"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def basic_ltca_results(
        self: "Self",
    ) -> "_882.CylindricalGearMeshLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicLTCAResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def basic_ltca_results_only_first_planetary_mesh(
        self: "Self",
    ) -> "_882.CylindricalGearMeshLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicLTCAResultsOnlyFirstPlanetaryMesh"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CylindricalGearMeshSystemDeflectionWithLTCAResults":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshSystemDeflectionWithLTCAResults
        """
        return _Cast_CylindricalGearMeshSystemDeflectionWithLTCAResults(self)
