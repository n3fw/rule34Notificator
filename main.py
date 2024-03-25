import run_app as run

application = run.RunApp()
application.list_for_notif()
application.update()
while True:
    application.create_notifs()
    application.run()
    if application.is_no_action():
        break
    application.reset_action()