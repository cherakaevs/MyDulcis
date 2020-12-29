from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QSlider, QColorDialog, QDockWidget
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        #Инициализируем главное окно
        title = "Dulcis"
        top = 0
        left = 0
        width = 1900
        height = 1000

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon('donut.ico'))

        #Создаем пустое изображение, которое будем использовать в качестве холста
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.isActiveWindow()

        self.drawing = False
        self.brushSize = 7
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
        self.brush = None

        #Создаем док-виджет для изменения толщины грифеля карандаша
        self.dock = QDockWidget('Thickness')
        thickness = QSlider(Qt.Horizontal)
        thickness.setValue(7)
        thickness.setRange(3, 30)
        thickness.setTickInterval(1)
        thickness.setTickPosition(1)
        thickness.valueChanged.connect(self.thicknessChange)
        self.dock.setWidget(thickness)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock)
        self.dock.close()

        #Создаем главное меню и второстепенные, а также прописываем все действия при взаимодействии с элементами меню
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu(QIcon("icons/file.png"), "")

        saveAction = QAction(QIcon("icons/save.ico"), "Save", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction(QIcon("icons/clear.png"), "Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        colorSet = QAction(QIcon("icons/palette.png"), "", self)
        colorSet.setShortcut("Ctrl+P")
        mainMenu.addAction(colorSet)
        colorSet.triggered.connect(self.selectColor)

        thickAction = QAction(QIcon("icons/thickness.png"), "", self)
        thickAction.setShortcut("Ctrl+T")
        mainMenu.addAction(thickAction)
        thickAction.triggered.connect(lambda: self.dock.show())

        eraserAction = QAction(QIcon("icons/eraser.jpg"), "", self)
        eraserAction.setShortcut("Ctrl+E")
        mainMenu.addAction(eraserAction)
        eraserAction.triggered.connect(self.eraser)

        cnvsMenu = mainMenu.addMenu(QIcon("icons/canvas.jpg"), "")
        changeCnvsColor = QAction("Change color", self)
        changeCnvsColor.setShortcut("Alt+C")
        cnvsMenu.addAction(changeCnvsColor)
        changeCnvsColor.triggered.connect(self.cnvsColor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def selectColor(self):
        self.brushColor = QColorDialog.getColor()

    def thicknessChange(self, value):
        self.brushSize = value

    def cnvsColor(self):
        self.image.fill(QColorDialog.getColor())

    def eraser(self):
        self.brushColor = Qt.white

