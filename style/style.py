from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

SHADOW = QGraphicsDropShadowEffect()
SHADOW.setBlurRadius(30)
SHADOW.setOffset(0, 0)
SHADOW.setColor(QColor(0, 102, 204, 127))
