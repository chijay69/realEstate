import os
from datetime import timedelta

from app import create_app, db, socket
from app.models import User, Property, CreditCard
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Property=Property, CreditCard=CreditCard)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    socket.run(app, host="localhost")
