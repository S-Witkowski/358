from gui.elements import *
from gui.selection_box import GameModeSelectionBox

class GuiInterface(object):
    def __init__(self, screen):
        self.screen = screen
        self.gui_list = []

    def show_label(self, position, text, text_size=15, color="black", timeout=3, id_=""):
        """ Creates text label on the screen. The label is stored in the internal gui_list
        list and gets rendered automatically.
        :param position: tuple with coordinates (x,y) of top left corner of the label
        :param text: string with text for the label
        :param text_size: integer text size
        :param color: tuple (R, G, B) with text color
        :param timeout: integer seconds for the label timeout. If equals 0, label won't timeout
            and should be hidden manually.
        :param id_: string ID of the label, should be unique for each GUI element
        :return: object of gui.Label
        """
        label = Label(self.screen, position, text, text_size, color, timeout, id_)
        self.gui_list.append(label)
        return label

    def show_button(self, rectangle, callback, text, text_size=15, color=(0, 0, 0), id_=""):
        """ Creates text button on the screen. The button is stored in the internal gui_list
        list and gets rendered automatically.
        :param rectangle: list with rectangle properties [x, y, width, height]
        :param callback: function that will be called when the button is clicked
        :param text: string with text for the button
        :param text_size: integer text size
        :param color: tuple (R, G, B) with text color
        :param id_: string ID of the button, should be unique for each GUI element
        :return: object of gui.Button
        """
        button = Button(self.screen, rectangle, callback, text, text_size, color, id_)
        self.gui_list.append(button)
        return button
    
    def show_icon(self, position, image, game_mode=None, id_=""):
        element = Icon(self.screen, position, image, game_mode, id_)
        self.gui_list.append(element)
        return element
    
    def show_selection_box(self, position, id_=""):
        """ Creates text button on the screen. The button is stored in the internal gui_list
        list and gets rendered automatically.
        :param position: tuple with coordinates (x,y) of top left corner of the label
        :param id_: string ID of the button, should be unique for each GUI element
        :return: object of gui.Button
        """
        element = GameModeSelectionBox(self.screen, position, id_)
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

    def render(self):
        """ Renders all current GUI elements in the gui_list. """
        for element in self.gui_list:
            if hasattr(element, 'expired') and element.expired:
                self.gui_list.remove(element)
                continue
            element.render()

    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
        for element in self.gui_list:
            element.check_mouse(mouse_pos, mouse_keys[0])

    def clean(self):
        """ Destroys all elements in the gui_list. """
        self.gui_list = []