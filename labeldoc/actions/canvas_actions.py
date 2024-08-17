from .base_action import UserAction


def qpoint_to_str(p):
    return f'({p.x()}, {p.y()})'


class PanAction(UserAction):
    def __init__(self, canvas, start_pos, end_pos):

        super().__init__(f"Pan from {qpoint_to_str(start_pos)} to {qpoint_to_str(end_pos)}", track_undo=False)
        self.canvas = canvas
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.offset_delta = end_pos - start_pos

    def execute(self):
        """Apply the pan by adjusting the canvas offset."""
        self.canvas.pan(self.offset_delta)

    def undo(self):
        """Undo the pan by reversing the offset."""
        self.canvas.offset -= self.offset_delta
        self.canvas.update()

    def redo(self):
        """Redo the pan by reapplying the offset."""
        self.execute()

# Zoom Actions

class ZoomAction(UserAction):
    def __init__(self, canvas, old_zoom, new_zoom):
        super().__init__(f"Zoom from {old_zoom} to {new_zoom}", track_undo=False)
        self.canvas = canvas
        self.old_zoom = old_zoom
        self.new_zoom = new_zoom

    def execute(self):
        self.canvas.set_zoom_level(self.new_zoom)

    def undo(self):
        self.canvas.set_zoom_level(self.old_zoom)

class InitialZoomAction(UserAction):
    def __init__(self, canvas):
        initial_zoom = canvas.calculate_initial_zoom()
        super().__init__(f"Initial to {initial_zoom}", can_undo=False, track_undo=False)
        self.canvas = canvas
        self.initial_zoom = initial_zoom

    def execute(self):
        self.canvas.update_min_zoom_level()
        self.canvas.set_zoom_level(self.initial_zoom)

class ZoomToFitPageAction(UserAction):
    def __init__(self, canvas):
        old_zoom = canvas.zoom_level
        new_zoom = self.canvas.calculate_zoom_to_fit_page()
        super().__init__(f"Zoom to fit page from {old_zoom} to {new_zoom}", track_undo=False)
        self.canvas = canvas
        self.old_zoom = old_zoom
        self.new_zoom = new_zoom

    def execute(self):
        self.canvas.set_zoom_level(self.new_zoom)

    def undo(self):
        self.canvas.set_zoom_level(self.old_zoom)

class ZoomToFitWidthAction(UserAction):
    def __init__(self, canvas):
        old_zoom = canvas.zoom_level
        new_zoom = self.canvas.calculate_zoom_to_fit_width()
        super().__init__(f"Zoom to fit width from {old_zoom} to {new_zoom}", track_undo=False)
        self.canvas = canvas
        self.old_zoom = old_zoom
        self.new_zoom = new_zoom

    def execute(self):
        self.canvas.set_zoom_level(self.new_zoom)

    def undo(self):
        self.canvas.set_zoom_level(self.old_zoom)
