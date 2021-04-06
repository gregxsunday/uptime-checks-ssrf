from flask import Flask, render_template
# from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.config')

# db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
  return 'Not Found', 404

from app.core.views import mod as core
app.register_blueprint(core)

import gunicorn
gunicorn.SERVER_SOFTWARE = 'Microsoft-IIS/6.0'

# Later on you'll import the other blueprints the same way:
#from app.comments.views import mod as commentsModule
#from app.posts.views import mod as postsModule
#app.register_blueprint(commentsModule)
#app.register_blueprint(postsModule)

