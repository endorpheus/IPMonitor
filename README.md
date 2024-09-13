# IP Monitor

**IP Monitor** is a simple and intuitive tool designed to help you keep track of your internal and external IP addresses. Whether you're managing a network or simply need to stay informed of your IP status, this application provides a straightforward solution with a clean and modern interface.

## Features

- **Internal IP Monitoring**: View all internal IP addresses assigned to your network interfaces.
- **External IP Tracking**: Get your current external IP address with a single click.
- **System Tray Integration**: Access IP details and more directly from your system tray.
- **Customizable Display**: Easily view IPs in a dedicated window with a frameless, rounded-corner design.
- **User-Friendly Interface**: Enjoy a simple and clean interface.

## Benefits

- **Efficiency**: Quickly access and manage your IP addresses without needing to navigate through multiple interfaces.
- **Convenience**: Monitor your IPs directly from the system tray, ensuring you stay updated with minimal disruption to your workflow.
- **Modern Design**: Benefit from a sleek, modern UI that integrates seamlessly with your operating system.

## Dependencies

- **Python 3**: Ensure Python 3 is installed on your system.
- **PySide6**: This application was built using the PySide6 library for GUI development... mostly.. I guess.
- **psutil**: Required for network interface information.
- **requests**: Used to fetch external IP information.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/endorpheus/ip-monitor.git
   cd ip-monitor
   ```

2. **Create a Virtual Environment (Optional but recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

- **System Tray**: Right-click on the tray icon to view internal IPs, check the external IP, access the "About" dialog, or quit the application.
- **Left-Click Action**: Left-click the tray icon to open a window displaying internal and external IP addresses.

## Contribution

Contributions are welcome! If you have suggestions, improvements, or issues to report, please open an issue or submit a pull request on the [GitHub repository](https://github.com/endorpheus/ip-monitor).

## Testing

So far, this has been tested on Linux with success under Linux with Cinnamon, KDE Plasma, and Enlightenment.
Feel free to let me know if you have tested it and if there were any issues. I don't expect there will be any since it's a very basic application.

## The Future

**Things to do:**
- add an update interval timer
- add a notification system on IP changes
- perhaps a switch for command line usage
- color, font, and text themes for the information display
- or we could just keep it simple... nah...

## Acknowledgements

- [PySide6](https://doc.qt.io/qtforpython/)
- [psutil](https://psutil.readthedocs.io/en/latest/)
- [requests](https://docs.python-requests.org/en/latest/)

### Thanks for checking out IP Monitor!
