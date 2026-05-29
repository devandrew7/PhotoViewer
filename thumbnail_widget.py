import os
from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, QSize, Qt, QPoint, QRect
from PyQt6.QtGui import QImage, QPixmap, QImageReader
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QSizePolicy
from styles import IMAGE_CARD_STYLE, FOLDER_SEPARATOR_STYLE
from flow_layout import FlowLayout

class ThumbnailSignals(QObject):
    # Signals must be defined on a QObject subclass
    loaded = pyqtSignal(str, QImage, int, int) # path, image, orig_w, orig_h
    error = pyqtSignal(str, str) # path, error_msg

class ThumbnailLoaderRunnable(QRunnable):
    def __init__(self, image_path, target_size):
        super().__init__()
        self.image_path = image_path
        self.target_size = target_size
        self.signals = ThumbnailSignals()

    def run(self):
        try:
            reader = QImageReader(self.image_path)
            reader.setAutoTransform(True) # Handle EXIF rotation
            
            orig_size = reader.size()
            if not orig_size.isValid():
                raise ValueError("Invalid image dimensions")

            # Calculate scaled size preserving aspect ratio
            scaled_size = orig_size.scaled(self.target_size, Qt.AspectRatioMode.KeepAspectRatio)
            reader.setScaledSize(scaled_size)
            
            image = reader.read()
            if image.isNull():
                raise ValueError("Failed to decode image data")

            self.signals.loaded.emit(self.image_path, image, orig_size.width(), orig_size.height())
        except Exception as e:
            self.signals.error.emit(self.image_path, str(e))

class ThumbnailWidget(QWidget):
    clicked = pyqtSignal(str)
    double_clicked = pyqtSignal(str)

    def __init__(self, image_path, target_max_size=128, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.target_max_size = target_max_size
        self.filename = os.path.basename(image_path)
        
        self.loaded = False
        self.loading_started = False
        self.aspect_ratio = 1.0  # width / height (default 1.0)
        self.cached_qimage = None
        self.selected = False

        self.setObjectName("thumbnailCard")
        self.setStyleSheet(IMAGE_CARD_STYLE)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(6)

        # Image Container Label
        self.image_label = QLabel(self)
        self.image_label.setObjectName("imageLabel")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Setup static placeholder initially
        self.set_placeholder()
        self.layout.addWidget(self.image_label)

        # Filename Label
        self.filename_label = QLabel(self.filename, self)
        self.filename_label.setObjectName("filenameLabel")
        self.filename_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.filename_label.setWordWrap(True)
        # Elide or limit filename display to avoid excessive vertical growth
        self.layout.addWidget(self.filename_label)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_placeholder(self):
        # Elegant loading/placeholder look
        self.image_label.setText("🖼️\nLoading...")
        self.image_label.setStyleSheet("color: #71717a; font-size: 11px;")

    def load_thumbnail(self, thread_pool):
        if self.loaded or self.loading_started:
            return
        
        self.loading_started = True
        # Request a larger target size to support high-DPI and smooth scaling
        runnable = ThumbnailLoaderRunnable(self.image_path, QSize(self.target_max_size * 2, self.target_max_size * 2))
        runnable.signals.loaded.connect(self.on_thumbnail_loaded)
        runnable.signals.error.connect(self.on_thumbnail_error)
        thread_pool.start(runnable)

    def on_thumbnail_loaded(self, path, image, orig_w, orig_h):
        if path != self.image_path:
            return
        
        self.cached_qimage = image
        self.aspect_ratio = orig_w / orig_h if orig_h > 0 else 1.0
        self.loaded = True
        self.update_thumbnail_display()

    def on_thumbnail_error(self, path, error_msg):
        self.loaded = True # Stop attempting to load
        self.image_label.setText("⚠️\nError")
        self.image_label.setStyleSheet("color: #ef4444; font-size: 11px;")

    def update_thumbnail_display(self):
        if not self.loaded or self.cached_qimage is None:
            return

        # Calculate exact dimensions based on current target_max_size and aspect ratio
        if self.aspect_ratio >= 1.0:
            # Landscape
            w = self.target_max_size
            h = int(self.target_max_size / self.aspect_ratio)
        else:
            # Portrait
            h = self.target_max_size
            w = int(self.target_max_size * self.aspect_ratio)

        # Ensure minimal dimensions to keep UI consistent
        w = max(32, w)
        h = max(32, h)

        # Scale in-memory QImage and convert to QPixmap
        scaled_img = self.cached_qimage.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pixmap = QPixmap.fromImage(scaled_img)
        
        self.image_label.setPixmap(pixmap)
        self.image_label.setText("") # Clear loading text
        self.image_label.setStyleSheet("") # Clear loading styles
        
        # Update layout sizes to hug the image tightly
        self.image_label.setFixedSize(w, h)
        
        # Card should be wide enough for the image plus padding
        self.setFixedSize(w + 18, h + 45)
        self.update()

    def set_target_size(self, max_size):
        if self.target_max_size == max_size:
            return
        
        self.target_max_size = max_size
        if self.loaded and self.cached_qimage:
            self.update_thumbnail_display()
        else:
            # Update size for placeholder as well
            self.image_label.setFixedSize(max_size, max_size)
            self.setFixedSize(max_size + 18, max_size + 45)

    def sizeHint(self):
        if self.loaded:
            if self.aspect_ratio >= 1.0:
                w = self.target_max_size
                h = int(self.target_max_size / self.aspect_ratio)
            else:
                h = self.target_max_size
                w = int(self.target_max_size * self.aspect_ratio)
            return QSize(w + 18, h + 45)
        else:
            return QSize(self.target_max_size + 18, self.target_max_size + 45)

    # Hover and selection styles
    def enterEvent(self, event):
        self.setProperty("hovered", True)
        self.style().unpolish(self)
        self.style().polish(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setProperty("hovered", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.image_path)
            self.set_selected(True)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit(self.image_path)
        super().mouseDoubleClickEvent(event)

    def set_selected(self, is_selected):
        self.selected = is_selected
        self.setProperty("selected", is_selected)
        self.style().unpolish(self)
        self.style().polish(self)


class FolderGroupWidget(QWidget):
    def __init__(self, folder_path, parent=None):
        super().__init__(parent)
        self.folder_path = folder_path
        self.thumbnails = []
        
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)

        # Header horizontal container
        self.header_layout = QHBoxLayout()
        self.header_layout.setSpacing(10)

        # Folder Icon & Path label
        folder_display_name = os.path.basename(self.folder_path)
        if not folder_display_name: # Handle root drive
            folder_display_name = self.folder_path
        
        self.header_label = QLabel(f"📂 {folder_display_name}", self)
        self.header_label.setObjectName("sectionHeader")
        self.header_layout.addWidget(self.header_label)

        # Full path label (smaller, elegant)
        self.full_path_label = QLabel(self.folder_path, self)
        self.full_path_label.setStyleSheet("color: #52525b; font-size: 11px; font-weight: normal; margin-left: 5px;")
        self.header_layout.addWidget(self.full_path_label)
        self.header_layout.addStretch()

        self.main_layout.addLayout(self.header_layout)

        # Horizontal separator line
        self.separator = QFrame(self)
        self.separator.setObjectName("separatorLine")
        self.separator.setStyleSheet(FOLDER_SEPARATOR_STYLE)
        self.main_layout.addWidget(self.separator)

        # Flow Layout container for thumbnails
        self.flow_container = QWidget(self)
        self.flow_layout = FlowLayout(self.flow_container, margin=5, hspacing=15, vspacing=15)
        self.main_layout.addWidget(self.flow_container)

    def add_thumbnail(self, thumbnail_widget):
        self.thumbnails.append(thumbnail_widget)
        self.flow_layout.addWidget(thumbnail_widget)
