from gui.elements import *
from gui.forms import *

class GuiInterface(object):
    def __init__(self, screen):
        self.screen = screen
        self.gui_list = []

    def show_label(self, id_, rect, **kwargs):
        label = Label(screen=self.screen, id_=id_, rect=rect, **kwargs)
        self.gui_list.append(label)
        return label

    def show_button(self, id_, rect, **kwargs):
        button = Button(screen=self.screen, id_=id_, rect=rect, **kwargs)
        self.gui_list.append(button)
        return button
    
    def show_icon(self, id_, rect, **kwargs):
        element = Icon(screen=self.screen, id_=id_, rect=rect, **kwargs)
        self.gui_list.append(element)
        return element
    
    def show_selection_box(self, id_, rect, **kwargs):
        """ Creates text button on the screen. The button is stored in the internal gui_list
        list and gets rendered automatically.
        :param position: tuple with coordinates (x,y) of top left corner of the label
        :param id_: string ID of the button, should be unique for each GUI element
        :return: object of gui.Button
        """
        element = GameModeSelectionBox(screen=self.screen, id_=id_, rect=rect, **kwargs)
        self.gui_list.append(element)
        return element
    
    def show_score_board_box(self, id_, rect, **kwargs):
        """ Creates text button on the screen. The button is stored in the internal gui_list
        list and gets rendered automatically.
        :param position: tuple with coordinates (x,y) of top left corner of the label
        :param id_: string ID of the button, should be unique for each GUI element
        :return: object of gui.Button
        """
        element = ScoreBoardBox(screen=self.screen, id_=id_, rect=rect, **kwargs)
        self.gui_list.append(element)
        return element
    
    def get_by_id(self, id_):
        """ Returns an object of gui.AbstractGUI (Button, Label etc.)
        :param id_: string with unique ID of GUI element
        """
        for element in self.gui_list:
            if hasattr(element, "id_") and element.id_ == id_:
                return element

    def hide_by_id(self, id_):
        """ Hides and destroys an object of gui.AbstractGUI (Button, Label etc.)
        :param id_: string with unique ID of GUI element
        """
        for element in self.gui_list:
            if hasattr(element, "id_") and element.id_ == id_:
                self.gui_list.remove(element)
                break
    
    def update(self):
        for element in self.gui_list:
            if hasattr(element, 'expired') and element.expired:
                self.gui_list.remove(element)
                continue
            element.update()

    def render(self):
        """ Renders all current GUI elements in the gui_list. """
        for element in self.gui_list:
            element.render()

    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
        for element in self.gui_list:
            element.check_mouse(mouse_pos, mouse_keys[0])

    def clean(self):
        """ Destroys all elements in the gui_list. """
        self.gui_list = []