"""Golden fixture plugin entry point."""

from qgis.PyQt.QtWidgets import QAction


class GoldenPlugin:
    """Minimal QGIS plugin used as a golden-report fixture."""

    def __init__(self, iface):
        self.iface = iface
        self.action = QAction("Run Golden", None)

    def init_gui(self):
        self.action.setText("OK")

    def run(self):
        self.iface.messageBar().pushMessage("Done")


def classFactory(iface):
    """QGIS plugin factory entry point."""
    return GoldenPlugin(iface)
