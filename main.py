# -*- coding: utf-8 -*-
"""
Multiplication app
"""
from __future__ import print_function

import sys
from PyQt4 import Qt, QtCore, QtGui
from PyQt4.QtCore import pyqtSlot
from random import randrange

personal_score = 0
attempts = 0


def new_operation():
    global first_number
    global second_number
    global operation
    global operand_result

    first_number = randrange(10)
    secondumber = randrange(10)
    operation = str(first_number) + 'x' + str(second_number)
    operand_result = first_number*second_number


class Computer(QtGui.QWidget):
    
    def __init__(self):

        new_operation()

        # Initialize the object as a QWidget and set its title and minimum width
        QtGui.QWidget.__init__(self)
        self.setWindowTitle(u"Fais fonctionner tes méninges !")
        self.setMinimumSize(640, 400)
        
        # Create the QVBoxLayout that lays out the whole elements
        self.layout = QtGui.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        # Create main zone, with start button and count zone
        self.menu = QtGui.QHBoxLayout()
        # Create the question line with label and line edit
        self.question_line = QtGui.QHBoxLayout()
        self.question_line.setMargin(0)
        # Create right button
        self.button_box = QtGui.QHBoxLayout()
        self.button_box.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.button_box.setAlignment(QtCore.Qt.AlignRight)
        # Create box for displaying result logic
        self.results = QtGui.QHBoxLayout()
        self.results.setAlignment(QtCore.Qt.AlignCenter)
        # Create box for image
        self.image = Qt.QHBoxLayout()
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        # Create box for "one more" button
        self.retry = Qt.QHBoxLayout()
        self.retry.setAlignment(QtCore.Qt.AlignCenter)

        # Define all elements
        # Start new game button
        self.button_start = QtGui.QPushButton('Start new game', self)
        self.button_start.setMaximumWidth(120)
        self.button_start.value = 1
        self.button_start.clicked.connect(self.make_reset_app)
        # Score
        self.score = Qt.QLabel(str(personal_score) + '/' + str(attempts))
        self.score.setAlignment(QtCore.Qt.AlignRight)
        # Line with question label and line edit for user answer
        self.question_label = QtGui.QLabel(operation)
        self.question_label.setMaximumWidth(50)
        self.question = QtGui.QLineEdit(self)
        self.question.setPlaceholderText('What about the result, huh ?')
        # Create White line to avoid content up on button hide
        self.fix_button_position = QtGui.QLabel('')
        self.fix_button_position.setMinimumHeight(30)
        # Create the build button with its caption
        self.build_button = QtGui.QPushButton('Verify !', self)
        self.build_button.setMaximumWidth(100)
        self.build_button.clicked.connect(self.show_result)
        # Create the area for displaying results, hidden by default
        self.result = QtGui.QLabel('')
        self.result.hide()
        # Display congrats or retry image, hidden by default
        self.result_image = QtGui.QLabel('')
        self.result_image.hide()
        # Add next button, hidden by default
        self.button_retry = QtGui.QPushButton('Next operation !', self)
        self.button_retry.value = 0
        self.button_retry.clicked.connect(self.make_reset_app)
        self.button_retry.hide()

        # Add all widgets
        self.menu.addWidget(self.button_start)
        self.menu.addWidget(self.score)
        self.question_line.addWidget(self.question_label)
        self.question_line.addWidget(self.question)
        self.button_box.addWidget(self.fix_button_position)
        self.button_box.addWidget(self.build_button)
        self.results.addWidget(self.result)
        self.image.addWidget(self.result_image)
        self.retry.addWidget(self.button_retry)
        
        # Add layouts to main layout
        self.layout.addLayout(self.menu)
        self.layout.addLayout(self.question_line)
        self.layout.addLayout(self.button_box)
        self.layout.addLayout(self.results)
        self.layout.addLayout(self.image)
        self.layout.addLayout(self.retry)

        # Set the VBox layout as the window's main layout
        self.setLayout(self.layout)

    def show_result(self):
        ''' Apply logic and show results '''
        # Get user answer
        answer = self.question.text()
        if answer == '':
            self.result.setText('Hum... Did you click by mistake ?')
            self.result_image.hide()
            self.button_retry.hide()
        else:
            try:
                answer = int(answer)
                self.result.setText('You said ' + str(answer) + ', result was ' + str(operand_result))
                if int(answer) == int(operand_result):
                    # Update score
                    global personal_score
                    personal_score += 1
                    image = 'well-done.png'
                else:
                    image = 'hum.png'

                # Hide buttons and clear elements
                self.build_button.hide()
                # Clear and Disable QLineEdit
                self.question.clear()
                self.question.setDisabled(1)
                # Display result image and button for new question
                img = QtGui.QPixmap()
                img.load('./img/'+image)
                self.result_image.setPixmap(img.scaled(200, 200, QtCore.Qt.KeepAspectRatio))
                self.result_image.show()
                self.button_retry.show()
            except ValueError:
                self.result.setText('Hum... Why not try with numbers ?')

            # Update attempts
            global attempts
            attempts += 1
            self.score.setText(str(personal_score) + '/' + str(attempts))
        
        # In all cases, show text message
        self.result.show()

    @pyqtSlot()
    def make_reset_app(self):

        source = self.sender()

        if source.value == 1:
            global personal_score
            global attempts
            personal_score = 0
            attempts = 0
            self.score.setText('0/0')

        self.question.clear()
        self.question.setDisabled(0)
        self.result.hide()
        self.result_image.hide()
        self.button_retry.hide()
        self.build_button.show()
        # New operation
        new_operation()
        self.question_label.setText(operation)

    # TODO : connect this function to the app
    def query_exit(self):
        exit = QtGui.QMessageBox.information(self,
                                        "Quit...",
                                        "Do you really want to quit ?",
                                        "&Ok",
                                        "&Cancel",
                                        "", 0, 1)
        if exit == 0:
            qt_app.quit()

    def run(self):
        # show the layout
        self.show()
        # Run the qt application
        qt_app.exec_()
        sys.exit()


# Create an instance of the application and run it
if __name__ == "__main__":
    qt_app = Qt.QApplication(sys.argv)
    Qt.QApplication.setStyle("plastique")
    app = Computer()
    app.run()