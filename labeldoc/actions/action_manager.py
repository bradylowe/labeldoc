class ActionManager:
    def __init__(self, track_all=False):
        self.undo_stack = []
        self.redo_stack = []
        self.action_log = []
        self.track_all = track_all

    def do_action(self, action):
        action.execute()
        if action.track_undo or self.track_all:
            self.undo_stack.append(action)
            self.redo_stack.clear()
        self.action_log.append(f"Executed: {action.description}")

    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            action.undo()
            self.redo_stack.append(action)
            self.action_log.append(f"Undone: {action.description}")

    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            action.redo()
            self.undo_stack.append(action)
            self.action_log.append(f"Redone: {action.description}")

    def print_action_log(self):
        if self.action_log:
            print()
            print('=== USER ACTION LOG ===')
            for log_entry in self.action_log:
                print(log_entry)
        else:
            print('=== USER ACTION LOG EMPTY ===')
