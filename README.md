VspexHost - By Xscripts Inc. (Owned by me)
--------------------------------------------------
 # What is VspexHost?

VSPEXHOST is a lightweight Python-based web server that can render HTML, handle requests, and display logs in a simple GUI. The server is designed to be extensible and provides a basic framework for routing and handling HTTP requests. It includes a graphical user interface (GUI) to display real-time logs and server status, making it easy to monitor server activity.

## Features
- **Routing:** Handle different HTTP requests using simple routes defined with `@router.setpath`.
- **HTML Rendering:** Dynamically generate HTML content and return it to clients.
- **Logging:** Logs server activity in real-time, including requests, errors, and messages.
- **GUI Monitoring:** Displays a graphical user interface (GUI) to view logs and server actions.
- **Multi-threaded:** Supports concurrent requests by using threading for the web server.

## Requirements
- Python 3.x or higher
- Tkinter (usually included with Python installation)

## Installation

1. Clone the repository or download the `main.py` file.
2. Install Python if you haven't already: https://www.python.org/downloads/.
3. Run the script using Python:

   ```bash
   python main.py
