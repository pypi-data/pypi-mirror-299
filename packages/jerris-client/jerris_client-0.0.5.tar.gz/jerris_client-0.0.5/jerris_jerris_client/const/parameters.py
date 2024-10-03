from jerris_jerris_client.const.globals import (
    TYPE_BOOLEAN,
    TYPE_INTEGER,
    TYPE_LIST,
    TYPE_STRING,
)
from jerris_jerris_client.const.typing import AnalyzeParameter

JERRIS_IMAGE_PARAMETER_APERTURE = "aperture"
JERRIS_IMAGE_PARAMETER_ARTIFICIAL_INTELLIGENCE_CREATION_PROBABILITY = (
    "artificial-intelligence-creation-probability"
)
JERRIS_IMAGE_PARAMETER_ASPECT_RATIO = "aspect-ratio"
JERRIS_IMAGE_PARAMETER_COLOR_HARMONY = "color-harmony"
JERRIS_IMAGE_PARAMETER_COLOR_MODE = "color-mode"
JERRIS_IMAGE_PARAMETER_COLOR_TEMPERATURE = "color-temperature"
JERRIS_IMAGE_PARAMETER_COMPOSITION_CONTRAST = "composition-contrast"
JERRIS_IMAGE_PARAMETER_CONTRAST = "contrast"
JERRIS_IMAGE_PARAMETER_CONTROL_MODE = "control-mode"
JERRIS_IMAGE_PARAMETER_DEPTH_OF_FIELD = "depth-of-field"
JERRIS_IMAGE_PARAMETER_DEVELOPMENT = "development"
JERRIS_IMAGE_PARAMETER_DIAGONAL_LEADING_LINES = "diagonal-leading-lines"
JERRIS_IMAGE_PARAMETER_DIGITAL_NOISE = "digital-noise"
JERRIS_IMAGE_PARAMETER_DIRECTIONAL_LIGHTING = "directional-lighting"
JERRIS_IMAGE_PARAMETER_DOUBLE_EXPOSURE = "double-exposure"
JERRIS_IMAGE_PARAMETER_DUST_VISIBILITY = "dust-visibility"
JERRIS_IMAGE_PARAMETER_EMOTIONAL_IMPACT = "emotional-impact"
JERRIS_IMAGE_PARAMETER_EXPOSURE = "exposure"
JERRIS_IMAGE_PARAMETER_FOCAL_DISTANCE = "focal-distance"
JERRIS_IMAGE_PARAMETER_FRAME_IN_A_FRAME = "frame-in-a-frame"
JERRIS_IMAGE_PARAMETER_FRAMING_VIEWER = "framing-viewer"
JERRIS_IMAGE_PARAMETER_GOLDEN_RECTANGLES = "golden-rectangles"
JERRIS_IMAGE_PARAMETER_GOLDEN_SPIRAL = "golden-spiral"
JERRIS_IMAGE_PARAMETER_GOLDEN_TRIANGLES = "golden-triangles"
JERRIS_IMAGE_PARAMETER_HAZE_PRESENCE = "haze-presence"
JERRIS_IMAGE_PARAMETER_HIGH_DYNAMIC_RANGE = "high-dynamic-range"
JERRIS_IMAGE_PARAMETER_HIGHLIGHT_TEXTURES_AND_DETAILS = "highlight-textures-and-details"
JERRIS_IMAGE_PARAMETER_HUE = "hue"
JERRIS_IMAGE_PARAMETER_IMAGE_REALISM = "image-realism"
JERRIS_IMAGE_PARAMETER_IMPLIED_LINES = "implied-lines"
JERRIS_IMAGE_PARAMETER_INTENDED_PURPOSE = "intended-purpose"
JERRIS_IMAGE_PARAMETER_ISO = "iso"
JERRIS_IMAGE_PARAMETER_LATITUDE = "latitude"
JERRIS_IMAGE_PARAMETER_LEADING_LINES = "leading-lines"
JERRIS_IMAGE_PARAMETER_LEADING_SPACE = "leading-space"
JERRIS_IMAGE_PARAMETER_LENS_FLARE = "lens-flare"
JERRIS_IMAGE_PARAMETER_LIGHT_REFLECTION = "light-reflection"
JERRIS_IMAGE_PARAMETER_LIGHT_SOFTNESS_VIEWER = "light-softness-viewer"
JERRIS_IMAGE_PARAMETER_LIGHT_SOURCE_VIEWER = "light-source-viewer"
JERRIS_IMAGE_PARAMETER_LIGHTING_QUALITY = "lighting-quality"
JERRIS_IMAGE_PARAMETER_LINE_DIRECTION = "line-direction"
JERRIS_IMAGE_PARAMETER_LOCATION_SETTING = "location-setting"
JERRIS_IMAGE_PARAMETER_LUMINOSITY = "luminosity"
JERRIS_IMAGE_PARAMETER_MINIMIZING_DISTRACTIONS = "minimizing-distractions"
JERRIS_IMAGE_PARAMETER_NEGATIVE_SPACE = "negative-space"
JERRIS_IMAGE_PARAMETER_OVERALL_AESTHETICS_ASSESSMENT = "overall-aesthetics-assessment"
JERRIS_IMAGE_PARAMETER_OVERALL_EXPERT_ASSESSMENT = "overall-expert-assessment"
JERRIS_IMAGE_PARAMETER_OVERALL_TECHNICAL_ASSESSMENT = "overall-technical-assessment"
JERRIS_IMAGE_PARAMETER_PATTERN_RECOGNITION = "pattern-recognition"
JERRIS_IMAGE_PARAMETER_PATTERN_REPETITION = "pattern-repetition"
JERRIS_IMAGE_PARAMETER_PERSPECTIVE_LINES = "perspective-lines"
JERRIS_IMAGE_PARAMETER_PERSPECTIVE_SHIFT = "perspective-shift"
JERRIS_IMAGE_PARAMETER_PHOTOGRAPHIC_INTENT = "photographic-intent"
JERRIS_IMAGE_PARAMETER_POINT_OF_LIGHT = "point-of-light"
JERRIS_IMAGE_PARAMETER_RETOUCHING = "retouching"
JERRIS_IMAGE_PARAMETER_RULE_OF_THIRDS = "rule-of-thirds"
JERRIS_IMAGE_PARAMETER_SATURATION = "saturation"
JERRIS_IMAGE_PARAMETER_SCALE_AND_PROPORTION = "scale-and-proportion"
JERRIS_IMAGE_PARAMETER_SENSE_OF_MOTION = "sense-of-motion"
JERRIS_IMAGE_PARAMETER_SHARPNESS = "sharpness"
JERRIS_IMAGE_PARAMETER_SHUTTER_SPEED = "shutter-speed"
JERRIS_IMAGE_PARAMETER_SOFT_FOCUS = "soft-focus"
JERRIS_IMAGE_PARAMETER_SUBTLE_COMPLEXITY = "subtle-complexity"
JERRIS_IMAGE_PARAMETER_SYMMETRICAL_BALANCE = "symmetrical-balance"
JERRIS_IMAGE_PARAMETER_TARGET_AUDIENCE = "target-audience"
JERRIS_IMAGE_PARAMETER_VISUAL_HARMONY = "visual-harmony"

PARAMETERS_MAPPING: dict[str, AnalyzeParameter] = {
    JERRIS_IMAGE_PARAMETER_ASPECT_RATIO: AnalyzeParameter(
        {
            "id": 13,
            "title": "Aspect Ratio",
            "type": TYPE_STRING,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_ARTIFICIAL_INTELLIGENCE_CREATION_PROBABILITY: AnalyzeParameter(
        {
            "id": 55,
            "title": "AI Creation Probability",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_COLOR_HARMONY: AnalyzeParameter(
        {
            "id": 21,
            "title": "Color Harmony",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_COLOR_MODE: AnalyzeParameter(
        {
            "id": 33,
            "title": "Color Mode",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_COLOR_TEMPERATURE: AnalyzeParameter(
        {
            "id": 43,
            "title": "Color Temperature",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_COMPOSITION_CONTRAST: AnalyzeParameter(
        {
            "id": 7,
            "title": "Composition Contrast",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_CONTRAST: AnalyzeParameter(
        {
            "id": 38,
            "title": "Contrast",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_DEPTH_OF_FIELD: AnalyzeParameter(
        {
            "id": 8,
            "title": "Depth of Field",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_DEVELOPMENT: AnalyzeParameter(
        {
            "id": 51,
            "title": "Development",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_DIAGONAL_LEADING_LINES: AnalyzeParameter(
        {
            "id": 26,
            "title": "Diagonal Leading Lines",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_DIGITAL_NOISE: AnalyzeParameter(
        {
            "id": 40,
            "title": "Digital noise",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_DIRECTIONAL_LIGHTING: AnalyzeParameter(
        {
            "id": 46,
            "title": "Directional Lighting",
            "type": TYPE_STRING,
            "nullable": True,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_DOUBLE_EXPOSURE: AnalyzeParameter(
        {
            "id": 50,
            "title": "Double Exposure",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_DUST_VISIBILITY: AnalyzeParameter(
        {
            "id": 50,
            "title": "Dust Visibility",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_EMOTIONAL_IMPACT: AnalyzeParameter(
        {
            "id": 57,
            "title": "Emotional Impact",
            "type": None,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_EXPOSURE: AnalyzeParameter(
        {
            "id": 37,
            "title": "Exposure",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_FRAME_IN_A_FRAME: AnalyzeParameter(
        {
            "id": 3,
            "title": "Frame in a frame",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_FRAMING_VIEWER: AnalyzeParameter(
        {
            "id": 3,
            "title": "Framing viewer",
            "type": TYPE_STRING,
            "nullable": True,
            "multiple": True,
        }
    ),
    JERRIS_IMAGE_PARAMETER_GOLDEN_RECTANGLES: AnalyzeParameter(
        {
            "id": 24,
            "title": "Golden Rectangles",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_GOLDEN_SPIRAL: AnalyzeParameter(
        {
            "id": 25,
            "title": "Golden Spiral",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_GOLDEN_TRIANGLES: AnalyzeParameter(
        {
            "id": 27,
            "title": "Golden Triangles",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_HAZE_PRESENCE: AnalyzeParameter(
        {
            "id": 53,
            "title": "Haze Presence",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_HIGH_DYNAMIC_RANGE: AnalyzeParameter(
        {
            "id": 53,
            "title": "HDR (High Dynamic Range)",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_HIGHLIGHT_TEXTURES_AND_DETAILS: AnalyzeParameter(
        {
            "id": 11,
            "title": "Highlight Textures and Details",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_HUE: AnalyzeParameter(
        {
            "id": 34,
            "title": "Hue",
            "type": TYPE_STRING,
            "nullable": False,
            "multiple": True,
        }
    ),
    JERRIS_IMAGE_PARAMETER_IMAGE_REALISM: AnalyzeParameter(
        {
            "id": 54,
            "title": "Image Realism",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_IMPLIED_LINES: AnalyzeParameter(
        {
            "id": 15,
            "title": "Implied Lines",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_INTENDED_PURPOSE: AnalyzeParameter(
        {
            "id": 58,
            "title": "Intended Purpose",
            "type": None,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_LEADING_LINES: AnalyzeParameter(
        {
            "id": 5,
            "title": "Leading Lines",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_LENS_FLARE: AnalyzeParameter(
        {
            "id": 5,
            "title": "Lens Flare",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_LEADING_SPACE: AnalyzeParameter(
        {
            "id": 4,
            "title": "Leading Space",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_LIGHT_REFLECTION: AnalyzeParameter(
        {
            "id": 16,
            "title": "Light Reflection",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_LIGHT_SOFTNESS_VIEWER: AnalyzeParameter(
        {
            "id": 42,
            "title": "Light Softness Viewer",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_LIGHT_SOURCE_VIEWER: AnalyzeParameter(
        {
            "id": 41,
            "title": "Light Source Viewer",
            "type": TYPE_LIST,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_LINE_DIRECTION: AnalyzeParameter(
        {
            "id": 14,
            "title": "Line Direction",
            "type": TYPE_STRING,
            "nullable": False,
            "multiple": True,
        }
    ),
    JERRIS_IMAGE_PARAMETER_LOCATION_SETTING: AnalyzeParameter(
        {
            "id": 22,
            "title": "Location Setting",
            "type": TYPE_STRING,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_LUMINOSITY: AnalyzeParameter(
        {
            "id": 35,
            "title": "Luminosity",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_MINIMIZING_DISTRACTIONS: AnalyzeParameter(
        {
            "id": 1,
            "title": "Minimizing Distractions",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_NEGATIVE_SPACE: AnalyzeParameter(
        {
            "id": 10,
            "title": "Negative Space",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_OVERALL_AESTHETICS_ASSESSMENT: AnalyzeParameter(
        {
            "id": 48,
            "title": "Overall Aesthetics Assessment",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_OVERALL_EXPERT_ASSESSMENT: AnalyzeParameter(
        {
            "id": 47,
            "title": "Overall Expert Assessment",
            "type": None,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_OVERALL_TECHNICAL_ASSESSMENT: AnalyzeParameter(
        {
            "id": 49,
            "title": "Overall Technical Assessment",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_PATTERN_RECOGNITION: AnalyzeParameter(
        {
            "id": 6,
            "title": "Pattern Recognition",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_PATTERN_REPETITION: AnalyzeParameter(
        {
            "id": 20,
            "title": "Pattern Repetition",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_PERSPECTIVE_LINES: AnalyzeParameter(
        {
            "id": 12,
            "title": "Perspective Lines",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_PERSPECTIVE_SHIFT: AnalyzeParameter(
        {
            "id": 9,
            "title": "Perspective Shift",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_PHOTOGRAPHIC_INTENT: AnalyzeParameter(
        {
            "id": 56,
            "title": "Photographic Intent",
            "type": TYPE_STRING,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_POINT_OF_LIGHT: AnalyzeParameter(
        {
            "id": 17,
            "title": "Point of Light",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_RETOUCHING: AnalyzeParameter(
        {
            "id": 52,
            "title": "Retouching",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_RULE_OF_THIRDS: AnalyzeParameter(
        {
            "id": 23,
            "title": "Rule of thirds",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_SATURATION: AnalyzeParameter(
        {
            "id": 36,
            "title": "Saturation",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_SCALE_AND_PROPORTION: AnalyzeParameter(
        {
            "id": 19,
            "title": "Scale and Proportion",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_SENSE_OF_MOTION: AnalyzeParameter(
        {
            "id": 45,
            "title": "Sense of Motion",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_SHARPNESS: AnalyzeParameter(
        {
            "id": 39,
            "title": "Sharpness",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_SOFT_FOCUS: AnalyzeParameter(
        {
            "id": 18,
            "title": "Soft Focus",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_SUBTLE_COMPLEXITY: AnalyzeParameter(
        {
            "id": 2,
            "title": "Subtle Complexity",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_SYMMETRICAL_BALANCE: AnalyzeParameter(
        {
            "id": 28,
            "title": "Symmetrical Balance",
            "type": TYPE_BOOLEAN,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_TARGET_AUDIENCE: AnalyzeParameter(
        {
            "id": 59,
            "title": "Target Audience",
            "type": TYPE_STRING,
            "nullable": False,
            "multiple": False,
        }
    ),
    JERRIS_IMAGE_PARAMETER_VISUAL_HARMONY: AnalyzeParameter(
        {
            "id": 44,
            "title": "Visual Harmony",
            "type": TYPE_INTEGER,
            "nullable": False,
            "multiple": False,
        }
    ),
}
