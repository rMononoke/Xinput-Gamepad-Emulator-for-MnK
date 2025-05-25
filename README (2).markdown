# XinputByMononoke v1.0

## Overview (English)

XinputByMononoke is a Python-based gamepad emulator that maps keyboard and mouse inputs to an Xbox 360 controller's XInput interface. Designed primarily for *Apex Legends*, it allows players to use keyboard and mouse inputs to control games that require a gamepad. The emulator features a graphical user interface (GUI) built with Dear PyGui for real-time configuration and supports customizable sensitivity and smoothing for precise control.

### Features

- **Keyboard Mapping**: Maps keyboard keys (e.g., WASD, Space, Q) to gamepad buttons and left stick inputs.
- **Mouse Control**: Converts mouse movements to right analog stick inputs with adjustable sensitivity and smoothing.
- **Mouse Wheel Support**: Maps mouse wheel scrolling to gamepad buttons (e.g., Y button for wheel-up).
- **GUI Configuration**: Adjust settings like mouse sensitivity, smoothing factor, and EMA alpha via a Dear PyGui interface.
- **Toggle Emulation**: Enable/disable emulation using the F1 key or GUI buttons, with visual status feedback.
- **Threaded Input Handling**: Ensures smooth and responsive input processing.
- **Customizable Parameters**: Fine-tune sensitivity, minimum sensitivity, smoothing factor, and EMA alpha for a tailored experience.

### Requirements

- Python 3.8 or higher
- Windows operating system (due to `win32api` and `vgamepad` dependencies)
- Required Python libraries:
  - `vgamepad`
  - `keyboard`
  - `mouse`
  - `pyautogui`
  - `numpy`
  - `dearpygui`

### Installation

1. **Install Python**: Ensure Python 3.8+ is installed. Download from [python.org](https://www.python.org/downloads/).
2. **Install Dependencies**: Run the following command to install required libraries:
   ```
   pip install vgamepad keyboard mouse pyautogui numpy dearpygui
   ```
3. **Download the Script**: Clone or download the `XinputByMononoke_v1.0.py` script from the repository.
4. **Run the Script**: Execute the script using Python:
   ```
   python XinputByMononoke_v1.0.py
   ```

### Usage

1. **Launch the Emulator**: Run the script to open the GUI window titled "Gamepad Emulator for Apex Legends".
2. **Configure Settings**:
   - Use the sliders to adjust:
     - **Mouse Sensitivity**: Controls the overall mouse-to-stick sensitivity (0.01–0.1).
     - **Sensitivity**: Maximum sensitivity for mouse movements (10–50).
     - **Min Sensitivity**: Minimum sensitivity for small mouse movements (10–50).
     - **Smoothing Factor**: Smooths mouse input transitions (0.05–0.5).
     - **EMA Alpha**: Controls the exponential moving average for mouse inputs (0.01–0.2).
3. **Toggle Emulation**:
   - Click the "Enable" button or press **F1** to start emulation.
   - Click the "Disable" button or press **F1** again to stop emulation.
   - The status text updates to "Enabled" (green) or "Disabled" (red).
4. **Control Mapping**:
   - **WASD**: Maps to the left analog stick (movement).
   - **Space, C, Q, Z, E, X, Tab, M, B, V, R, 1, 2, 3**: Map to various gamepad buttons (e.g., A, B, X, Y, bumpers, D-pad).
   - **Mouse Movement**: Controls the right analog stick (aiming).
   - **Mouse Wheel Up**: Triggers the Y button.
5. **Exit the Program**: Close the GUI window or press **Ctrl+C** in the console.

### Notes

- The emulator is optimized for *Apex Legends* but may work with other XInput-compatible games.
- Ensure no other applications are intercepting keyboard or mouse inputs, as this may cause conflicts.
- The GUI is resizable, and elements adjust dynamically to the window size.
- Debug information (e.g., button presses, stick values) is printed to the console for troubleshooting.
- The default font is Arial (16pt), but the script falls back gracefully if the font is unavailable.

### Troubleshooting

- **No Gamepad Detected**: Ensure `vgamepad` is installed correctly and your system recognizes the virtual Xbox 360 controller.
- **GUI Issues**: Verify that `dearpygui` is installed and compatible with your Python version.
- **Input Lag**: Reduce the `time.sleep(0.005)` value in the `handle_inputs` function for faster response, but monitor CPU usage.
- **Permission Errors**: Run the script as an administrator if `keyboard` or `mouse` libraries encounter issues.

### Contributing

Contributions are welcome! Feel free to submit pull requests or issues on the project repository. Suggestions for additional key mappings or features are appreciated.

### Credits

Developed by **rMononoke**.

### License

This project is licensed under the MIT License.

---

## Обзор (Русский)

XinputByMononoke — это эмулятор геймпада на Python, который преобразует ввод с клавиатуры и мыши в интерфейс XInput для Xbox 360 контроллера. Проект разработан в первую очередь для *Apex Legends*, позволяя игрокам использовать клавиатуру и мышь для управления играми, требующими геймпад. Эмулятор оснащён графическим интерфейсом (GUI) на основе Dear PyGui для настройки параметров в реальном времени и поддерживает настраиваемую чувствительность и сглаживание для точного управления.

### Возможности

- **Сопоставление клавиатуры**: Привязка клавиш (например, WASD, Пробел, Q) к кнопкам и левому стику геймпада.
- **Управление мышью**: Преобразование движений мыши в правый аналоговый стик с настраиваемой чувствительностью и сглаживанием.
- **Поддержка колеса мыши**: Колесо мыши активирует определённые кнопки геймпада (например, Y при прокрутке вверх).
- **Графический интерфейс**: Настройка параметров, таких как чувствительность мыши, коэффициент сглаживания и альфа EMA, через интерфейс Dear PyGui.
- **Переключение эмуляции**: Включение/выключение эмуляции с помощью клавиши F1 или кнопок в GUI с визуальной индикацией статуса.
- **Многопоточная обработка ввода**: Обеспечивает плавную и отзывчивую обработку ввода.
- **Настраиваемые параметры**: Точная настройка чувствительности, минимальной чувствительности, коэффициента сглаживания и альфа EMA.

### Требования

- Python 3.8 или выше
- Операционная система Windows (из-за зависимостей `win32api` и `vgamepad`)
- Необходимые библиотеки Python:
  - `vgamepad`
  - `keyboard`
  - `mouse`
  - `pyautogui`
  - `numpy`
  - `dearpygui`

### Установка

1. **Установите Python**: Убедитесь, что установлен Python 3.8 или выше. Скачайте с [python.org](https://www.python.org/downloads/).
2. **Установите зависимости**: Выполните следующую команду для установки необходимых библиотек:
   ```
   pip install vgamepad keyboard mouse pyautogui numpy dearpygui
   ```
3. **Скачайте скрипт**: Клонируйте или скачайте файл `XinputByMononoke_v1.0.py` из репозитория.
4. **Запустите скрипт**: Выполните скрипт с помощью Python:
   ```
   python XinputByMononoke_v1.0.py
   ```

### Использование

1. **Запустите эмулятор**: Запустите скрипт, чтобы открыть окно GUI с названием "Gamepad Emulator for Apex Legends".
2. **Настройте параметры**:
   - Используйте ползунки для настройки:
     - **Чувствительность мыши**: Управляет общей чувствительностью мыши для стика (0.01–0.1).
     - **Чувствительность**: Максимальная чувствительность для движений мыши (10–50).
     - **Минимальная чувствительность**: Минимальная чувствительность для мелких движений мыши (10–50).
     - **Коэффициент сглаживания**: СглажиАдаптер для ввода мыши (0.05–0.5).
     - **Альфа EMA**: Управляет экспоненциальным скользящим средним для ввода мыши (0.01–0.2).
3. **Переключение эмуляции**:
   - Нажмите кнопку "Enable" или клавишу **F1**, чтобы включить эмуляцию.
   - Нажмите кнопку "Disable" или клавишу **F1** снова, чтобы выключить эмуляцию.
   - Текст статуса обновляется до "Enabled" (зелёный) или "Disabled" (красный).
4. **Сопоставление управления**:
   - **WASD**: Привязаны к левому аналоговому стику (движение).
   - **Пробел, C, Q, Z, E, X, Tab, M, B, V, R, 1, 2, 3**: Привязаны к различным кнопкам геймпада (например, A, B, X, Y, бамперы, D-pad).
   - **Движение мыши**: Управляет правым аналоговым стиком (прицеливание).
   - **Прокрутка колеса мыши вверх**: Активирует кнопку Y.
5. **Выход из программы**: Закройте окно GUI или нажмите **Ctrl+C** в консоли.

### Примечания

- Эмулятор оптимизирован для *Apex Legends*, но может работать с другими играми, поддерживающими XInput.
- Убедитесь, что другие приложения не перехватывают ввод с клавиатуры или мыши, чтобы избежать конфликтов.
- GUI поддерживает изменение размера, элементы автоматически адаптируются к размеру окна.
- Для отладки информация о нажатиях кнопок и значениях стиков выводится в консоль.
- По умолчанию используется шрифт Arial (16pt), но скрипт корректно работает, если шрифт недоступен.

### Устранение неполадок

- **Геймпад не определяется**: Убедитесь, что `vgamepad` установлен правильно и система распознаёт виртуальный контроллер Xbox 360.
- **Проблемы с GUI**: Проверьте, что `dearpygui` установлен и совместим с вашей версией Python.
- **Задержка ввода**: Уменьшите значение `time.sleep(0.005)` в функции `handle_inputs` для более быстрого отклика, но следите за нагрузкой на процессор.
- **Ошибки прав доступа**: Запустите скрипт от имени администратора, если библиотеки `keyboard` или `mouse` выдают ошибки.

### Вклад в проект

Приветствуются любые улучшения! Отправляйте pull requests или сообщайте об ошибках в репозитории проекта. Предложения по добавлению новых привязок клавиш или функций также приветствуются.

### Автор

Разработано **rMononoke**.

### Лицензия

Проект распространяется под лицензией MIT.