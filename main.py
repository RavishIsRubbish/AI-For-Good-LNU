import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QColorDialog, QGraphicsScene, \
    QGraphicsView, QToolBar, QFileDialog, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QPointF, QObject, QThread, pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen, QPixmap, QColor, QIcon
import sdxl


class ImageGenWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        image = sdxl.gen_image(self.prompt, "ugly proportions, shading, details, coloring, photorealistic")
        image.save("background.png")
        self.finished.emit()


class PaintApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Art Assistant")
        self.setWindowIcon(QIcon('main_icon.svg'))

        self.canvas = QGraphicsView()
        self.scene = QGraphicsScene()
        self.canvas.setScene(self.scene)

        self.color = Qt.black
        self.paint_opacity = 100
        self.brush_size = 5
        self.drawing = False
        self.is_control_pressed = False
        self.last_point = QPointF()

        self.setup_toolbar()

        self.setup_events()

        self.setCentralWidget(QWidget())
        layout = QVBoxLayout(self.centralWidget())
        layout.addWidget(self.canvas)

        self.background_image = QPixmap("background.png")
        self.scene.addPixmap(self.background_image)

    def setup_toolbar(self):
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.color_button = QPushButton(QIcon('color_picker.svg'), "Color Picker")
        self.color_button.clicked.connect(self.choose_color)
        self.toolbar.addWidget(self.color_button)

        self.clear_button = QPushButton(QIcon('clear_screen.svg'), "Clear Screen")
        self.clear_button.clicked.connect(self.clear_canvas)
        self.toolbar.addWidget(self.clear_button)

        self.generate_image_button = QPushButton("Generate AI Image")
        self.generate_image_button.clicked.connect(self.generate_image)
        self.toolbar.addWidget(self.generate_image_button)

        self.import_button = QPushButton(QIcon('image_import.svg'), "Import Image")
        self.import_button.clicked.connect(self.import_image)
        self.toolbar.addWidget(self.import_button)

        self.export_button = QPushButton(QIcon('image_export.svg'), "Export Image")
        self.export_button.clicked.connect(self.export_image)
        self.toolbar.addWidget(self.export_button)

    def setup_events(self):
        self.scene.mousePressEvent = self.mouse_press_event
        self.scene.mouseMoveEvent = self.mouse_move_event
        self.scene.mouseReleaseEvent = self.mouse_release_event

    def paint(self, event):
        pass

    def choose_color(self):
        color = QColorDialog.getColor(initial=self.color)
        if color.isValid():
            self.color = color

    def clear_canvas(self):
        self.scene.clear()

    def draw_background(self):
        self.background_image = QPixmap("background.png")
        self.scene.clear()
        self.scene.addPixmap(self.background_image)

    def generate_image(self):
        prompt, done = QtWidgets.QInputDialog.getText(self, "Generate AI Image", "Enter a prompt: ")
        if not done:
            return
        prompt = "Pose art, line art, only lines, black and white" + prompt
        print("generating image")

        self.thread = QThread()
        self.worker = ImageGenWorker(prompt)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.draw_background)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def import_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            pixmap = QPixmap(file_path)
            item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(item)

    def export_image(self):
        pixmap = self.canvas.grab()
        pixmap.save("drawing.png")

    def mouse_press_event(self, event):
        self.export_image()
        self.drawing = True
        self.last_point = event.scenePos()

    def mouse_move_event(self, event):
        if self.drawing:
            new_point = event.scenePos()
            self.draw_line(self.last_point, new_point)
            self.last_point = new_point

    def mouse_release_event(self, event):
        if self.drawing:
            self.drawing = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.is_control_pressed = True
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.is_control_pressed = False
        super().keyReleaseEvent(event)

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        if self.is_control_pressed:
            if delta > 0:
                self.paint_opacity = self.paint_opacity + 5
            else:
                self.paint_opacity = self.paint_opacity - 5
            return

        if delta > 0:
            self.brush_size = self.brush_size + 5
        else:
            self.brush_size = self.brush_size - 5
        super().wheelEvent(event)

    def draw_line(self, p1, p2):
        adjusted_color = QColor(self.color)
        adjusted_color.setAlpha(self.paint_opacity)

        pen = QPen(adjusted_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)


def main():
    app = QApplication(sys.argv)
    window = PaintApp()
    window.resize(1024, 1024)
    window.setWindowIcon(QIcon("main_icon.svg"))
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
