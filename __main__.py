from sys import exit, argv
from PyQt5.QtWidgets import QApplication
from ui import UI
from pack import Pack

pack = Pack(512, 512, False)
pack.insert(256, 256)
pack.insert(128, 128)
pack.insert(64, 64)
pack.insert(32, 32)
pack.insert(16, 16)
pack.insert(8, 8)
pack.insert(4, 4)
pack.insert(2, 2)
pack.insert(100, 100)
pack.insert(200, 50)
pack.insert(400, 25)
pack.insert(50, 200)
pack.insert(25, 400)
pack.insert(100, 100)
pack.insert(200, 50)
pack.insert(400, 25)
pack.insert(50, 200)
pack.insert(25, 400)

app = QApplication(argv)
ui = UI(pack)
ui.show()
exit(app.exec_())
