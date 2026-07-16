# csv_qwen_suite (ComfyUI custom nodes)
# ComfyUI loads this module from custom_nodes/* folders. Register nodes via NODE_CLASS_MAPPINGS.

from .src.nodes import CSVQwenPromptSeedIterator

NODE_CLASS_MAPPINGS = {
    "CSVQwenPromptSeedIterator": CSVQwenPromptSeedIterator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CSVQwenPromptSeedIterator": "CSV Qwen Prompt + Seed Iterator",
}
