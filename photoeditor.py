import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter

workdir = ""

class ImageProcessor:
    def __init__(self, image):
        self.image = image

    def do_mirror(self):
        return self.image.transpose(Image.FLIP_LEFT_RIGHT)

    def do_left(self):
        return self.image.rotate(90, expand=True)

    def do_right(self):
        return self.image.rotate(-90, expand=True)

    def do_sharpen(self):
        return self.image.filter(ImageFilter.SHARPEN)

    def do_bw(self):
        return self.image.convert('L')
class PhotoEditorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Photo Editor")
        self.setGeometry(100, 100, 400, 300)

        self.folder_button = QPushButton("Folder")
        self.image_label = QLabel("Picture")
        self.image_list = QListWidget()

        self.edit_buttons = {
            "Left": QPushButton("Left"),
            "Right": QPushButton("Right"),
            "Mirror": QPushButton("Mirror"),
            "Sharpness": QPushButton("Sharpness"),
            "B/w": QPushButton("B/w"),
            "Save": QPushButton("Save"),
            "Reset filters": QPushButton("Reset filters"),
        }

        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        self.main_layout.addWidget(self.folder_button)
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.image_list)

        for name, button in self.edit_buttons.items():
            button.clicked.connect(self.create_handler(name))
            self.button_layout.addWidget(button)

        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.folder_button.clicked.connect(self.showFilenamesList)
        self.current_image = None

    def chooseWorkdir(self):
        global workdir
        workdir = QFileDialog.getExistingDirectory(self, "Choose work folder:")
        return workdir

    def filter(self, filename):
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', )
        return filename.endswith(image_extensions)

    def showFilenamesList(self):
        self.chooseWorkdir()
        if workdir:
            self.image_list.clear()
            for filename in os.listdir(workdir):
                if self.filter(filename):
                    self.image_list.addItem(filename)
            self.image_list.itemClicked.connect(self.load_image)

    def load_image(self, item):
        filename = os.path.join(workdir, item.text())
        self.current_image = Image.open(filename)
        self.update_image_display()

    def update_image_display(self):
        if self.current_image:
            self.current_image.save('temp_image.png')
            pixmap = QPixmap('temp_image.png')
            self.image_label.setPixmap(pixmap)

    def create_handler(self, action):
        def handler():
            if self.current_image:
                processor = ImageProcessor(self.current_image)
                if action == "Mirror":
                    self.current_image = processor.do_mirror()
                elif action == "Left":
                    self.current_image = processor.do_left()
                elif action == "Right":
                    self.current_image = processor.do_right()
                elif action == "Sharpness":
                    self.current_image = processor.do_sharpen()
                elif action == "B/w":
                    self.current_image = processor.do_bw()
                self.update_image_display()
        return handler

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoEditorApp()
    window.show()
    sys.exit(app.exec_())