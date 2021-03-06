import os
from flask import Blueprint
from flask import Flask, g
from views import blueprint, CitationHelper
from flask.ext.restful import Api
from flask.ext.discoverer import Discoverer
from client import Client

def _create_blueprint_():
  '''
  Returns a initialized Flask.Blueprint instance;
  This should be in a closure instead of the top level of a module because
  a blueprint can only be registered once. Having it at the top level
  creates a problem with unittests in that the app is created/destroyed at every test,
  but its blueprint is still the same object which was already registered
  '''
  return Blueprint(
    'citation_helper',
    __name__,
    static_folder=None,
  )

def create_app(blueprint_only=False):
  app = Flask(__name__, static_folder=None)

  app.url_map.strict_slashes = False
  app.config.from_pyfile('config.py')
  try:
    app.config.from_pyfile('local_config.py')
  except IOError:
    pass

  app.config['CITATION_HELPER_CLIENT'] = Client({'TOKEN':app.config.get('CITATION_HELPER_API_TOKEN',None)})

  blueprint = _create_blueprint_()
  api = Api(blueprint)
  api.add_resource(CitationHelper, '/')

  if blueprint_only:
    return blueprint

  app.register_blueprint(blueprint)

  discoverer = Discoverer(app)

  return app

if __name__ == "__main__":
  app = create_app()
  app.run(debug=True,use_reloader=False)
