import sys
sys.path.append('py_scripts/')
import py_scripts.run_app as run


application = run.RunApp()
application.launch()
application.list_for_notif()
application.update()
while True:
    application.create_notifs()
    application.run()
    if application.is_no_action():
        break
    application.reset_action()
