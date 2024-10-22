from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,QDialog, QHBoxLayout,QLineEdit,QCheckBox, QPushButton,QComboBox, QLabel, QGridLayout, QFrame, QTextEdit, QGroupBox
)
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt ,QMetaObject
from hid import _initialise_driver_ ,connect_to_all
from PyQt6.QtGui import QPixmap
from controller import *

# -------------------Data Base Import-----------------------
from  database.database import get_db
from database.hid_crud import get_controller
from sqlalchemy.orm import Session

db: Session = next(get_db())
controllers = get_controller(db)

   
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
        # Get data from the input fields
        card_number = self.card_number_input.text()
        facility_code = self.facility_code_input.text()
        issue_code = self.issue_code_input.text()
        cardholder_name = self.cardholder_name_input.text()
        cardholder_phone = self.cardholder_phone_input.text()
        cardholder_image = self.cardholder_image_input.text()
        all_controllers = self.select_all_checkbox.isChecked()

        # Get selected controller if not all controllers are selected
        selected_controller = self.controller_selector.currentText() if not all_controllers else "All Controllers"

        # Pass this data to main window, database, or controllers
        # For now, print it to verify
        print(f"Card Number: {card_number}, Facility Code: {facility_code}, Issue Code: {issue_code}")
        print(f"Cardholder Name: {cardholder_name}, Phone: {cardholder_phone}, Image: {cardholder_image}")
        print(f"Controllers: {selected_controller}")

        # Close the dialog after submission
        self.accept()

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
            pixmap = QPixmap("hid_aero.png")  # Assuming you uploaded this image
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
    # Open the dialog for adding a card
        controllers = get_controller(db)  # Assuming db and get_controller are defined
        dialog = AddCardDialog(controllers)
        if dialog.exec():
            # Get card information from the dialog and process it
            pass          

# Entry point for the application
def main():
    app = QApplication([])
    window = HIDSimulator()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
