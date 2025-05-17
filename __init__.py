

try:
    from aqt import mw
    from .addon.addonWindow import Windows
    try:
        from aqt import QAction
    except:
        from PyQt5.QtWidgets import QAction


    def showWindow():
        w = Windows()
        w.exec()


    action = QAction("Dict2Anki...(By Dream)", mw)
    action.triggered.connect(showWindow)
    mw.form.menuTools.addAction(action)

except ImportError:
    import os
    try:
        from PyQt6.QtWidgets import QApplication
    except:
        from PyQt5.QtWidgets import QApplication
    from addon.addonWindow import Windows
    import sys
    if os.environ.get('DEVDICT2ANKI'):
        app = QApplication(sys.argv)
        window = Windows()
        window.show()
        sys.exit(app.exec())
