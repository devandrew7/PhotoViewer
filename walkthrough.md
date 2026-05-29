# Photo Viewer & Organizer Prototype Walkthrough

A high-performance, beautifully styled Windows desktop application for scanning, organizing, and viewing local images.

## Features Completed

### 1. Slender Layout with High-Contrast Light Theme
- **Fixed Height Top Bar**: Structured the top control panel inside a `36px` fixed-height QWidget container. The top bar is fully compact and never stretches vertically when the main window resizes, maximizing the image grid area.
- **Fluent Light Theme**: Implemented a highly readable, premium light mode theme using elegant slate borders (`#cbd5e1`), clean white backgrounds (`#ffffff`), and solid dark-charcoal typography (`#0f172a` / `#334155`).
- **2의 제곱수 스냅 슬라이더**: 크기 조절 슬라이더가 모든 픽셀 단위 대신 2의 제곱수(`16`, `32`, `64`, `128`, `256`, `512` px) 크기값 단계로만 스냅(Snap) 이동하여 레이아웃을 빠르고 정밀하게 확대/축소합니다.
- **SVG Grip Splitter**: The left/right panels are separated by a custom-styled `QSplitter` handle showing a subtle vertical grip mark. Moving your mouse over the border highlights it with an active indigo-blue glow, providing clear drag-and-resize feedback.

### 2. Multi-Folder Extended Selection
- **Extended Selection Model**: Upgraded the left `QTreeView` to support `ExtendedSelection`. You can now select multiple directories using `Ctrl` or `Shift` click.
- **Recursive Scan & Folder Grouping**: Scanning is fully recursive, aggregating all files in the selected folders and subfolders. Images are cleanly grouped by their folder path, showing dedicated headers and horizontal separator lines.

### 3. Asynchronous Lazy Loading & Warning Dialog
- **Viewport Buffer Observer**: We monitor the scroll position of the grid view and only trigger the image loading runnable when placeholders intersect the viewport (plus a pre-load buffer of 400px above and below).
- **QRunnable Thread Pool**: Thumbnail loading and EXIF auto-rotation run in a background worker pool (`QThreadPool`), ensuring zero UI lag or freezing even under deep directory structures.
- **Large Scan Confirmation**: Added a `QMessageBox` safety pop-up warning the user if a scan detects more than 500 images, allowing them to proceed safely or cancel.

### 4. Standalone Windows Executable
- **Standalone Package**: Fully compiled the application inside its virtual environment (`.venv`) into a single-file, non-console executable under the `dist/` folder using PyInstaller:
  - Executable path: [main.exe](dist/main.exe)

---

## File Structure Created

- [main.py](main.py): App entry point, folder tree, splitter layout, drag & drop, and main event listeners.
- [thumbnail_widget.py](thumbnail_widget.py): Background workers (`QRunnable`), thumbnail card rendering, double-click launch, and grouping widgets.
- [flow_layout.py](flow_layout.py): Custom PySide/PyQt responsive wrapper layout class.
- [styles.py](styles.py): Complete Light Theme styling and vector SVG resources.

---

## How to Run & Verify

1. **Locate the Executable**:
   Open Windows Explorer and navigate to `D:\Antigravity\PhotoViewer\dist\`.
2. **Execute**:
   Double click [main.exe](dist/main.exe) to start the app instantly without any command terminal showing up in the background!
