LIGHT_THEME = """
/* General Styles */
QMainWindow {
    background-color: #f8fafc; /* light slate background */
    color: #0f172a; /* slate 900 text */
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, sans-serif;
}

QWidget {
    color: #0f172a;
    font-size: 13px;
}

/* Splitter */
QSplitter::handle {
    background-color: #e2e8f0;
}
QSplitter::handle:horizontal {
    width: 6px;
    image: url(data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="9" y1="5" x2="9" y2="19"></line><line x1="15" y1="5" x2="15" y2="19"></line></svg>);
}
QSplitter::handle:horizontal:hover {
    background-color: #2563eb;
}
QSplitter::handle:vertical {
    height: 6px;
    image: url(data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="9" x2="19" y2="9"></line><line x1="5" y1="15" x2="19" y2="15"></line></svg>);
}
QSplitter::handle:vertical:hover {
    background-color: #2563eb;
}

/* Folder Tree Explorer (Left Panel) */
QTreeView {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 4px;
    color: #0f172a;
}

QTreeView::item {
    padding: 4px 4px;
    border-radius: 4px;
}

QTreeView::item:hover {
    background-color: #f1f5f9;
}

QTreeView::item:selected {
    background-color: #dbeafe;
    color: #1e40af;
    font-weight: 500;
}

QTreeView::branch {
    background: transparent;
}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {
    image: url(data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="%2364748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>);
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings  {
    image: url(data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="%2364748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>);
}

/* ScrollArea (Right Panel Container) */
QScrollArea {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
}

QScrollArea > QWidget > QWidget {
    background-color: #ffffff;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #f1f5f9;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #cbd5e1;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #f1f5f9;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background: #cbd5e1;
    min-width: 20px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background: #94a3b8;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
    width: 0px;
}

/* Buttons */
QPushButton {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 5px 12px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e3a8a;
}

QPushButton:disabled {
    background-color: #e2e8f0;
    color: #94a3b8;
}

/* Secondary Button style for Folder view buttons */
QPushButton#actionButton {
    background-color: #e2e8f0;
    color: #334155;
    border: 1px solid #cbd5e1;
}
QPushButton#actionButton:hover {
    background-color: #cbd5e1;
}
QPushButton#actionButton:pressed {
    background-color: #94a3b8;
}

/* Text Inputs / Path bar */
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 4px 10px;
    color: #0f172a;
    selection-background-color: #93c5fd;
    selection-color: #1e3a8a;
}

QLineEdit:focus {
    border: 1px solid #2563eb;
}

/* Sliders */
QSlider::groove:horizontal {
    border: 1px solid #cbd5e1;
    height: 6px;
    background: #f1f5f9;
    margin: 2px 0;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #2563eb;
    border: none;
    width: 14px;
    height: 14px;
    margin: -4px 0;
    border-radius: 7px;
}

QSlider::handle:horizontal:hover {
    background: #1d4ed8;
}

QSlider::handle:horizontal:pressed {
    background: #1e3a8a;
}

/* Headers / Labels */
QLabel#sectionHeader {
    font-size: 15px;
    font-weight: bold;
    color: #1e40af;
    padding: 8px 0px 4px 6px;
}

QLabel#titleLabel {
    font-size: 18px;
    font-weight: 800;
    color: #0f172a;
}

QLabel#statusLabel {
    color: #475569;
    font-size: 12px;
}
"""

IMAGE_CARD_STYLE = """
QWidget#thumbnailCard {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}
QWidget#thumbnailCard[hovered="true"] {
    background-color: #f8fafc;
    border: 1px solid #2563eb;
}
QWidget#thumbnailCard[selected="true"] {
    background-color: #eff6ff;
    border: 2px solid #3b82f6;
}

QLabel#imageLabel {
    background-color: #f1f5f9;
    border-radius: 6px;
    border: 1px solid #e2e8f0;
}

QLabel#filenameLabel {
    color: #334155;
    font-size: 11px;
    font-weight: 500;
}
QWidget#thumbnailCard[hovered="true"] QLabel#filenameLabel {
    color: #0f172a;
}
"""

FOLDER_SEPARATOR_STYLE = """
QFrame#separatorLine {
    background-color: #cbd5e1;
    max-height: 1px;
    min-height: 1px;
}
"""
