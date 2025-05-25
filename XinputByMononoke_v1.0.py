import vgamepad as vg
import keyboard
import mouse
import time
import threading
import win32api
import win32con
import pyautogui
import math
import numpy as np
import dearpygui.dearpygui as dpg

# Инициализация виртуального геймпада
gamepad = vg.VX360Gamepad()

# Чувствительность мыши для стика
MOUSE_SENSITIVITY = 0.05
sensitivity = 30
min_sensitivity = 30  
smoothing_factor = 0.15 
dead_zone_radius = 0  
ema_alpha = 0.05 

# Максимальное значение стика (от -1.0 до 1.0)
STICK_MAX = 1.0

# Переменные для отслеживания состояния стиков
left_stick_x = 0.0
left_stick_y = 0.0
right_stick_x = 0.0
right_stick_y = 0.0

# Переменные для EMA и нормализации
prev_ema_delta_x = 0.0
prev_ema_delta_y = 0.0
screen_width, screen_height = pyautogui.size()
center_x, center_y = screen_width // 2, screen_height // 2
prev_norm_delta_x = 0.0
prev_norm_delta_y = 0.0

# Флаги для остановки потоков и состояния эмуляции
running = True
emulation_enabled = False

# Сопоставление клавиш клавиатуры с кнопками геймпада
key_to_gamepad_button = {
    'space': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    'c': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    'left ctrl': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    'q': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    'z': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER | vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    'e': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    'x': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    'tab': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    'm': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    'b': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    'v': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
    'r': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    '1': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    '2': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    '3': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
}

# Переменные для отслеживания состояния кнопок
button_states = {key: False for key in key_to_gamepad_button}

# Функция для обработки всех вводов (движение, кнопки, мышь)
def handle_inputs():
    global left_stick_x, left_stick_y, right_stick_x, right_stick_y, running, emulation_enabled
    global prev_ema_delta_x, prev_ema_delta_y, prev_norm_delta_x, prev_norm_delta_y

    while running:
        if emulation_enabled:
            # Сбрасываем состояние геймпада
            gamepad.reset()

            # Обработка WASD (левый стик)
            left_stick_x = 0.0
            left_stick_y = 0.0
            if keyboard.is_pressed('w'):
                left_stick_y = STICK_MAX
                print("W pressed: left_stick_y = ", left_stick_y)
            if keyboard.is_pressed('s'):
                left_stick_y = -STICK_MAX
                print("S pressed: left_stick_y = ", left_stick_y)
            if keyboard.is_pressed('a'):
                left_stick_x = -STICK_MAX
                print("A pressed: left_stick_x = ", left_stick_x)
            if keyboard.is_pressed('d'):
                left_stick_x = STICK_MAX
                print("D pressed: left_stick_x = ", left_stick_x)
            gamepad.left_joystick_float(x_value_float=left_stick_x, y_value_float=left_stick_y)

            # Обработка мыши (правый стик)
            x, y = pyautogui.position()
            delta_x = (x - center_x) * MOUSE_SENSITIVITY
            delta_y = (y - center_y) * MOUSE_SENSITIVITY
            distance_from_center_squared = delta_x**2 + delta_y**2
            if distance_from_center_squared < dead_zone_radius**2:
                delta_x = 0
                delta_y = 0

            x_offset = delta_x / center_x
            y_offset = delta_y / center_y
            distance_max = math.sqrt(center_x**2 + center_y**2)
            distance_from_center = math.sqrt(distance_from_center_squared)
            normalized_distance = distance_from_center / distance_max
            final_sensitivity = (sensitivity * normalized_distance) + min_sensitivity
            final_sensitivity = np.clip(final_sensitivity, min_sensitivity, sensitivity)

            if distance_from_center == 0.0:
                norm_delta_x = 0.0
                norm_delta_y = 0.0
            else:
                norm_delta_x = x_offset * final_sensitivity
                norm_delta_y = y_offset * final_sensitivity

            norm_delta_x = prev_norm_delta_x + smoothing_factor * (norm_delta_x - prev_norm_delta_x)
            norm_delta_y = prev_norm_delta_y + smoothing_factor * (norm_delta_y - prev_norm_delta_y)

            ema_delta_x = ema_alpha * norm_delta_x + (1 - ema_alpha) * prev_ema_delta_x
            ema_delta_y = ema_alpha * norm_delta_y + (1 - ema_alpha) * prev_ema_delta_y
            prev_ema_delta_x = ema_delta_x
            prev_ema_delta_y = ema_delta_y

            prev_norm_delta_x = norm_delta_x
            prev_norm_delta_y = norm_delta_y

            right_stick_x = max(-1.0, min(ema_delta_x, 1.0))
            right_stick_y = max(-1.0, min(ema_delta_y, 1.0))

            gamepad.right_joystick_float(x_value_float=right_stick_x, y_value_float=-right_stick_y)

            # Обработка кнопок
            for key, button in key_to_gamepad_button.items():
                current_state = keyboard.is_pressed(key)
                if current_state and not button_states[key]:
                    print(f"Button pressed: {key} -> {button}")
                    gamepad.press_button(button=button)
                    button_states[key] = True
                elif not current_state and button_states[key]:
                    print(f"Button released: {key} -> {button}")
                    gamepad.release_button(button=button)
                    button_states[key] = False

            # Обновляем состояние геймпада
            gamepad.update()
        else:
            # Сбрасываем геймпад, когда эмуляция выключена
            gamepad.reset()
            gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
            for key in button_states:
                if button_states[key]:
                    gamepad.release_button(button=key_to_gamepad_button[key])
                    button_states[key] = False
            gamepad.update()
        time.sleep(0.005)  # Уменьшенная задержка для плавности

# Функция для обработки колеса мыши
def handle_mouse_wheel(event):
    if emulation_enabled and isinstance(event, mouse.WheelEvent):
        if event.delta > 0:
            print("Mouse wheel up: Emulating Y button")
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            gamepad.update()
            time.sleep(0.05)
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            gamepad.update()

# Функция для переключения эмуляции
def toggle_emulation(sender=None, app_data=None, user_data=None):
    global emulation_enabled
    emulation_enabled = not emulation_enabled
    print(f"Эмуляция {'включена' if emulation_enabled else 'выключена'}")
    dpg.set_value("status_text", f"Status: {'Enabled' if emulation_enabled else 'Disabled'}")
    dpg.configure_item("status_text", color=[0, 255, 0] if emulation_enabled else [255, 0, 0])
    dpg.configure_item("start_button", enabled=not emulation_enabled)
    dpg.configure_item("stop_button", enabled=emulation_enabled)
    gamepad.reset()
    gamepad.update()
    time.sleep(0.5)

# Функции для обновления параметров чувствительности
def update_mouse_sensitivity(sender, app_data):
    global MOUSE_SENSITIVITY
    MOUSE_SENSITIVITY = app_data
    print(f"Mouse Sensitivity updated: {MOUSE_SENSITIVITY}")

def update_sensitivity(sender, app_data):
    global sensitivity
    sensitivity = app_data
    print(f"Sensitivity updated: {sensitivity}")

def update_min_sensitivity(sender, app_data):
    global min_sensitivity
    min_sensitivity = app_data
    print(f"Min Sensitivity updated: {min_sensitivity}")

def update_smoothing_factor(sender, app_data):
    global smoothing_factor
    smoothing_factor = app_data
    print(f"Smoothing Factor updated: {smoothing_factor}")

def update_ema_alpha(sender, app_data):
    global ema_alpha
    ema_alpha = app_data
    print(f"EMA Alpha updated: {ema_alpha}")

# Настройка Dear PyGui
dpg.create_context()
dpg.create_viewport(title="Gamepad Emulator for Apex Legends", width=400, height=600, resizable=True)

# Загрузка шрифта
with dpg.font_registry():
    try:
        default_font = dpg.add_font("C:/Windows/Fonts/Arial.ttf", 16, tag="default_font")
    except:
        default_font = None
dpg.bind_font(default_font)

# Настройка стилей
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [50, 50, 50, 255])
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, [20, 20, 20, 255])
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [70, 70, 70, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [100, 100, 100, 255])
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)

# Создание окна
with dpg.window(label="Gamepad Emulator", no_resize=False, no_title_bar=False, tag="main_window", width=400, height=600, pos=[0, 0], no_scrollbar=True, no_scroll_with_mouse=True):
    with dpg.group(tag="main_group"):
        dpg.add_text("Gamepad Emulator v1.0", tag="title_text", color=[255, 255, 255, 255])
        dpg.add_spacer(height=10, tag="spacer1")
        dpg.add_text("Mouse Sensitivity Settings:", tag="sensitivity_label", color=[200, 200, 200, 255])
        dpg.add_spacer(height=5, tag="spacer2")
        dpg.add_text("Mouse Sensitivity:", tag="mouse_sensitivity_label", color=[200, 200, 200, 255])
        dpg.add_slider_float(label="", default_value=MOUSE_SENSITIVITY, min_value=0.01, max_value=0.1, callback=update_mouse_sensitivity, tag="mouse_sensitivity_slider", width=0)
        dpg.add_spacer(height=5, tag="spacer3")
        dpg.add_text("Sensitivity:", tag="sensitivity_label2", color=[200, 200, 200, 255])
        dpg.add_slider_float(label="", default_value=sensitivity, min_value=10, max_value=50, callback=update_sensitivity, tag="sensitivity_slider", width=0)
        dpg.add_spacer(height=5, tag="spacer4")
        dpg.add_text("Min Sensitivity:", tag="min_sensitivity_label", color=[200, 200, 200, 255])
        dpg.add_slider_float(label="", default_value=min_sensitivity, min_value=10, max_value=50, callback=update_min_sensitivity, tag="min_sensitivity_slider", width=0)
        dpg.add_spacer(height=5, tag="spacer5")
        dpg.add_text("Smoothing Factor:", tag="smoothing_label", color=[200, 200, 200, 255])
        dpg.add_slider_float(label="", default_value=smoothing_factor, min_value=0.05, max_value=0.5, callback=update_smoothing_factor, tag="smoothing_slider", width=0)
        dpg.add_spacer(height=5, tag="spacer6")
        dpg.add_text("EMA Alpha:", tag="ema_alpha_label", color=[200, 200, 200, 255])
        dpg.add_slider_float(label="", default_value=ema_alpha, min_value=0.01, max_value=0.2, callback=update_ema_alpha, tag="ema_alpha_slider", width=0)
        dpg.add_spacer(height=10, tag="spacer7")
        dpg.add_button(label="Enable", callback=toggle_emulation, tag="start_button", width=0, height=0)
        with dpg.theme() as start_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [76, 175, 80, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [69, 160, 73, 255])
        dpg.bind_item_theme("start_button", start_theme)
        dpg.add_spacer(height=10, tag="spacer8")
        dpg.add_button(label="Disable", callback=toggle_emulation, tag="stop_button", width=0, height=0, enabled=False)
        with dpg.theme() as stop_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [244, 67, 54, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [220, 60, 48, 255])
        dpg.bind_item_theme("stop_button", stop_theme)
        dpg.add_spacer(height=10, tag="spacer9")
        dpg.add_text("Status: Disabled", tag="status_text", color=[255, 0, 0, 255])
        dpg.add_spacer(height=5, tag="spacer10")
        dpg.add_text("Press F1 or buttons to toggle emulation", tag="instruction_text", color=[200, 200, 200, 255])
        dpg.add_spacer(height=5, tag="spacer11")
        dpg.add_text("Made by rMononoke", tag="signature_text", color=[150, 150, 150, 255])

# Функция для обработки изменения размера окна
def resize_callback(sender, app_data):
    viewport_width, viewport_height = app_data[0], app_data[1]
    dpg.configure_item("main_window", width=viewport_width, height=viewport_height, pos=[0, 0])
    padding = max(10, viewport_width * 0.05)
    element_width = int(viewport_width * 0.8)
    button_height = int(viewport_height * 0.08)
    font_scale = max(1.0, min(viewport_width / 400, viewport_height / 600))
    with dpg.font_registry():
        try:
            default_font = dpg.add_font("C:/Windows/Fonts/Arial.ttf", 16 * font_scale, tag="default_font")
            dpg.bind_font(default_font)
        except:
            pass
    dpg.configure_item("mouse_sensitivity_slider", width=element_width)
    dpg.configure_item("sensitivity_slider", width=element_width)
    dpg.configure_item("min_sensitivity_slider", width=element_width)
    dpg.configure_item("smoothing_slider", width=element_width)
    dpg.configure_item("ema_alpha_slider", width=element_width)
    dpg.configure_item("start_button", width=element_width, height=button_height)
    dpg.configure_item("stop_button", width=element_width, height=button_height)
    indent = (viewport_width - element_width) // 2
    for tag in ["title_text", "sensitivity_label", "mouse_sensitivity_label", "mouse_sensitivity_slider",
                "sensitivity_label2", "sensitivity_slider", "min_sensitivity_label", "min_sensitivity_slider",
                "smoothing_label", "smoothing_slider", "ema_alpha_label", "ema_alpha_slider",
                "start_button", "stop_button", "status_text", "instruction_text", "signature_text"]:
        dpg.configure_item(tag, indent=indent)
    total_elements_height = (
        30 + 10 + 20 + 5 + 20 + 30 + 5 + 20 + 30 + 5 + 20 + 30 + 5 + 20 + 30 + 5 +
        button_height + 10 + button_height + 10 + 20 + 5 + 20 + 5 + 20
    )
    vertical_offset = (viewport_height - total_elements_height) // 2
    if vertical_offset < padding:
        vertical_offset = padding
    dpg.configure_item("spacer1", height=vertical_offset)

# Основной цикл программы
def main():
    global running
    print("Запущена программа эмуляции геймпада для Apex Legends. Используйте GUI или F1 для включения/выключения эмуляции, закройте окно или нажмите Ctrl+C для выхода.")
    
    # Запускаем единый поток для обработки всех вводов
    input_thread = threading.Thread(target=handle_inputs)
    input_thread.start()
    
    # Настройка слушателя для колеса мыши
    mouse.hook(handle_mouse_wheel)
    
    # Настройка Dear PyGui
    dpg.bind_theme(global_theme)
    dpg.set_viewport_resize_callback(resize_callback)
    resize_callback(None, [400, 600])
    dpg.setup_dearpygui()
    dpg.show_viewport()
    
    # Привязка F1 для переключения эмуляции
    keyboard.on_press_key('f1', lambda e: toggle_emulation())
    
    try:
        dpg.start_dearpygui()
    except KeyboardInterrupt:
        print("Программа завершена.")
    finally:
        running = False
        gamepad.reset()
        gamepad.update()
        mouse.unhook(handle_mouse_wheel)
        input_thread.join()
        dpg.destroy_context()

if __name__ == "__main__":
    main()