#!/usr/bin/env python3
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server
from web import app, db

migrate = Migrate(app, db)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(host="0.0.0.0", port=8899))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
