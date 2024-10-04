from timeit import default_timer
import dearpygui.dearpygui as dpg
from pynput.mouse import Controller
import time

EPS = 1
MOUSE = Controller()
TIMEOUT_OFFSET = 20


def update_state():
    label_is_enabled = dpg.get_value("is_enabled") == "Enabled"
    # we flip the label
    new_label = "Enabled" if not label_is_enabled else "Disabled"
    dpg.set_value("is_enabled", new_label)
    dpg.configure_item("is_enabled", label=new_label)


def main():
    LAST_TRIGGER = default_timer()
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

    with dpg.window(label="Toss 'n' Turn") as primary_window:
        dpg.add_text("Toss 'n' Turn...")
        dpg.add_text('keeps the session "alive"')
        dpg.add_button(label="Toggle", callback=update_state)
        dpg.add_text(label="Enabled", tag="is_enabled", default_value="Enabled")
        dpg.add_slider_int(
            label="timeout in minutes",
            tag="timeout_in_minutes",
            min_value=0,
            max_value=10,
            default_value=5,
        )

    # move_mouse()
    dpg.set_primary_window(primary_window, True)
    dpg.create_viewport(title="Window", width=200, height=150)
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        is_enabled = dpg.get_value("is_enabled") == "Enabled"
        timeout_in_minutes = dpg.get_value("timeout_in_minutes") * 60
        timeout_in_seconds = timeout_in_minutes - TIMEOUT_OFFSET
        if (
            is_enabled
            and default_timer() - LAST_TRIGGER > timeout_in_seconds
            and timeout_in_minutes > 0
        ):
            MOUSE.move(EPS, 0)
            MOUSE.move(-EPS, 0)
            LAST_TRIGGER = default_timer()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
