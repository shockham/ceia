import os
from flask import Flask, render_template, make_response, send_from_directory
from flask.ext.mongoengine import MongoEngine
from datetime import datetime, timedelta

app = Flask(__name__)
app.debug = True
app.config.from_pyfile('config.cfg')

db = MongoEngine(app)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

@app.errorhandler(500)
def page_broken(error):
    return render_template('error.html'), 500

@app.errorhandler(502)
def page_broken(error):
    return render_template('error.html'), 502

@app.errorhandler(413)
def upload_large(error):
    return render_template('error.html'), 413

@app.route('/sitemap.xml', methods=['GET'])
@app.route('/sitemap1.xml', methods=['GET'])
def sitemap():
      """Generate sitemap.xml. Makes a list of urls and date modified."""
      pages=[]
      ten_days_ago=datetime.now() - timedelta(days=10)
      # static pages
      for rule in app.url_map.iter_rules():
          if "GET" in rule.methods and len(rule.arguments)==0:
              pages.append( [rule.rule,ten_days_ago] )


      sitemap_xml = render_template('sitemap.xml', pages=pages)
      response= make_response(sitemap_xml)
      response.headers["Content-Type"] = "application/xml"    
    
      return response

@app.route('/robots.txt')
def robots():
    return render_template('robots.txt')

@app.route('/favicon.ico/')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'images/favicon.ico', mimetype='image/vnd.microsoft.icon')

def register_blueprints(app):
    from App.modules.routes import routes
    from App.modules.sanc import sanc
    app.register_blueprint(routes)
    app.register_blueprint(sanc)

register_blueprints(app)

if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler('ceia.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run()
