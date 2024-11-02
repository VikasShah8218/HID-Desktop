from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,  QDialog , QTableWidget ,
    QTableWidgetItem,QHBoxLayout,QMessageBox,QLineEdit,QCheckBox,
    QPushButton,QComboBox, QLabel,QGridLayout, QFrame, QTextEdit, 
    QGroupBox,QFileDialog,QGraphicsDropShadowEffect,
    )
from controller.hid import _initialise_driver_, connect_to_all, config_controller ,set_time, change_ACR
from views.file_view import upload_file, get_all_files, delete_config_record, get_config_file_by_id
from views.controller_crud import get_controllers, get_controller, create_controller
from views.transaction_log import get_all_transaction_logs
from views.card_handeler import add_card_to_db, card_test
from style.button_css import BUTTON_CSS , CTRL_CSS
from PyQt6.QtCharts import QChart, QChartView, QBarSet, QBarSeries
from PyQt6.QtGui import QPixmap ,QColor,QPainter,QIntValidator
from PyQt6.QtWidgets import QApplication
from database.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from PyQt6.QtCore import Qt 
from controller import *
import configparser


db: Session = next(get_db())
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

class AddControllerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Controller")
        self.setGeometry(300, 300, 400, 300)
        
        # Main layout
        container = QWidget(self)
        layout = QVBoxLayout(container)

        # Controller Name (Text)
        layout.addWidget(QLabel("Controller Name"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Controller Name")
        layout.addWidget(self.name_input)

        # Controller SCP Number (Integer)
        layout.addWidget(QLabel("Controller SCP Number"))
        self.scp_number_input = QLineEdit()
        self.scp_number_input.setPlaceholderText("Enter SCP Number")
        self.scp_number_input.setValidator(QIntValidator())  # Ensures input is an integer
        layout.addWidget(self.scp_number_input)

        # Controller Channel Number (Integer)
        layout.addWidget(QLabel("Controller Channel Number"))
        self.channel_number_input = QLineEdit()
        self.channel_number_input.setPlaceholderText("Enter Channel Number")
        self.channel_number_input.setValidator(QIntValidator())  # Ensures input is an integer
        layout.addWidget(self.channel_number_input)

        # Controller IP Address (IP format)
        layout.addWidget(QLabel("Controller IP Address"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP Address (e.g., 192.168.0.1)")
        layout.addWidget(self.ip_input)

        # Submit Button
        submit_button = QPushButton("Submit")
        push_button = """ 
                QPushButton{ 
                border-radius:100px;
                border: 1px solid #0255ed; 
                background: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 1, 
                    stop: 0 rgba(16, 22, 29, 255), 
                    stop: 1 rgba(5, 17, 37, 255)
                );
                padding:5px;
                } 
                QPushButton:hover {background-color: #020d42;}
            """
        submit_button.setStyleSheet(push_button)
        submit_button.clicked.connect(self.submit_form)
        layout.addWidget(submit_button)

        self.setLayout(layout)
        self.setStyleSheet("""
                               QLineEdit { padding:6px; } ;
                               background-color: black;
                               """)

    def validate_ip(self, ip):
        parts = ip.split(".")
        if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
            return True
        return False

    def submit_form(self):
        name = self.name_input.text().strip()
        scp_number = self.scp_number_input.text().strip()
        channel_number = self.channel_number_input.text().strip()
        ip = self.ip_input.text().strip()

        # Validate required fields
        if not name or not scp_number or not channel_number or not ip:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        # Validate IP address format
        if not self.validate_ip(ip):
            QMessageBox.warning(self, "Input Error", "Invalid IP address format.")
            return

        # Print values if all inputs are valid
        print("Controller Name:", name)
        print("SCP Number:", scp_number)
        print("Channel Number:", channel_number)
        print("IP Address:", ip)
        try:
            res,data = create_controller(name,scp_number,channel_number,ip)
            if res:
                QMessageBox.information(self, "Success", "Controller registered successfully")
            else:
                QMessageBox.information(self, "Error", data)
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))
        self.accept()

class TempACRDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Temp ACR Calls")
        self.setGeometry(400, 300, 400, 300)

        layout = QVBoxLayout()

        # ACR Number input
        self.acr_number_input = QLineEdit()
        self.acr_number_input.setPlaceholderText("Enter ACR Number")
        layout.addWidget(QLabel("ACR Number"))
        layout.addWidget(self.acr_number_input)

        # ACR Mode dropdown
        self.acr_mode_dropdown = QComboBox()
        self.acr_mode_values = {
            "Disable the ACR, no REX": "1",
            "Unlock (unlimited access)": "2",
            "Locked (no access, REX active)": "3",
            "Facility code only": "4",
            "Card only": "5",
            "PIN only": "6",
            "Card and PIN required": "7",
            "Card or PIN required": "8"
        }
        self.acr_mode_dropdown.addItems(self.acr_mode_values.keys())
        layout.addWidget(QLabel("ACR Mode"))
        layout.addWidget(self.acr_mode_dropdown)

        # Time Period dropdown
        self.time_period_dropdown = QComboBox()
        self.time_period_values = {
            "1 min": 1,
            "3 min": 3,
            "5 min": 5,
            "10 min": 10,
            "30 min": 30,
            "60 min": 60
        }
        self.time_period_dropdown.addItems(self.time_period_values.keys())
        layout.addWidget(QLabel("Time Period (minutes)"))
        layout.addWidget(self.time_period_dropdown)

        # Controller selection
        controller_layout = QHBoxLayout()
        self.select_all_checkbox = QCheckBox("Select All Controllers")
        self.controller_dropdown = QComboBox()
        self.controller_dropdown.setPlaceholderText("Select Controller")

        # Add all controllers to the dropdown
        controllers = get_controllers()
        for controller in controllers:
            self.controller_dropdown.addItem(str(controller.scp_number))

        controller_layout.addWidget(self.controller_dropdown)
        controller_layout.addWidget(self.select_all_checkbox)
        layout.addWidget(QLabel("Select Controller"))
        layout.addLayout(controller_layout)

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.confirm_submission)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def confirm_submission(self):
        acr_number = self.acr_number_input.text()
        acr_mode_text = self.acr_mode_dropdown.currentText()
        acr_mode = self.acr_mode_values[acr_mode_text]
        time_period_text = self.time_period_dropdown.currentText()
        time_period = self.time_period_values[time_period_text]
        selected_controller = self.controller_dropdown.currentText() if not self.select_all_checkbox.isChecked() else "All Controllers"

        if not acr_number:
            QMessageBox.warning(self, "Input Error", "Please enter the ACR Number.")
            return

        # Show confirmation dialog
        reply = QMessageBox.question(
            self, "Confirm Action", 
            f"Are you sure you want to apply the following settings?\n\n"
            f"ACR Number: {acr_number}\n"
            f"ACR Mode: {acr_mode_text}\n"
            f"Time Period: {time_period_text}\n"
            f"Controller: {selected_controller}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            msg = ''
            if self.select_all_checkbox.isChecked():
                controllers = get_controllers()
                for controller in controllers:
                    res, msgg = change_ACR(acr_number, acr_mode, str(controller.scp_number), str(time_period))
                    msg += f"{controller.name} Temp ACR Changed" if res else f'Error: {controller.name}, {msgg} \n '
                    print(acr_mode, acr_number, controller.scp_number, time_period)
            else:
                controller = get_controller(None, selected_controller)
                res, msgg = change_ACR(acr_number, acr_mode, str(controller.scp_number), str(time_period))
                msg += f"{controller.name} Temp ACR Changed" if res else f'Error: {controller.name}, {msgg} \n '
                print(acr_mode, acr_number, controller.scp_number, time_period)
            
            QMessageBox.information(self, "ACR Mode", msg)
            self.accept()

class ChangeACRDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change ACR")
        self.setGeometry(400, 300, 400, 300)

        layout = QVBoxLayout()

        # ACR Number input
        self.acr_number_input = QLineEdit()
        self.acr_number_input.setPlaceholderText("Enter ACR Number")
        layout.addWidget(QLabel("ACR Number"))
        layout.addWidget(self.acr_number_input)

        # ACR Mode dropdown
        self.acr_mode_dropdown = QComboBox()
        self.acr_mode_values = {
            "Disable the ACR, no REX": "1",
            "Unlock (unlimited access)": "2",
            "Locked (no access, REX active)": "3",
            "Facility code only": "4",
            "Card only": "5",
            "PIN only": "6",
            "Card and PIN required": "7",
            "Card or PIN required": "8"
        }
        self.acr_mode_dropdown.addItems(self.acr_mode_values.keys())
        layout.addWidget(QLabel("ACR Mode"))
        layout.addWidget(self.acr_mode_dropdown)

        # Controller selection
        controller_layout = QHBoxLayout()
        self.select_all_checkbox = QCheckBox("Select All Controllers")
        self.controller_dropdown = QComboBox()
        self.controller_dropdown.setPlaceholderText("Select Controller")

        # Add all controllers to the dropdown
        controllers = get_controllers()
        for controller in controllers:
            self.controller_dropdown.addItem(str(controller.scp_number))

        controller_layout.addWidget(self.controller_dropdown)
        controller_layout.addWidget(self.select_all_checkbox)
        layout.addWidget(QLabel("Select Controller"))
        layout.addLayout(controller_layout)

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.confirm_submission)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def confirm_submission(self):
        acr_number = self.acr_number_input.text()
        acr_mode_text = self.acr_mode_dropdown.currentText()
        acr_mode = self.acr_mode_values[acr_mode_text] 
        selected_controller = self.controller_dropdown.currentText() if not self.select_all_checkbox.isChecked() else "All Controllers"

        if not acr_number:
            QMessageBox.warning(self, "Input Error", "Please enter the ACR Number.")
            return

        # Show confirmation dialog
        reply = QMessageBox.question(
            self, "Confirm Action", 
            f"Are you sure you want to apply the following settings?\n\n"
            f"ACR Number: {acr_number}\n"
            f"ACR Mode: {acr_mode_text}\n"
            f"Controller: {selected_controller}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            msg = ''
            if self.select_all_checkbox.isChecked():
                controllers = get_controllers()
                for controller in controllers:
                    res,msgg = change_ACR(acr_number,acr_mode,str(controller.scp_number))
                    msg += f"{controller.name} ACR Changed" if res else f'Error: {controller.name} , {msgg} \n'
                    print(acr_mode,  acr_number , controller.scp_number)
            else:
                controller = get_controller(None,selected_controller)
                res,msgg = change_ACR(acr_number,acr_mode,str(controller.scp_number))
                msg += f"{controller.name} ACR Changed" if res else f'Error: {controller.name} , {msgg} \n '
                print(acr_mode,  acr_number , controller.scp_number)
            QMessageBox.information(self, "ACR Mode ",msg)
            self.accept() 

class SimulateDialog(QDialog):
    def __init__(self, controllers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Simulate Actions")
        self.setGeometry(300, 300, 400, 300)

        # Main layout
        main_layout = QVBoxLayout()

        # Button layout
        button_layout = QHBoxLayout()

        # Set Time button
        # QPushButton.setStyleSheet(CSS)
        self.set_time_button = QPushButton("Set Time")
        self.set_time_button.setObjectName("setTimeButton")
        # self.set_time_button.setGraphicsEffect(SHADOW)
        self.set_time_button.clicked.connect(lambda: self._set_time())
        button_layout.addWidget(self.set_time_button)

        # Card Simulate button
        self.card_simulate_button = QPushButton("Card Simulate")
        self.card_simulate_button.clicked.connect(self.open_card_test_dialog)
        button_layout.addWidget(self.card_simulate_button)

        # Change ACR button
        self.change_acr_button = QPushButton("Change ACR")
        self.change_acr_button.clicked.connect(self.open_change_acr_dialog)
        button_layout.addWidget(self.change_acr_button)

        # Control Points button
        self.control_points_button = QPushButton("Control Points")
        self.control_points_button.clicked.connect(lambda: self.perform_action("Control Points"))
        button_layout.addWidget(self.control_points_button)

        # Temp ACR
        self.temp_ACR = QPushButton("Temp ACR")
        self.temp_ACR.clicked.connect(self.open_tmp_acr_dialog)
        button_layout.addWidget(self.temp_ACR)

        
        SHADOW = QGraphicsDropShadowEffect()
        SHADOW.setBlurRadius(30)
        SHADOW.setOffset(0, 0)
        SHADOW.setColor(QColor(0, 102, 204, 127))

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        self.setStyleSheet(BUTTON_CSS)
        self.setGraphicsEffect(SHADOW)

    def toggle_controller_selection(self, state):
        # If "Select All" is checked, disable the dropdown; otherwise, enable it
        self.controller_selector.setEnabled(state == Qt.CheckState.Unchecked)

    def perform_action(self, action_name):
        # Check if "Select All" is selected or specific controller
        # selected_controller = "All Controllers" if self.select_all_checkbox.isChecked() else self.controller_selector.currentText()
        
        # Process the action with the selected controller(s)
        print(f"Performing action: {action_name} on 123")
    
    def _set_time(self):
        try:
            controllers = get_controllers()
            message = ""
            if controllers:
                for controller in controllers:
                    if(set_time(controller)):
                        message+=f"{controller.scp_number} Time Set True \n"
                    else:
                        message+= f"Somwthing Went wrong with Controller {controller.scp_number} \n"
                QMessageBox.information(self, "Time Set", message)
        except Exception as e:
            QMessageBox.information(self, "Time Set", str(e))
            print(str(e))

    def open_card_test_dialog(self):
        dialog = CardTestDialog(self)
        if dialog.exec():
            pass 
    
    def open_change_acr_dialog(self):
        dialog = ChangeACRDialog(self)
        dialog.exec()

    def open_tmp_acr_dialog(self):
        dialog = TempACRDialog(self)
        dialog.exec()

class ActionDialog(QDialog):
    def __init__(self, file_id, controllers, parent=None):
        super().__init__(parent)
        self.file_id = file_id
        self.controllers = controllers

        self.setWindowTitle("File Actions")
        self.setGeometry(400, 300, 400, 200)

        layout = QVBoxLayout()

        # Add the Delete Record button
        self.delete_button = QPushButton("Delete Record")
        self.delete_button.clicked.connect(self.delete_record)
        layout.addWidget(self.delete_button)

        # Add the Apply File button
        self.apply_button = QPushButton("Apply File")
        self.apply_button.clicked.connect(self.apply_file)
        layout.addWidget(self.apply_button)

        # Dropdown for controller selection (only for Apply File)
        self.controller_selector = QComboBox()
        for controller in self.controllers:
            self.controller_selector.addItem(controller.name, controller.id)
        self.controller_selector.setEnabled(False)  # Initially disabled
        layout.addWidget(QLabel("Select Controller"))
        layout.addWidget(self.controller_selector)

        # "Select All" checkbox
        self.select_all_checkbox = QCheckBox("Select All Controllers")
        self.select_all_checkbox.stateChanged.connect(self.toggle_controller_selection)
        layout.addWidget(self.select_all_checkbox)

        self.setLayout(layout)

    def toggle_controller_selection(self):
        # Enable or disable controller dropdown based on "Select All" checkbox
        if self.select_all_checkbox.isChecked():
            self.controller_selector.setEnabled(False)
        else:
            self.controller_selector.setEnabled(True)

    def delete_record(self):
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Delete Record", "Are you sure you want to delete this record?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Response", delete_config_record(db,self.file_id))

    def apply_file(self):
        selected_controller = None
        if not self.select_all_checkbox.isChecked():
            selected_controller = self.controller_selector.currentData()  # Get selected controller ID
        # Call function to apply file to the selected controller(s)
        self.apply_file_to_controller(self.file_id, selected_controller)
        self.accept()
    
    def apply_file_to_controller(self, file_id, controller_id=None):
        file = get_config_file_by_id(db,file_id)
        if controller_id and file:
            controller = get_controller(controller_id)
            if controller:
                result,response = config_controller(controller,file)
                QMessageBox.information(self, f"Configure {result}", response)
            else:
                QMessageBox.information(self, "Error", "Controller SCP not found in Database. Please register the controller first")
        elif file:
            controllers = get_controllers()
            if controllers:
                message = ""
                for controller in controllers:
                    result,response = config_controller(controller,file)
                    message += f"{controller.scp_number} | {controller.name} => {result} \n"
                QMessageBox.information(self, "Config All Controllers", message)
        else:
            QMessageBox.information(self, "Error", f"Config file not found")

class InitializeDeviceDialog(QDialog):
    def __init__(self, db: Session, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Initialize Device")
        self.setGeometry(300, 300, 600, 500)
        self.db = db
        self.file_path = None

        layout = QVBoxLayout()

        self.file_button = QPushButton("Select .ini File")
        self.file_button.clicked.connect(self.select_ini_file)
        layout.addWidget(self.file_button)

        self.upload_button = QPushButton("Upload File")
        self.upload_button.setVisible(False)
        self.upload_button.clicked.connect(self.upload_ini_file)
        layout.addWidget(self.upload_button)

        self.file_content_display = QTextEdit()
        self.file_content_display.setReadOnly(True)
        layout.addWidget(self.file_content_display)

        self.db_files_table = QTableWidget()
        self.db_files_table.setColumnCount(4)  
        self.db_files_table.setHorizontalHeaderLabels(["File Name", "Purpose", "Notes", "Uploaded On"])
        layout.addWidget(self.db_files_table)
        self.update_db_files_list()

        self.setLayout(layout)

    def select_ini_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open .ini File", "", "INI Files (*.ini)")
        if file_path:
            if not file_path.lower().endswith('.ini'):
                QMessageBox.warning(self, "Invalid File", "Please select a file with a .ini extension.")
                return
            
            self.file_path = file_path
            self.upload_button.setVisible(True)  # Show the upload button

            # Read and display the file content as plain text
            with open(file_path, 'r') as file:
                content = file.read()
            
            self.file_content_display.setText(content)

    def upload_ini_file(self):
        if self.file_path:
            with open(self.file_path, 'r') as file:
                content = file.read()
            upload_file(file_name=self.file_path.split("/")[-1], file_content=content, purpose="General", notes="Uploaded via GUI")
            self.update_db_files_list()
    
    def update_db_files_list(self):
        # Retrieve all uploaded files from the database
        files = get_all_files()

        # Set the table row count based on number of files
        self.db_files_table.setRowCount(len(files))
        self.db_files_table.setColumnCount(5)  # Add an extra column for "Action"
        self.db_files_table.setHorizontalHeaderLabels(["File Name", "Purpose", "Notes", "Uploaded On", "Action"])

        # Populate the table with file details and add an action button
        for row, file in enumerate(files):
            self.db_files_table.setItem(row, 0, QTableWidgetItem(file.file_name))
            self.db_files_table.setItem(row, 1, QTableWidgetItem(file.purpose))
            self.db_files_table.setItem(row, 2, QTableWidgetItem(file.notes or ""))
            self.db_files_table.setItem(row, 3, QTableWidgetItem(file.uploaded_on.strftime("%Y-%m-%d %H:%M:%S")))

            # Create an action button
            action_button = QPushButton("Action")
            action_button.clicked.connect(lambda checked, file_id=file.id: self.open_action_window(file_id))
            self.db_files_table.setCellWidget(row, 4, action_button)
        
    def open_action_window(self, file_id):
        controllers = get_controllers()  # Assume get_all_controllers fetches all controllers from the DB
        dialog = ActionDialog(file_id, controllers, self)
        dialog.exec()

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
        self.setGeometry(300, 300, 400, 300)
        container = QWidget(self)
            
        layout = QVBoxLayout(container)

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

        # Dropdown for selecting controllers
        controllers = get_controllers()
        self.controllers = controllers
        self.controller_selector = QComboBox()
        self.controller_selector.setStyleSheet("padding:6px;")
        for controller in controllers:
            self.controller_selector.addItem(str(controller.scp_number))
        layout.addWidget(QLabel("Select Controller"))
        layout.addWidget(self.controller_selector)

        # Select All Checkbox
        self.select_all_checkbox = QCheckBox("Select All Controllers")
        self.select_all_checkbox.stateChanged.connect(self.toggle_controller_selection)
        layout.addWidget(self.select_all_checkbox)
        push_button = """ 
                QPushButton{ 
                border-radius:100px;
                border: 1px solid #0255ed; 
                background: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 1, 
                    stop: 0 rgba(16, 22, 29, 255), 
                    stop: 1 rgba(5, 17, 37, 255)
                );
                padding:5px;
                } 
                QPushButton:hover {background-color: #020d42;}
            """
        # Submit Button
        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet(push_button)
        submit_button.clicked.connect(self.submit_card_info)
        layout.addWidget(submit_button)

        self.setLayout(layout)
        self.setStyleSheet("""
                            QLineEdit { padding:6px; } ;
                            QComboBox { padding:6px; } ;
                            background-color: black;
                            """)

    def toggle_controller_selection(self, state):
        self.controller_selector.setEnabled(state == Qt.CheckState.Unchecked)

    def submit_card_info(self):
        card_number = self.card_number_input.text().strip()
        facility_code = self.facility_code_input.text().strip()
        acr_number = self.acr_number.text().strip()

        if not card_number or not facility_code:
            self.show_alert("Input Error", "Please fill all fields before submitting.")
            return

        message = ""
        if self.select_all_checkbox.isChecked():
            for controller in self.controllers:
                success, message_rec = card_test(db, card_number, facility_code, acr_number, controller.scp_number)
                if (success): message += f"Controller: {controller.scp_number} -> True \n"
                else:message += f"Controller: {controller.scp_number} -> False \n"
            QMessageBox.information(self, "Card Test Results",message)
        else:
            for controller in self.controllers:
                print(self.controller_selector.currentText(), "       ",controller.scp_number)
                if (self.controller_selector.currentText()) == str(controller.scp_number):
                    success, message_rec = card_test(db, card_number, facility_code, acr_number, controller.scp_number)
            if success:
                QMessageBox.information(self, "Card Test",message_rec)
            else:
                QMessageBox.information(self, "Card Test Fail",message_rec)
     
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
            self.setGeometry(300, 300, 400, 500)

            # Main layout container widget
            container = QWidget(self)
            # container.setStyleSheet("background-color: black;")  # Apply background color to the container

            # Main layout
            layout = QVBoxLayout(container)
            layout.setContentsMargins(10, 10, 10, 10)  # Set margins to avoid sticking to the edges
            
            SHADOW = QGraphicsDropShadowEffect()
            SHADOW.setBlurRadius(30)
            SHADOW.setOffset(0, 0)
            SHADOW.setColor(QColor(0, 102, 204, 127))
            
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
            self.controller_selector.setStyleSheet("padding:6px;")
            
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
            push_button = """ 
                QPushButton{ 
                border-radius:100px;
                border: 1px solid #0255ed; 
                background: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 1, 
                    stop: 0 rgba(16, 22, 29, 255), 
                    stop: 1 rgba(5, 17, 37, 255)
                );
                padding:5px;
                } 
                QPushButton:hover {background-color: #020d42;}
            """
            submit_button.setStyleSheet(push_button)
            submit_button.clicked.connect(self.submit_card_info)
            layout.addWidget(submit_button)
            
            self.setLayout(layout)
            self.setStyleSheet("""
                               QLineEdit { padding:6px; } ;
                               QComboBox { padding:6px; } ;
                               background-color: black;
                               """)
            # self.setStyleSheet("")
            # self.setStyleSheet("")
            
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
        self.setObjectName("mainBody") 
        self.setStyleSheet(""" #mainBody { background: qlineargradient(spread: pad, x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 rgba(16, 22, 29, 255),stop: 1 rgba(5, 17, 37, 255));}""")
        _initialise_driver_(self)

    def init_ui(self):
        self.setWindowTitle('HID Aero X1100 Simulator')
        self.setGeometry(100, 100, 1200, 800)  # Larger canvas
        self.showMaximized()
        # Main layout (divided into three sections: left (buttons), right (controllers), and bottom (log))
        main_layout = QVBoxLayout()

        # Top section: Contains control buttons and HID controllers
        top_section_layout = QHBoxLayout()
        background_image="""
                QGroupBox{
                background-image: url('assets/images/3.png');
                border:2px solid #07016e;
                border-radius:10px ;
                }
                QPushButton {
                    padding: 10px;
                    width: 100px;
                   
                    border-radius: 0px;  
                    background-color: red; 
                    color: white;
                }
                QPushButton:hover {
                    background-color: red; 
                }
        """
        push_button = """ 
            QPushButton{ 
            border-radius:100px;
            border: 1px solid #0255ed; 
            background: qlineargradient(
                spread: pad, x1: 0, y1: 0, x2: 1, y2: 1, 
                stop: 0 rgba(16, 22, 29, 255), 
                stop: 1 rgba(5, 17, 37, 255)
            );
            } 
            QPushButton:hover {background-color: #020d42;}
         """
        # Left: Control Buttons section layout
        control_group = QGroupBox("Control Button")
        control_group.setStyleSheet(background_image)
        # control_box_layout = QVBoxLayout()
        control_grid_layout = QGridLayout()
        # control_grid_layout.setContentsMargins(1, -100, 0, 0) 
     

        # Control Buttons: Adding the buttons into the control box
        connect_button = QPushButton('Connect to Device')
        disconnect_button = QPushButton('Register Controller')
        initialize_button = QPushButton('Initialize Device')
        card_test_button = QPushButton('Card Test')
        add_card_button = QPushButton('Add Card')
        simulate_controller = QPushButton('Simulate Controller')
        some_other_button = QPushButton('Other Action')
        # connect_button.setStyleSheet()

        for button in [connect_button, disconnect_button, initialize_button,card_test_button, add_card_button, simulate_controller, some_other_button]:
            SHADOW = QGraphicsDropShadowEffect()
            SHADOW.setBlurRadius(30)
            SHADOW.setOffset(0, 0)
            SHADOW.setColor(QColor(0, 102, 204, 127))
            button.setStyleSheet(push_button)
            button.setGraphicsEffect(SHADOW)
            button.setFixedSize(170, 50)

        # Add buttons to the layout
        control_grid_layout.addWidget(connect_button, 0, 0)
        control_grid_layout.addWidget(disconnect_button, 0, 1)
        control_grid_layout.addWidget(initialize_button, 0, 2)
        control_grid_layout.addWidget(card_test_button, 1, 0)
        control_grid_layout.addWidget(add_card_button, 1, 1)
        control_grid_layout.addWidget(simulate_controller, 1, 2)
        control_grid_layout.addWidget(some_other_button, 2, 0)


        control_group.setLayout(control_grid_layout)
        # Connect the button click to a function
        connect_button.clicked.connect(lambda: connect_to_all(self))
        add_card_button.clicked.connect(self.open_add_card_dialog)
        disconnect_button.clicked.connect(self.open_controller_form)
        card_test_button.clicked.connect(self.open_card_test_dialog)
        some_other_button.clicked.connect(self.open_transaction_log_dialog)
        initialize_button.clicked.connect(self.open_initialize_device_dialog)
        simulate_controller.clicked.connect(self.open_simulate_dialog)


        # Add chart below the control buttons
        chart_group = QGroupBox("Statistics Chart")
        chart_layout = QVBoxLayout()

        # # Create a sample bar chart
        # bar_set = QBarSet("Values")
        # bar_set.append([1, 2, 3, 4, 5, 6])

        # series = QBarSeries()
        # series.append(bar_set)

        # chart = QChart()
        # chart.addSeries(series)
        # chart.setTitle("Controller Statistics")
        # chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # chart_view = QChartView(chart)
        # chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        # chart_view.setMaximumSize(600, 300)
        # chart_layout.addWidget(chart_view)
        

        # chart_group.setLayout(chart_layout)
        
        # Left side layout
        left_side_layout = QVBoxLayout()
        left_side_layout.addWidget(control_group)
        # left_side_layout.addWidget(chart_group)



        # Right: HID Controllers section
        controllers_group = QGroupBox("HID Controllers")
        controllers_group.setStyleSheet(background_image)
        device_layout = QGridLayout()

        controllers = get_controllers()
        for i,controller in enumerate(controllers): 
            device_frame = QFrame()
            device_frame.setObjectName("controller_frame")
            device_frame.setFrameShape(QFrame.Shape.Box)
            device_frame.setLineWidth(2)
            device_frame.setFixedSize(250, 170)
            

            # style
            
            box_shadow = QGraphicsDropShadowEffect()
            box_shadow.setBlurRadius(30)
            box_shadow.setOffset(0, 0)
            box_shadow.setColor(QColor(0, 102, 204, 127))


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

            device_frame.setGraphicsEffect(box_shadow)
            device_frame.setStyleSheet(CTRL_CSS)


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
        SHADOW = QGraphicsDropShadowEffect()
        SHADOW.setBlurRadius(30)
        SHADOW.setOffset(0, 0)
        SHADOW.setColor(QColor(0, 102, 204, 127))
        log_group.setGraphicsEffect(SHADOW)
        # log_group.setStyleSheet("""QGroupBox{ background-image: url('assets/images/3.png');""")
        # log_group.setStyleSheet("""QGroupBox{ background-color: #002b5c""")

        self.log_box = QTextEdit()  # Use self.log_box to access in other methods
        self.log_box.setPlaceholderText("Log details will be displayed here...")
        self.log_box.setStyleSheet("""QTextEdit{ background-image: url('assets/images/3.png'); 
                                  
                                    background-position: center;
                                    background-size: cover;
                                    background-attachment: fixed; 
                                   padding:5px }}""")
        log_group_layout = QVBoxLayout()
        log_group_layout.addWidget(self.log_box)
        log_group.setLayout(log_group_layout)
        log_group.setFixedHeight(150)  # Set fixed height for the log output

        # Add the left (buttons) and right (controllers) sections to the top section
        top_section_layout.addLayout(left_side_layout)
        # top_section_layout.addWidget(control_group)  # Add control buttons on the left
        top_section_layout.addWidget(controllers_group)  # Add HID controllers on the right

        # Add the top section and bottom section to the main layout
        main_layout.addLayout(top_section_layout)  # Top section with buttons and controllers
        main_layout.addWidget(log_group)  # Bottom section with log output

        self.setLayout(main_layout)
    
    def open_simulate_dialog(self):
        controllers = ["Controller 1", "Controller 2", "Controller 3"]  # Replace with actual controller data
        dialog = SimulateDialog(controllers, self)
        dialog.exec()

    def open_controller_form(self):
        dialog = AddControllerDialog(self)
        dialog.exec()

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
        controllers = get_controllers() 
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

    def open_initialize_device_dialog(self):
        # Open the dialog to initialize the device
        dialog = InitializeDeviceDialog(self)
        dialog.exec()

           
def main():
    app = QApplication([])
    window = HIDSimulator()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
