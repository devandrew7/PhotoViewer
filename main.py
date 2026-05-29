import os
import sys
from PyQt6.QtCore import QDir, QSize, Qt, QPoint, QRect, QThreadPool, QTimer
from PyQt6.QtGui import QIcon, QAction, QDragEnterEvent, QDropEvent, QFileSystemModel
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSplitter, QTreeView, QScrollArea,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider,
    QStatusBar, QFileDialog, QFrame, QSizePolicy
)

# Import custom components
from styles import LIGHT_THEME
from thumbnail_widget import ThumbnailWidget, FolderGroupWidget

class PhotoViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("프로토타입 이미지 뷰어 및 정리 프로그램")
        self.resize(1280, 800)
        
        # Load Premium Stylesheet
        self.setStyleSheet(LIGHT_THEME)

        # State Variables
        self.current_folder = ""
        self.all_thumbnails = []
        self.THUMB_SIZES = [16, 32, 64, 128, 256, 512]
        self.thread_pool = QThreadPool.globalInstance()
        # Limit max threads to avoid overwhelming the system
        self.thread_pool.setMaxThreadCount(max(2, os.cpu_count() - 1))
        
        # Setup UI
        self.init_ui()
        
        # Setup Drag & Drop
        self.setAcceptDrops(True)

    def init_ui(self):
        # Main Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 4, 12, 10)
        main_layout.setSpacing(8)

        # ----------------------------------------------------
        # 1. Top Control Bar (Fixed height container)
        # ----------------------------------------------------
        top_widget = QWidget()
        top_widget.setFixedHeight(36)
        top_widget.setObjectName("topBarWidget")
        
        top_bar = QHBoxLayout(top_widget)
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.setSpacing(8)

        # App Title / Brand
        brand_label = QLabel("✨ PhotoViewer")
        brand_label.setObjectName("titleLabel")
        top_bar.addWidget(brand_label)
        top_bar.addSpacing(10)

        # Path display & manual navigation
        path_label = QLabel("🔍 폴더 경로:")
        path_label.setStyleSheet("font-weight: 500;")
        top_bar.addWidget(path_label)

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("탐색할 폴더 경로를 입력하거나 좌측 트리에서 선택하세요...")
        self.path_edit.returnPressed.connect(self.on_path_entered)
        top_bar.addWidget(self.path_edit)

        self.btn_go = QPushButton("이동")
        self.btn_go.setToolTip("입력한 경로로 이동합니다.")
        self.btn_go.clicked.connect(self.on_path_entered)
        top_bar.addWidget(self.btn_go)

        self.btn_browse = QPushButton("폴더 선택")
        self.btn_browse.setObjectName("actionButton")
        self.btn_browse.clicked.connect(self.on_browse_clicked)
        top_bar.addWidget(self.btn_browse)

        top_bar.addSpacing(15)

        # Thumbnail Scaling Slider
        slider_label = QLabel("크기 조절:")
        slider_label.setStyleSheet("font-weight: 500;")
        top_bar.addWidget(slider_label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.THUMB_SIZES) - 1)
        self.slider.setValue(3)
        self.slider.setFixedWidth(120)
        self.slider.setToolTip("썸네일 이미지 크기를 실시간으로 확대/축소합니다.")
        self.slider.valueChanged.connect(self.on_slider_value_changed)
        top_bar.addWidget(self.slider)

        self.slider_val_label = QLabel("128px")
        self.slider_val_label.setFixedWidth(45)
        self.slider_val_label.setStyleSheet("color: #475569; font-weight: bold;")
        top_bar.addWidget(self.slider_val_label)

        main_layout.addWidget(top_widget)

        # ----------------------------------------------------
        # 2. Main Content Splitter (Left: Tree, Right: Grid)
        # ----------------------------------------------------
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # --- LEFT PANEL (Folder Tree & Action Button) ---
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        # QFileSystemModel to display folder tree
        self.dir_model = QFileSystemModel()
        self.dir_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot)
        self.dir_model.setRootPath("")  # Triggers drive loading

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.dir_model)
        self.tree_view.setRootIndex(self.dir_model.index(""))
        self.tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        
        # Hide detailed columns to only show name
        self.tree_view.hideColumn(1) # Size
        self.tree_view.hideColumn(2) # Type
        self.tree_view.hideColumn(3) # Date Modified
        self.tree_view.setHeaderHidden(True)
        self.tree_view.clicked.connect(self.on_tree_item_clicked)
        left_layout.addWidget(self.tree_view)

        # Primary Action Button below Tree
        self.btn_view_images = QPushButton("이미지 보기 📂")
        self.btn_view_images.setStyleSheet("font-size: 12px; padding: 8px;")
        self.btn_view_images.setToolTip("선택한 폴더 및 모든 하위 폴더의 이미지를 그룹화하여 로드합니다.")
        self.btn_view_images.clicked.connect(self.load_images_from_selected)
        left_layout.addWidget(self.btn_view_images)

        splitter.addWidget(left_container)

        # --- RIGHT PANEL (Image Scroll Grid View) ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Scroll area container widget
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(15, 15, 15, 15)
        self.scroll_layout.setSpacing(20)
        self.scroll_layout.addStretch() # Push everything up initially
        
        self.scroll_area.setWidget(self.scroll_content)
        
        # Bind vertical scrollbar to Lazy Loader trigger
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.load_visible_thumbnails)
        
        splitter.addWidget(self.scroll_area)

        # Set initial proportions for Left/Right panels (25% / 75%)
        splitter.setSizes([320, 960])
        main_layout.addWidget(splitter)

        # ----------------------------------------------------
        # 3. Status Bar
        # ----------------------------------------------------
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_lbl = QLabel("준비 완료")
        self.status_lbl.setObjectName("statusLabel")
        self.status_bar.addWidget(self.status_lbl)
        
        # Timer for lazy loading triggered after resize/slider changes
        self.lazy_load_timer = QTimer()
        self.lazy_load_timer.setSingleShot(True)
        self.lazy_load_timer.timeout.connect(self.load_visible_thumbnails)

    # ----------------------------------------------------
    # Event Handlers & Core Methods
    # ----------------------------------------------------
    def on_tree_item_clicked(self, index):
        # Get absolute folder path and display in top bar
        path = self.dir_model.filePath(index)
        self.path_edit.setText(path)

    def on_path_entered(self):
        target_path = self.path_edit.text().strip()
        if not target_path or not os.path.exists(target_path):
            self.status_lbl.setText("⚠️ 올바르지 않은 폴더 경로입니다.")
            return

        # Navigate tree view
        index = self.dir_model.index(target_path)
        if index.isValid():
            self.tree_view.setCurrentIndex(index)
            self.tree_view.scrollTo(index)
            self.tree_view.expand(index)
            
        self.load_images_from_paths([target_path])

    def on_browse_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(self, "탐색할 폴더 선택", self.path_edit.text() or "")
        if dir_path:
            self.path_edit.setText(dir_path)
            self.on_path_entered()

    def load_images_from_selected(self):
        selected_indexes = self.tree_view.selectedIndexes()
        if not selected_indexes:
            self.status_lbl.setText("⚠️ 좌측 트리에서 폴더를 먼저 선택해 주세요.")
            return
        
        # Extract unique paths from all selected rows (filtering only column 0)
        paths = list(set([self.dir_model.filePath(idx) for idx in selected_indexes if idx.column() == 0]))
        self.load_images_from_paths(paths)

    def load_images_from_paths(self, root_paths):
        if not root_paths:
            self.status_lbl.setText("⚠️ 선택된 폴더가 없습니다.")
            return

        # Filter out invalid directory paths
        valid_paths = [p for p in root_paths if os.path.isdir(p)]
        if not valid_paths:
            self.status_lbl.setText("⚠️ 올바른 폴더가 아닙니다.")
            return

        self.current_folder = valid_paths[0]
        self.status_lbl.setText("🔄 이미지 스캔 중...")
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        
        # Clean current grid & cancel any running threads
        self.clear_grid()

        # Image extensions to scan
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')
        
        # Step 1: Scan and group image files recursively for all target paths
        grouped_images = {}
        total_images = 0
        
        for root_path in valid_paths:
            for dirpath, _, filenames in os.walk(root_path):
                # Exclude files starting with dot (like .meta) and filter extensions
                img_files = []
                for f in filenames:
                    if f.lower().endswith(valid_extensions) and not f.startswith('.'):
                        img_files.append(os.path.join(dirpath, f))
                
                if img_files:
                    # Sort files alphabetically inside the folder
                    img_files.sort(key=str.lower)
                    
                    if dirpath not in grouped_images:
                        grouped_images[dirpath] = img_files
                        total_images += len(img_files)
                    else:
                        # Avoid duplicates
                        existing = set(grouped_images[dirpath])
                        for f in img_files:
                            if f not in existing:
                                grouped_images[dirpath].append(f)
                                total_images += 1
                        grouped_images[dirpath].sort(key=str.lower)

        # Restore cursor before showing dialogue to avoid wait cursor hover
        QApplication.restoreOverrideCursor()

        # Step 1.5: Warn if total images count is over 500
        if total_images > 500:
            from PyQt6.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self,
                "대량 이미지 로딩 경고",
                f"선택한 폴더(들)에서 {total_images}개의 이미지가 발견되었습니다.\n"
                "500개 이상의 많은 이미지를 불러오면 프로그램 로딩이 일시적으로 느려질 수 있습니다.\n"
                "계속 진행하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            if reply == QMessageBox.StandardButton.No:
                self.status_lbl.setText("📂 로딩이 취소되었습니다.")
                no_img_label = QLabel("로딩이 취소되었습니다.")
                no_img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                no_img_label.setStyleSheet("color: #71717a; font-size: 14px; margin-top: 50px;")
                self.scroll_layout.insertWidget(0, no_img_label)
                return

        # Show wait cursor again for layout building
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        if total_images == 0:
            QApplication.restoreOverrideCursor()
            self.status_lbl.setText("📂 이미지가 존재하지 않는 폴더입니다.")
            no_img_label = QLabel("선택된 폴더 내에 지원되는 이미지 파일(.jpg, .png 등)이 없습니다.")
            no_img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_img_label.setStyleSheet("color: #71717a; font-size: 14px; margin-top: 50px;")
            self.scroll_layout.insertWidget(0, no_img_label)
            return

        # Sort folder groups alphabetically
        sorted_groups = sorted(grouped_images.keys(), key=str.lower)

        # Step 2: Build UI structures with Placeholders
        slider_val = self.THUMB_SIZES[self.slider.value()]
        
        for folder_path in sorted_groups:
            files = grouped_images[folder_path]
            
            # Create a header & layout group
            group_widget = FolderGroupWidget(folder_path, self.scroll_content)
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, group_widget)
            
            for file_path in files:
                thumb = ThumbnailWidget(file_path, target_max_size=slider_val, parent=group_widget.flow_container)
                thumb.clicked.connect(self.on_thumbnail_clicked)
                thumb.double_clicked.connect(self.on_thumbnail_double_clicked)
                
                group_widget.add_thumbnail(thumb)
                self.all_thumbnails.append(thumb)

        QApplication.restoreOverrideCursor()
        self.status_lbl.setText(f"📂 스캔 완료 | 총 {total_images}개의 이미지")
        
        # Trigger immediate lazy load
        self.load_visible_thumbnails()

    def clear_grid(self):
        # Safely remove all folder group widgets from the scroll layout
        self.all_thumbnails.clear()
        
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
                
        # Force garbage collection/layout update
        self.scroll_content.adjustSize()

    # ----------------------------------------------------
    # Lazy Loading Core Logic
    # ----------------------------------------------------
    def load_visible_thumbnails(self):
        if not self.all_thumbnails:
            return

        viewport = self.scroll_area.viewport()
        viewport_rect = viewport.rect()
        
        # Buffer zone: Load 400px above and below current view for fluid scrolling
        visible_buffer_rect = QRect(
            0,
            -400,
            viewport.width(),
            viewport.height() + 800
        )

        for thumb in self.all_thumbnails:
            if thumb.loaded or thumb.loading_started:
                continue

            # Check if thumbnail overlaps the visible buffer viewport
            pos_in_viewport = thumb.mapTo(viewport, QPoint(0, 0))
            thumb_rect = QRect(pos_in_viewport, thumb.size())

            if visible_buffer_rect.intersects(thumb_rect):
                thumb.load_thumbnail(self.thread_pool)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Delay lazy loading check slightly to let widgets recalculate coordinates
        self.lazy_load_timer.start(50)

    # ----------------------------------------------------
    # Slider & Interaction Actions
    # ----------------------------------------------------
    def on_slider_value_changed(self, index):
        value = self.THUMB_SIZES[index]
        self.slider_val_label.setText(f"{value}px")
        
        # Rescale all existing thumbnails dynamically
        for thumb in self.all_thumbnails:
            thumb.set_target_size(value)
            
        # Re-adjust scroll content size
        self.scroll_content.adjustSize()
        
        # Trigger lazy load for new items scrolled/reflowed into view
        self.lazy_load_timer.start(100)

    def on_thumbnail_clicked(self, image_path):
        # Deselect all other thumbnails
        for thumb in self.all_thumbnails:
            if thumb.image_path != image_path:
                thumb.set_selected(False)
        self.status_lbl.setText(f"선택됨: {image_path}")

    def on_thumbnail_double_clicked(self, image_path):
        # Open in default system viewer
        try:
            if sys.platform.startswith('win'):
                os.startfile(image_path)
            elif sys.platform.startswith('darwin'):
                import subprocess
                subprocess.call(('open', image_path))
            else:
                import subprocess
                subprocess.call(('xdg-open', image_path))
        except Exception as e:
            self.status_lbl.setText(f"⚠️ 이미지를 열 수 없습니다: {str(e)}")

    # ----------------------------------------------------
    # Drag and Drop Events
    # ----------------------------------------------------
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            # Check if at least one URL is a directory
            urls = event.mimeData().urls()
            for url in urls:
                if os.path.isdir(url.toLocalFile()):
                    event.acceptProposedAction()
                    return
        super().dragEnterEvent(event)

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            first_dir = urls[0].toLocalFile()
            if os.path.isdir(first_dir):
                self.path_edit.setText(first_dir)
                self.on_path_entered()
                event.acceptProposedAction()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoViewerApp()
    window.show()
    sys.exit(app.exec())
