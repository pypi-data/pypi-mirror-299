"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results._2705 import (
        CompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2706 import SingleAnalysis
    from mastapy._private.system_model.analyses_and_results._2707 import (
        AdvancedSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2708 import (
        AdvancedSystemDeflectionSubAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2709 import (
        AdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2710 import (
        CompoundParametricStudyToolAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2711 import (
        CriticalSpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2712 import DynamicAnalysis
    from mastapy._private.system_model.analyses_and_results._2713 import (
        DynamicModelAtAStiffnessAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2714 import (
        DynamicModelForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2715 import (
        DynamicModelForModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2716 import (
        DynamicModelForStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2717 import (
        DynamicModelForSteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2718 import (
        HarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2719 import (
        HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2720 import (
        HarmonicAnalysisOfSingleExcitationAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2721 import ModalAnalysis
    from mastapy._private.system_model.analyses_and_results._2722 import (
        ModalAnalysisAtASpeed,
    )
    from mastapy._private.system_model.analyses_and_results._2723 import (
        ModalAnalysisAtAStiffness,
    )
    from mastapy._private.system_model.analyses_and_results._2724 import (
        ModalAnalysisForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2725 import (
        MultibodyDynamicsAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2726 import (
        ParametricStudyToolAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2727 import (
        PowerFlowAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2728 import (
        StabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2729 import (
        SteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2730 import (
        SteadyStateSynchronousResponseAtASpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2731 import (
        SteadyStateSynchronousResponseOnAShaftAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2732 import (
        SystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2733 import (
        TorsionalSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2734 import (
        AnalysisCaseVariable,
    )
    from mastapy._private.system_model.analyses_and_results._2735 import (
        ConnectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2736 import Context
    from mastapy._private.system_model.analyses_and_results._2737 import (
        DesignEntityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2738 import (
        DesignEntityGroupAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2739 import (
        DesignEntitySingleContextAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2743 import PartAnalysis
    from mastapy._private.system_model.analyses_and_results._2744 import (
        CompoundAdvancedSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2745 import (
        CompoundAdvancedSystemDeflectionSubAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2746 import (
        CompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2747 import (
        CompoundCriticalSpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2748 import (
        CompoundDynamicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2749 import (
        CompoundDynamicModelAtAStiffnessAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2750 import (
        CompoundDynamicModelForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2751 import (
        CompoundDynamicModelForModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2752 import (
        CompoundDynamicModelForStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2753 import (
        CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2754 import (
        CompoundHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2755 import (
        CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2756 import (
        CompoundHarmonicAnalysisOfSingleExcitationAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2757 import (
        CompoundModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2758 import (
        CompoundModalAnalysisAtASpeed,
    )
    from mastapy._private.system_model.analyses_and_results._2759 import (
        CompoundModalAnalysisAtAStiffness,
    )
    from mastapy._private.system_model.analyses_and_results._2760 import (
        CompoundModalAnalysisForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2761 import (
        CompoundMultibodyDynamicsAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2762 import (
        CompoundPowerFlowAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2763 import (
        CompoundStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2764 import (
        CompoundSteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2765 import (
        CompoundSteadyStateSynchronousResponseAtASpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2766 import (
        CompoundSteadyStateSynchronousResponseOnAShaftAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2767 import (
        CompoundSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2768 import (
        CompoundTorsionalSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2769 import (
        TESetUpForDynamicAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results._2770 import TimeOptions
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results._2705": ["CompoundAnalysis"],
        "_private.system_model.analyses_and_results._2706": ["SingleAnalysis"],
        "_private.system_model.analyses_and_results._2707": [
            "AdvancedSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2708": [
            "AdvancedSystemDeflectionSubAnalysis"
        ],
        "_private.system_model.analyses_and_results._2709": [
            "AdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2710": [
            "CompoundParametricStudyToolAnalysis"
        ],
        "_private.system_model.analyses_and_results._2711": ["CriticalSpeedAnalysis"],
        "_private.system_model.analyses_and_results._2712": ["DynamicAnalysis"],
        "_private.system_model.analyses_and_results._2713": [
            "DynamicModelAtAStiffnessAnalysis"
        ],
        "_private.system_model.analyses_and_results._2714": [
            "DynamicModelForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2715": [
            "DynamicModelForModalAnalysis"
        ],
        "_private.system_model.analyses_and_results._2716": [
            "DynamicModelForStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2717": [
            "DynamicModelForSteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2718": ["HarmonicAnalysis"],
        "_private.system_model.analyses_and_results._2719": [
            "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2720": [
            "HarmonicAnalysisOfSingleExcitationAnalysis"
        ],
        "_private.system_model.analyses_and_results._2721": ["ModalAnalysis"],
        "_private.system_model.analyses_and_results._2722": ["ModalAnalysisAtASpeed"],
        "_private.system_model.analyses_and_results._2723": [
            "ModalAnalysisAtAStiffness"
        ],
        "_private.system_model.analyses_and_results._2724": [
            "ModalAnalysisForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2725": [
            "MultibodyDynamicsAnalysis"
        ],
        "_private.system_model.analyses_and_results._2726": [
            "ParametricStudyToolAnalysis"
        ],
        "_private.system_model.analyses_and_results._2727": ["PowerFlowAnalysis"],
        "_private.system_model.analyses_and_results._2728": ["StabilityAnalysis"],
        "_private.system_model.analyses_and_results._2729": [
            "SteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2730": [
            "SteadyStateSynchronousResponseAtASpeedAnalysis"
        ],
        "_private.system_model.analyses_and_results._2731": [
            "SteadyStateSynchronousResponseOnAShaftAnalysis"
        ],
        "_private.system_model.analyses_and_results._2732": [
            "SystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2733": [
            "TorsionalSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2734": ["AnalysisCaseVariable"],
        "_private.system_model.analyses_and_results._2735": ["ConnectionAnalysis"],
        "_private.system_model.analyses_and_results._2736": ["Context"],
        "_private.system_model.analyses_and_results._2737": ["DesignEntityAnalysis"],
        "_private.system_model.analyses_and_results._2738": [
            "DesignEntityGroupAnalysis"
        ],
        "_private.system_model.analyses_and_results._2739": [
            "DesignEntitySingleContextAnalysis"
        ],
        "_private.system_model.analyses_and_results._2743": ["PartAnalysis"],
        "_private.system_model.analyses_and_results._2744": [
            "CompoundAdvancedSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2745": [
            "CompoundAdvancedSystemDeflectionSubAnalysis"
        ],
        "_private.system_model.analyses_and_results._2746": [
            "CompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2747": [
            "CompoundCriticalSpeedAnalysis"
        ],
        "_private.system_model.analyses_and_results._2748": ["CompoundDynamicAnalysis"],
        "_private.system_model.analyses_and_results._2749": [
            "CompoundDynamicModelAtAStiffnessAnalysis"
        ],
        "_private.system_model.analyses_and_results._2750": [
            "CompoundDynamicModelForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2751": [
            "CompoundDynamicModelForModalAnalysis"
        ],
        "_private.system_model.analyses_and_results._2752": [
            "CompoundDynamicModelForStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2753": [
            "CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2754": [
            "CompoundHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2755": [
            "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2756": [
            "CompoundHarmonicAnalysisOfSingleExcitationAnalysis"
        ],
        "_private.system_model.analyses_and_results._2757": ["CompoundModalAnalysis"],
        "_private.system_model.analyses_and_results._2758": [
            "CompoundModalAnalysisAtASpeed"
        ],
        "_private.system_model.analyses_and_results._2759": [
            "CompoundModalAnalysisAtAStiffness"
        ],
        "_private.system_model.analyses_and_results._2760": [
            "CompoundModalAnalysisForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2761": [
            "CompoundMultibodyDynamicsAnalysis"
        ],
        "_private.system_model.analyses_and_results._2762": [
            "CompoundPowerFlowAnalysis"
        ],
        "_private.system_model.analyses_and_results._2763": [
            "CompoundStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2764": [
            "CompoundSteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2765": [
            "CompoundSteadyStateSynchronousResponseAtASpeedAnalysis"
        ],
        "_private.system_model.analyses_and_results._2766": [
            "CompoundSteadyStateSynchronousResponseOnAShaftAnalysis"
        ],
        "_private.system_model.analyses_and_results._2767": [
            "CompoundSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2768": [
            "CompoundTorsionalSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2769": [
            "TESetUpForDynamicAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results._2770": ["TimeOptions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CompoundAnalysis",
    "SingleAnalysis",
    "AdvancedSystemDeflectionAnalysis",
    "AdvancedSystemDeflectionSubAnalysis",
    "AdvancedTimeSteppingAnalysisForModulation",
    "CompoundParametricStudyToolAnalysis",
    "CriticalSpeedAnalysis",
    "DynamicAnalysis",
    "DynamicModelAtAStiffnessAnalysis",
    "DynamicModelForHarmonicAnalysis",
    "DynamicModelForModalAnalysis",
    "DynamicModelForStabilityAnalysis",
    "DynamicModelForSteadyStateSynchronousResponseAnalysis",
    "HarmonicAnalysis",
    "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    "HarmonicAnalysisOfSingleExcitationAnalysis",
    "ModalAnalysis",
    "ModalAnalysisAtASpeed",
    "ModalAnalysisAtAStiffness",
    "ModalAnalysisForHarmonicAnalysis",
    "MultibodyDynamicsAnalysis",
    "ParametricStudyToolAnalysis",
    "PowerFlowAnalysis",
    "StabilityAnalysis",
    "SteadyStateSynchronousResponseAnalysis",
    "SteadyStateSynchronousResponseAtASpeedAnalysis",
    "SteadyStateSynchronousResponseOnAShaftAnalysis",
    "SystemDeflectionAnalysis",
    "TorsionalSystemDeflectionAnalysis",
    "AnalysisCaseVariable",
    "ConnectionAnalysis",
    "Context",
    "DesignEntityAnalysis",
    "DesignEntityGroupAnalysis",
    "DesignEntitySingleContextAnalysis",
    "PartAnalysis",
    "CompoundAdvancedSystemDeflectionAnalysis",
    "CompoundAdvancedSystemDeflectionSubAnalysis",
    "CompoundAdvancedTimeSteppingAnalysisForModulation",
    "CompoundCriticalSpeedAnalysis",
    "CompoundDynamicAnalysis",
    "CompoundDynamicModelAtAStiffnessAnalysis",
    "CompoundDynamicModelForHarmonicAnalysis",
    "CompoundDynamicModelForModalAnalysis",
    "CompoundDynamicModelForStabilityAnalysis",
    "CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis",
    "CompoundHarmonicAnalysis",
    "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    "CompoundHarmonicAnalysisOfSingleExcitationAnalysis",
    "CompoundModalAnalysis",
    "CompoundModalAnalysisAtASpeed",
    "CompoundModalAnalysisAtAStiffness",
    "CompoundModalAnalysisForHarmonicAnalysis",
    "CompoundMultibodyDynamicsAnalysis",
    "CompoundPowerFlowAnalysis",
    "CompoundStabilityAnalysis",
    "CompoundSteadyStateSynchronousResponseAnalysis",
    "CompoundSteadyStateSynchronousResponseAtASpeedAnalysis",
    "CompoundSteadyStateSynchronousResponseOnAShaftAnalysis",
    "CompoundSystemDeflectionAnalysis",
    "CompoundTorsionalSystemDeflectionAnalysis",
    "TESetUpForDynamicAnalysisOptions",
    "TimeOptions",
)
