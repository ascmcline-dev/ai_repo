from .src.nodes import StandardCharacterCreator

NODE_CLASS_MAPPINGS = {
    "StandardCharacterCreator": StandardCharacterCreator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StandardCharacterCreator": "Standard Character Creator v1.5",
}

WEB_DIRECTORY = "./web"

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]
