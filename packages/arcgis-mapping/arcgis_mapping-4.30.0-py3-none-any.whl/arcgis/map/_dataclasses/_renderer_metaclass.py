import logging
from pydantic import ValidationError


class RendererMetaclassObject(type):
    def __call__(cls, **kwargs):
        spec = kwargs.get("spec")
        renderer_type = kwargs.get("renderer_type")
        renderer = kwargs.get("renderer")
        is_map = kwargs.get("is_map")

        renderer_class_mapping = {
            "heatmap": spec.HeatmapRenderer,
            "class breaks": spec.ClassBreaksRenderer,
            "classbreaks": spec.ClassBreaksRenderer,
            "unique value": spec.UniqueValueRenderer,
            "uniquevalue": spec.UniqueValueRenderer,
            "simple": spec.SimpleRenderer,
        }
        if is_map:
            # Webmap spec has more renderers than scene spec
            extra_classes = {
                "dot density": spec.DotDensityRenderer,
                "dotdensity": spec.DotDensityRenderer,
                "dictionary": spec.DictionaryRenderer,
                "flow": spec.FlowRenderer,
                "piechart": spec.PieChartRenderer,
                "pie chart": spec.PieChartRenderer,
                "temporal": spec.TemporalRenderer,
                "vector field": spec.VectorFieldRenderer,
                "vectorfield": spec.VectorFieldRenderer,
                "predominance": spec.PredominanceRenderer,
            }
            renderer_class_mapping.update(extra_classes)

        # Look up the renderer class from the spec
        renderer_class = renderer_class_mapping.get(
            renderer_type.lower(), spec.SimpleRenderer
        )

        try:
            return renderer_class(**renderer)
        except ValidationError as e:
            logging.error(
                f"Renderer of type {renderer_type} could not be created. Error: {e}"
            )
            return None


class FactoryWorker(metaclass=RendererMetaclassObject):
    def __init__(self, spec, renderer_type, renderer, is_map):
        spec = spec
        self.renderer_type = renderer_type
        self.renderer = renderer
        self.is_map = is_map
