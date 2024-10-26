from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,  QDialog , QTableWidget ,
    QTableWidgetItem,QHBoxLayout,QMessageBox,QLineEdit,QCheckBox,
    QPushButton,QComboBox, QLabel,QGridLayout, QFrame, QTextEdit, 
    QGroupBox,
    )

from controller.hid import _initialise_driver_ ,connect_to_all
from views.transaction_log import get_all_transaction_logs
from views.card_handeler import add_card_to_db, card_test
from database.hid_crud import get_controller
from PyQt6.QtWidgets import QApplication
from  database.database import get_db
from sqlalchemy.orm import Session
from PyQt6.QtGui import QPixmap
from datetime import datetime
from PyQt6.QtCore import Qt 
from controller import *


db: Session = next(get_db())


class TransactionTableDialog(QDialog):
    def __init__(self, transactions, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Transaction Log")
        self.setGeometry(300, 300, 600, 400)

        # Main layout
        layout = QVBoxLayout()

        # Create table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["    Card Holder Name", "Card Number", "Transaction Code", "Note", "Date"])
        self.populate_table(transactions)

        # Add table to layout
        layout.addWidget(self.table_widget)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def populate_table(self, transactions):
        self.table_widget.setRowCount(len(transactions))
        for row, transaction in enumerate(transactions):
            self.table_widget.setItem(row, 0, QTableWidgetItem(transaction["card_holder_name"]))
            self.table_widget.setItem(row, 1, QTableWidgetItem(transaction["card_number"]))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(transaction["transaction_code"])))
            self.table_widget.setItem(row, 3, QTableWidgetItem(transaction["note"]))
            self.table_widget.setItem(row, 4, QTableWidgetItem(transaction["date"].strftime('%Y-%m-%d %H:%M:%S')))

class CardTestDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Card Test")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        # Input fields for card information
        self.card_number_input = QLineEdit()
        self.card_number_input.setPlaceholderText("Enter Card Number")
        self.facility_code_input = QLineEdit()
        self.facility_code_input.setPlaceholderText("Enter Facility Code")
        self.acr_number = QLineEdit()
        self.acr_number.setPlaceholderText("Enter ACR Number")

        # Add inputs to the layout
        layout.addWidget(QLabel("Card Number"))
        layout.addWidget(self.card_number_input)
        layout.addWidget(QLabel("Facility Code"))
        layout.addWidget(self.facility_code_input)
        layout.addWidget(QLabel("Acr Number"))
        layout.addWidget(self.acr_number)

        # Submit Button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_card_info)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def submit_card_info(self):
        card_number = self.card_number_input.text().strip()
        facility_code = self.facility_code_input.text().strip()
        acr_number = self.acr_number.text().strip()

        if not card_number or not facility_code:
            self.show_alert("Input Error", "Please fill all fields before submitting.")
            return

        print(f"Card Number: {card_number}, Facility Code: {facility_code}, ACR NUmber: {acr_number}")

        success, message = card_test(db, card_number, facility_code, acr_number)
        if success:
            self.show_alert("Success", message)
            self.accept()
        else:
            self.show_alert("Error", message)

    def show_alert(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

class AddCardDialog(QDialog):
    def __init__(self, controllers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Card")
        self.setGeometry(300, 300, 400, 300)

        # Main layout
        layout = QVBoxLayout()

        # Input fields for card information
        self.card_number_input = QLineEdit()
        self.card_number_input.setPlaceholderText("Enter Card Number")
        self.card_pin = QLineEdit()
        self.card_pin.setPlaceholderText("Enter Card Pin")
        self.facility_code_input = QLineEdit()
        self.facility_code_input.setPlaceholderText("Enter Facility Code")
        self.issue_code_input = QLineEdit()
        self.issue_code_input.setPlaceholderText("Enter Issue Code")
        self.cardholder_name_input = QLineEdit()
        self.cardholder_name_input.setPlaceholderText("Enter Cardholder Name")
        self.cardholder_phone_input = QLineEdit()
        self.cardholder_phone_input.setPlaceholderText("Enter Cardholder Phone")

        # Add cardholder image (optional)
        self.cardholder_image_input = QLineEdit()
        self.cardholder_image_input.setPlaceholderText("Upload Cardholder Image")

        # Controller Selection (All or Specific)
        self.select_all_checkbox = QCheckBox("Select All Controllers")
        self.controller_selector = QComboBox()
        self.controller_selector.setPlaceholderText("Select Controllers")
        
        # Add all controllers to the dropdown
        for controller in controllers:
            self.controller_selector.addItem(controller.name)

        # Add inputs to the layout
        layout.addWidget(QLabel("Card Number"))
        layout.addWidget(self.card_number_input)
        layout.addWidget(QLabel("Facility Code"))
        layout.addWidget(self.facility_code_input)
        layout.addWidget(QLabel("Card Pin"))
        layout.addWidget(self.card_pin)
        layout.addWidget(QLabel("Issue Code"))
        layout.addWidget(self.issue_code_input)
        layout.addWidget(QLabel("Cardholder Name"))
        layout.addWidget(self.cardholder_name_input)
        layout.addWidget(QLabel("Cardholder Phone"))
        layout.addWidget(self.cardholder_phone_input)
        layout.addWidget(QLabel("Cardholder Image"))
        layout.addWidget(self.cardholder_image_input)
        layout.addWidget(self.select_all_checkbox)
        layout.addWidget(QLabel("Select Specific Controller"))
        layout.addWidget(self.controller_selector)

        # Submit Button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_card_info)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def submit_card_info(self):
        card_number = self.card_number_input.text().strip()
        facility_code = self.facility_code_input.text().strip()
        issue_code = self.issue_code_input.text().strip()
        cardholder_name = self.cardholder_name_input.text().strip()
        cardholder_phone = self.cardholder_phone_input.text().strip()
        card_pin = self.card_pin.text().strip()
        cardholder_image = self.cardholder_image_input.text().strip()
        
        if not card_number or not facility_code or not issue_code or not cardholder_name or not card_pin:
            self.show_alert("Input Error", "Please fill all required fields before submitting.")
            return

        try:
            facility_code = int(facility_code)
            issue_code = int(issue_code)
        except ValueError:
            self.show_alert("Input Error", "Facility Code and Issue Code must be valid numbers.")
            return

        db: Session = next(get_db())

        success, message = add_card_to_db(db, card_number, facility_code, issue_code, cardholder_name, cardholder_phone)
        if success:
            self.show_alert("Success", message)
            self.accept()
        else:
            self.show_alert("Error", message)

    def show_alert(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

class HIDSimulator(QWidget):

    def __init__(self):
        super().__init__()
        # self.live_status_labels = [] 
        self.controller_widgets = {}
        self.init_ui()
        _initialise_driver_(self)

    def init_ui(self):
        self.setWindowTitle('HID Aero X1100 Simulator')
        self.setGeometry(100, 100, 1200, 800)  # Larger canvas
        self.showMaximized()
        # Main layout (divided into three sections: left (buttons), right (controllers), and bottom (log))
        main_layout = QVBoxLayout()

        # Top section: Contains control buttons and HID controllers
        top_section_layout = QHBoxLayout()

        # Left: Control Buttons section layout
        control_group = QGroupBox("Control Button")
        control_box_layout = QVBoxLayout()

        # Control Buttons: Adding the buttons into the control box
        connect_button = QPushButton('Connect to Device')
        disconnect_button = QPushButton('Disconnect Device')
        initialize_button = QPushButton('Initialize Device')
        card_test_button = QPushButton('Card Test')
        add_card_button = QPushButton('Add Card')
        remove_card_button = QPushButton('Remove Card')
        some_other_button = QPushButton('Other Action')

        # Add buttons to the layout
        control_box_layout.addWidget(connect_button)
        control_box_layout.addWidget(disconnect_button)
        control_box_layout.addWidget(initialize_button)
        control_box_layout.addWidget(card_test_button)
        control_box_layout.addWidget(add_card_button)
        control_box_layout.addWidget(remove_card_button)
        control_box_layout.addWidget(some_other_button)

        control_group.setLayout(control_box_layout)

        # Connect the button click to a function
        connect_button.clicked.connect(lambda: connect_to_all(self))
        add_card_button.clicked.connect(self.open_add_card_dialog)
        remove_card_button.clicked.connect(self.show_alert)
        card_test_button.clicked.connect(self.open_card_test_dialog)
        some_other_button.clicked.connect(self.open_transaction_log_dialog)

        # Right: HID Controllers section
        controllers_group = QGroupBox("HID Controllers")
        device_layout = QGridLayout()

        controllers = get_controller(db)
        for i,controller in enumerate(controllers): 
            device_frame = QFrame()
            device_frame.setFrameShape(QFrame.Shape.Box)
            device_frame.setLineWidth(2)
            device_frame.setFixedSize(250, 150)

            # Layout for details within the device frame
            device_inner_layout = QVBoxLayout()

            # Image for HID Device
            image_label = QLabel()
            pixmap = QPixmap("assets/images/hid_aero.png")  # Assuming you uploaded this image
            image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

            # Controller details
            controller_label = QLabel(f'Controller {controller.scp_number}')
            controller_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            controller_name = QLabel(f'Name: {controller.name}')
            controller_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Live status icons
            live_status = QLabel('Not Fetched ❌')
            live_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # self.live_status_labels.append(live_status)

            driver_status = QLabel('Not Fetched ✅')
            driver_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Add all elements to the device layout
            device_inner_layout.addWidget(image_label)
            device_inner_layout.addWidget(controller_label)
            device_inner_layout.addWidget(controller_name)
            device_inner_layout.addWidget(live_status)
            device_inner_layout.addWidget(driver_status)

            device_frame.setLayout(device_inner_layout)
            device_layout.addWidget(device_frame, i // 2, i % 2)  # 2 devices per row

            self.controller_widgets[controller.scp_number] = {
                "frame": device_frame,
                "controller_label": controller_label,
                "controller_name": controller_name,
                "online_status": live_status,
                "driver_status": driver_status
            }

        controllers_group.setLayout(device_layout)

        # Bottom section: Log output box
        log_group = QGroupBox("Log Output")
        self.log_box = QTextEdit()  # Use self.log_box to access in other methods
        self.log_box.setPlaceholderText("Log details will be displayed here...")
        log_group_layout = QVBoxLayout()
        log_group_layout.addWidget(self.log_box)
        log_group.setLayout(log_group_layout)
        log_group.setFixedHeight(150)  # Set fixed height for the log output

        # Add the left (buttons) and right (controllers) sections to the top section
        top_section_layout.addWidget(control_group)  # Add control buttons on the left
        top_section_layout.addWidget(controllers_group)  # Add HID controllers on the right

        # Add the top section and bottom section to the main layout
        main_layout.addLayout(top_section_layout)  # Top section with buttons and controllers
        main_layout.addWidget(log_group)  # Bottom section with log output

        self.setLayout(main_layout)
    
    def update_controller(self, scp_number, driver_status=None, new_name=None,scp_online_status=None):
        if scp_number in self.controller_widgets:
            if driver_status:
                self.controller_widgets[scp_number]["driver_status"].setText(driver_status)
            if new_name:
                self.controller_widgets[scp_number]["controller_name"].setText(f"{new_name}")
            if scp_online_status:
                self.controller_widgets[scp_number]["online_status"].setText(f"{scp_online_status}")
        else:
            self.log_box.append(f"Controller with SCP number {scp_number} not found.")

    def update_live_status(self, index, status):
        # Update the status safely using QMetaObject
        # QMetaObject.invokeMethod(self.live_status_labels[index], "setText", Qt.ConnectionType.QueuedConnection,
        #                          status)
        self.live_status_labels[index].setText(status)

    def open_add_card_dialog(self):
        controllers = get_controller(db) 
        dialog = AddCardDialog(controllers)
        if dialog.exec():
            pass 

    def open_card_test_dialog(self):
        dialog = CardTestDialog(self)
        if dialog.exec():
            pass    
    
    def show_alert(self):

        title ="checking"
        message="Checking the message"
        alert_type="info"
        """
        Show an alert message in the application.

        Args:
            window (QWidget): The parent window where the alert will be shown.
            title (str): The title of the alert dialog.
            message (str): The message to display in the alert.
            alert_type (str): The type of alert to show: 'info', 'warning', 'error', 'critical'.
        """
        alert = QMessageBox(self)
        
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

    def open_transaction_log_dialog(self):
        # Example data for transactions; replace with actual database queries as needed
        try:
            transactions = get_all_transaction_logs(db)
            t_data = []
            for i in transactions:
                t_data.append({"card_holder_name": str(i.card_id), "card_number": str(i.card_id), "transaction_code": str(i.log_type), "note": i.log_detail, "date": datetime.now()})
                # print(i.card_id , i.controller.name , i.created_on , i.card_id , i.log_type)
            dialog = TransactionTableDialog(t_data, self)
            dialog.exec()
        except Exception as e:
            print(e)

def main():
    app = QApplication([])
    window = HIDSimulator()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
