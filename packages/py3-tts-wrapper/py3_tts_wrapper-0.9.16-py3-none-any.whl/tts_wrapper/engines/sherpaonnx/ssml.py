from ...ssml import BaseSSMLRoot, SSMLNode, Child


class SherpaOnnxSSMLNode(SSMLNode):
    def __str__(self) -> str:
        # Override to generate only the inner content without the actual SSML tags
        rendered_children = "".join(str(c) for c in self._children)
        return rendered_children


class SherpaOnnxSSML(BaseSSMLRoot):
    def __init__(self) -> None:
        super().__init__()
        self._inner = SherpaOnnxSSMLNode(
            "speak"
        )  # The tag is irrelevant but kept for compatibility

    def __str__(self) -> str:
        # Use the overridden __str__ method of SherpaOnnxSSMLNode
        return str(self._inner)

    def clear_ssml(self):
        self._inner.clear_ssml()
