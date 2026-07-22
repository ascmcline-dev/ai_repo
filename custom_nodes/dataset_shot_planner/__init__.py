from .src.nodes import DatasetShotPlanner

NODE_CLASS_MAPPINGS = {
    "DatasetShotPlanner": DatasetShotPlanner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DatasetShotPlanner": "Dataset Shot Planner v1.7.0",
}

WEB_DIRECTORY = "./web"

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]
