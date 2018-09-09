from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from zlkt import app
from exts import db
from models import User,Question,Answer

manager = Manager(app)

# 绑定Migrate绑定app和db
migrate = Migrate(app,db)

# 添加迁移脚本命令到migrate
manager.add_command('db',MigrateCommand)

if  __name__ == '__main__':
    manager.run()
