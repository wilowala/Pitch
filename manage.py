from app import create_app
from flask_script import Manager,Server
from app.models import User,Role,Pitch
from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager,Server

app = create_app('development')

manager = Manager(app)
manager.add_command('server',Server)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User, Role = Role)

# manager.add_command('server',Server)
if __name__ == '__main__':
    manager.run(debug=True)