from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, game_controller):
        self.game_controller = game_controller
        self.prev_state = None
        self.done = False
        self.quit = False
        self.clicked_rect = None

    def enter_state(self):
        if len(self.game_controller.state_stack) >= 1:
            self.prev_state = self.game_controller.state_stack[-1]
            print(f"prev state: {self.prev_state}")
        self.game_controller.state_stack.append(self)
        print(f"new state: {self}")

    def exit_state(self):
        self.game_controller.state_stack.pop()

    @abstractmethod
    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event=None):
        pass

    @abstractmethod
    def update(self):
        """Implement update method to update game state"""
        pass

    @abstractmethod
    def render(self, screen):
        pass

