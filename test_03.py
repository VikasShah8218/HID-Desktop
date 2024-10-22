from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QFrame, QTextEdit, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class HIDSimulator(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

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
        connect_button.clicked.connect(self.connect_to_device)

        # Right: HID Controllers section
        controllers_group = QGroupBox("HID Controllers")
        device_layout = QGridLayout()

        for i in range(6):  # 6 devices for example
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
            controller_label = QLabel(f'Controller {i+1}')
            controller_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            controller_name = QLabel(f'Name: HID Device {i+1}')
            controller_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Live status icons
            live_status = QLabel('Controller is Live ✅')
            live_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            driver_status = QLabel('Driver is Live ✅')
            driver_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Add all elements to the device layout
            device_inner_layout.addWidget(image_label)
            device_inner_layout.addWidget(controller_label)
            device_inner_layout.addWidget(controller_name)
            device_inner_layout.addWidget(live_status)
            device_inner_layout.addWidget(driver_status)

            device_frame.setLayout(device_inner_layout)
            device_layout.addWidget(device_frame, i // 2, i % 2)  # 2 devices per row

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

    # Function that will be triggered when 'Connect to Device' is clicked
    def connect_to_device(self):
        self.log_box.append("Connecting to device...")  # Append log to log_box

# Entry point for the application
def main():
    app = QApplication([])
    window = HIDSimulator()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
