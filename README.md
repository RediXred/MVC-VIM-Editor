# MVC Vim Editor

## Overview
MVC Vim Editor is a text editor implemented in Python using the Curses library. It follows the MVC (Model-View-Controller) architecture and is built on a custom MVC framework. Additionally, it utilizes a custom-built **MyString.pyd** library, which is a C++ wrapper for `std::string`.

## Installation & Usage

### Usage
To run MVC Vim Editor, ensure you have Python installed along with the required `curses` package:

```sh
pip install windows-curses  # Only needed for Windows users
python main.py
```

## MVC Framework Architecture
The **MVC framework** used in this project is located in the `mymvc` directory. Below are its main components and how to extend them:

### BaseController.py
- To add controllers, use:
  ```python
  BaseController.add_controller('name', NameModeController(BaseControllerObject))
  ```
- To switch active controllers:
  ```python
  BaseController.switch_controller('name')
  ```
- To add models:
  ```python
  BaseController.add_model('name', NameModelObject)
  ```
- To start the program's main loop:
  ```python
  BaseController.start_cycle()
  ```

### IController.py
Defines an interface for sub-controllers. Implement the provided methods in subclasses.

### BaseModel.py
- To add an Observer:
  ```python
  BaseModel.add_observer(observer)
  ```
- To notify all Observers:
  ```python
  BaseModel.notify_observers()
  ```

### BaseView.py
- To get the TUI library adapter (Curses in this case), implement:
  ```python
  def get_tui_adapter(self):
  ```
- Additional methods to override in subclasses:
  ```python
  def update_text(self, text: str)
  def update_cursor(self, cursor_x: int, cursor_y: int)
  def update_status_bar(self, mode: str, f_name: str, current_line: int, total_lines: int)
  ```

### Observer.py
Implements the Observer pattern. Methods should be defined in subclassed Views.

### ITuiAdapter.py
Defines an interface for TUI adapters. Implement required methods in a subclass.

### ICommand.py
Defines an interface for implementing commands in controllers. Subclasses should provide concrete implementations.

### IInput.py
Defines an interface for handling key presses. Implement required methods in a subclass.

## Additional Details
For further implementation details, refer to `main.py`.

---
**Author:** XRediX

