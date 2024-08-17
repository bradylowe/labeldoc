class UserAction:
    def __init__(self, description, can_undo=True, track_undo=True):
        self.description = description
        self.can_undo = can_undo
        self.track_undo = track_undo

    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

    def redo(self):
        self.execute()
    
    def undo_not_supported(self):
        raise NotImplementedError(f"Undo functionality not supported for action \"{self.description}\"")
