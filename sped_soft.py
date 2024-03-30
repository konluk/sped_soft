import datetime
import sys
import os
import csv

from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QCheckBox, QApplication, \
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QLabel, QLineEdit, QFrame, QMessageBox
from PyQt5.QtCore import Qt

from geo_tools import *
from sped_data_tools import *

filename = "sped_data.csv"


class CenteredCheckBox(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Use Qt module to access AlignCenter
        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sped Beky")
        self.setGeometry(100, 100, 700, 700)  # Increased window height for the text area

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Section One
        self.section_one_label = QLabel("<b>ADD TRANSPORT</b>")
        self.layout.addWidget(self.section_one_label)

        self.section_one = QWidget()
        self.layout.addWidget(self.section_one)

        self.section_one_layout = QHBoxLayout()
        self.section_one.setLayout(self.section_one_layout)

        self.s1_label1 = QLabel("CLIENT ID:")
        self.s1_textbox_client = QLineEdit()
        self.s1_label2 = QLabel("ZIP FROM:")
        self.s1_textbox_zip_from = QLineEdit()
        self.s1_label3 = QLabel("ZIP TO:")
        self.s1_textbox_zip_to = QLineEdit()
        self.s1_button1 = QPushButton("ADD")
        self.s1_button1.clicked.connect(self.add_new_transport)

        self.section_one_layout.addWidget(self.s1_label1)
        self.section_one_layout.addWidget(self.s1_textbox_client)
        self.section_one_layout.addWidget(self.s1_label2)
        self.section_one_layout.addWidget(self.s1_textbox_zip_from)
        self.section_one_layout.addWidget(self.s1_label3)
        self.section_one_layout.addWidget(self.s1_textbox_zip_to)
        self.section_one_layout.addWidget(self.s1_button1)

        # Line Separator
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.line)

        # Section Two
        self.section_two_label = QLabel("<b>FIND CLIENT</b>")
        self.layout.addWidget(self.section_two_label)

        self.section_two = QWidget()
        self.layout.addWidget(self.section_two)

        self.section_two_layout = QHBoxLayout()
        self.section_two.setLayout(self.section_two_layout)

        self.s2_label3 = QLabel("ZIP CODE:")
        self.s2_textbox3 = QLineEdit()
        self.s2_button2 = QPushButton("FIND")
        self.s2_button2.clicked.connect(self.submit_section_two)

        self.section_two_layout.addWidget(self.s2_label3)
        self.section_two_layout.addWidget(self.s2_textbox3)
        self.section_two_layout.addWidget(self.s2_button2)

        # Large Table Area
        self.large_text_label = QLabel("<b>FINDED TRANSPORTS</b>")
        self.layout.addWidget(self.large_text_label)
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.show_all_transport()

    # Button ADD
    def add_new_transport(self):
        try:
            client_id = self.s1_textbox_client.text().strip()
            zip_from = self.s1_textbox_zip_from.text().strip()
            zip_to = self.s1_textbox_zip_to.text().strip()
            date = datetime.datetime.now().strftime("%Y%m%d")

            if client_id is None or zip_from is None or zip_to is None:
                QMessageBox.information(self, "ERR", "NOT ALL BOX FILLED")


            print(client_id, zip_from, zip_to, date)

            get_location_info(zip_from)
            get_location_info(zip_to)

            return
        except Exception as e:
            QMessageBox.information(self, "ERR", str(e))

            """
            if client_id and zip_code:
                zip_code = fix_zip_code(zip_code)
                city = get_city_from_zip(zip_code)
                lat, lon = get_coordinates(zip_code)
                file_text = client_id + "," + zip_code + "," + city + "," + str(lat) + "," + str(lon) + "," + date
                if os.path.exists(filename):
                    with open(filename, 'a') as file:
                        file.write('\n' + file_text)
                else:
                    with open(filename, 'w') as file:
                        file.write(file_text)
                self.textbox1.clear()
                self.textbox2.clear()
            else:
                QMessageBox.information(self, "ERR", "CLIENT ID OR ZIP CODE IS EMPTY")
            """

    # Button FIND
    def submit_section_two(self):
        self.add_to_tab()
        return
        try:
            search_zip_code = self.textbox3.text()
            search_zip_code = "SK 95176"
            if(search_zip_code):
                search_zip_code = fix_zip_code(search_zip_code)
                search_city = get_city_from_zip(search_zip_code)
                search_lat, search_lon = get_coordinates(search_zip_code)

                arr_with_distance = []
                # Open the CSV file
                with open(filename, mode='r') as file:
                    csv_reader = csv.reader(file)
                    # Iterate over each row in the CSV file
                    for f_client_id, f_zip_code, f_city, f_lat, f_lon, f_date in csv_reader:
                        distance_between_zip = haversine(search_lat, search_lon, f_lat, f_lon)
                        arr_with_distance.append([int(distance_between_zip), f_zip_code, f_city, f_client_id])

                print(arr_with_distance)

                # Sort the list based on the first attribute (number)
                sorted_list = sorted(arr_with_distance, key=lambda x: x[0])

                print(sorted_list)

                self.large_text.clear()
                self.large_text.append(f"<b>SEARCHED ZIP:</b> {search_zip_code} / {search_city} \n\n")
                out_text =""
                line = False
                # Print the sorted list
                for i, transport in enumerate(sorted_list):
                    distance = int(transport[0])
                    if distance > 100 and line == False:
                        line = True
                        self.large_text.append("------------------------------------------------------------------")

                    formatted_order = f"{str(i+1).ljust(3)}"
                    formatted_distance = f"{str(distance).ljust(5)}"

                    print(formatted_distance + "A")

                    self.large_text.insertHtml(f'{formatted_order}. <b>KM:</b> {formatted_distance}, <b>CLIENT: </b>{transport[1]}, <b>ZIP: </b>{transport[2]} / {transport[3]}')
                    #formated_transport_text = f'<b>hh </b> \n'


                    #out_text = out_text + str(item) + "\n"
                #print(out_text)


                return



            else:
                self.large_text.clear()
                self.large_text.setText("nieco sem dame")


        except Exception as e:
            QMessageBox.information(self, "ERR", str(e))

    # Add data to table by table type
    def fill_table(self, table_type, data):
        self.table.clear()

        # Set number of rows and columns based on data
        num_rows = len(data)
        num_columns = len(data[0])

        if table_type == "search":
            headers = ["Distance", "Zip", "Location", "Client", "Sent", "Rejected"]
            num_columns += 2  # Add 2 columns for checkboxes
            max_widths = [20, 100, 200, 200, 10, 10]
        else:
            headers = ["Client", "Zip", "Location", "Lat/Lon", "Created date"]
            max_widths = [200, 100, 200, 100, 100]

        self.table.setRowCount(num_rows)
        self.table.setColumnCount(num_columns)
        self.table.setHorizontalHeaderLabels(headers)

        # Populate table with data and checkboxes
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(item)))

            # Add checkboxes to the last two columns
            if table_type == "search":
                checkbox1 = CenteredCheckBox()
                checkbox2 = CenteredCheckBox()
                self.table.setCellWidget(i, num_columns - 2, checkbox1)
                self.table.setCellWidget(i, num_columns - 1, checkbox2)

        # Adjust column widths based on content
        for col in range(num_columns):
            width = min(max_widths[col], self.table.columnWidth(col))
            self.table.setColumnWidth(col, width)

    # Show all transport
    def show_all_transport(self):
        data = get_all_transports()
        if data:
            self.fill_table(table_type="all", data=data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
