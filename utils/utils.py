# utils.py
from PyQt6.QtWidgets import QMessageBox

def show_alert(window, title, message, alert_type="info"):
    """
    Show an alert message in the application.

    Args:
        window (QWidget): The parent window where the alert will be shown.
        title (str): The title of the alert dialog.
        message (str): The message to display in the alert.
        alert_type (str): The type of alert to show: 'info', 'warning', 'error', 'critical'.
    """
    alert = QMessageBox(window)
    
    # Set the alert title and message
    alert.setWindowTitle(title)
    alert.setText(message)
    
    # Define the alert type
    if alert_type == "info":
        alert.setIcon(QMessageBox.Icon.Information)
    elif alert_type == "warning":
        alert.setIcon(QMessageBox.Icon.Warning)
    elif alert_type == "error":
        alert.setIcon(QMessageBox.Icon.Critical)
    elif alert_type == "critical":
        alert.setIcon(QMessageBox.Icon.Critical)
    
    # Display the alert dialog
    alert.exec()
