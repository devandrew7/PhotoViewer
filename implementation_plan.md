# PyQt6 Image Viewer & Organizer Prototype Plan

An elegant, high-performance desktop application for Windows 10/11 built with Python and PyQt6. The application features a split-pane layout: a folder tree explorer on the left and a responsive, lazy-loading image grid view on the right, controlled by an adaptive slider for real-time thumbnail resizing.

## Features & Implementation Strategy

### Subfolder Grouping & Lazy Loading Strategy
- When the "View Images" (이미지 보기) button is clicked, the app recursively scans the selected folder and all its subfolders.
- Images are grouped by their folder path. Each folder group gets a dedicated header and a wrap-around Flow Layout.
- **Lazy Loading**: If a folder contains many images, we instantiate empty placeholder widgets first to keep the UI immediate. We then monitor the scroll position of the `QScrollArea` and load thumbnails asynchronously only for the items currently visible in the viewport.
- **Threading**: A `QThreadPool` executes `QRunnable` tasks in the background to read and scale image files (supporting `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.webp`), preventing the main UI thread from freezing.

### Aesthetics & Performance
- The UI uses a premium Light Theme stylesheet, featuring smooth hover states, clean card outlines for thumbnail items, and subtle micro-animations (e.g., active highlight outlines).
- We package the application into a standalone Windows `.exe` using `PyInstaller`.

## Proposed Changes

We have created a modular, clean Python project structure inside the workspace:

### 1. [flow_layout.py](flow_layout.py)
A custom PyQt6 `QLayout` subclass that arranges widgets horizontally and wraps them to the next line when width is exceeded. This is crucial for the responsive thumbnail grid.

### 2. [styles.py](styles.py)
Holds the premium CSS stylesheets, color tokens (Light Theme white backgrounds, active blue accents, smooth transitions), and icon/font helper setups.

### 3. [thumbnail_widget.py](thumbnail_widget.py)
- `ThumbnailRunnable`: A `QRunnable` subclass to load and scale images in a worker thread.
- `ThumbnailWidget`: An individual image card widget displaying the image thumbnail and filename. Features hover styling and lazy-loading state management.
- `FolderGroupWidget`: A container widget for a single folder group. It contains a section header (styled label + horizontal line) and a `FlowLayout` to arrange `ThumbnailWidget`s.

### 4. [main.py](main.py)
The primary entry point. Integrates:
- `QSplitter` dividing the left and right view.
- Left: `QTreeView` with `QFileSystemModel` displaying drives and folders, supporting multiple folders selection, and the "View Images" button.
- Top bar: Directory path line-edit, "Go" button, and the Thumbnail Scaling Slider with a 2의 제곱수 스냅 슬라이더 (16px, 32px, 64px, 128px, 256px, 512px).
- Right: A `QScrollArea` holding the vertical arrangement of `FolderGroupWidget`s.
- Scroll and Resize listener logic to trigger Lazy Loading of thumbnails inside the visible viewport.

---

## Verification Plan

### Automated/Local Execution Tests
1. **Dependencies Installation**: Verify PyQt6 is installed (`pip install PyQt6`).
2. **Execution Test**: Run `python main.py` and interactively test navigation, slider adjustments, multiple folders, and >500 warning.
3. **Executable Compilation**: Compile the prototype using `PyInstaller` (`pyinstaller --noconsole --onefile main.py`) and verify the resulting `.exe` works standalone.
