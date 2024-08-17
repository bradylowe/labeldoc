from .base_action import UserAction


class DrawShapeAction(UserAction):
    def __init__(self, canvas, shape):
        super().__init__(f"Draw shape: {shape}")
        self.canvas = canvas
        self.shape = shape

    def execute(self):
        self.canvas.add_shape(self.shape)

    def undo(self):
        self.canvas.remove_shape(self.shape)