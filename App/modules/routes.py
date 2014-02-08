from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.mongoengine.wtf import model_form
from model import Concept, Stat
from auth import requires_auth
from stats import track_stats
import os
from werkzeug import secure_filename

routes = Blueprint('routes', __name__, template_folder='../template')


@routes.route('/')
@track_stats
def index():
    concepts = Concept.objects(parent="")
    return render_template('main.html', concepts=concepts)

@routes.route('/<concept_slug>')
@routes.route('/<concept_slug>/')
@track_stats
def concept(concept_slug):
    concept = Concept.objects.get(slug=concept_slug)
    sub_concepts = Concept.objects(parent__icontains=concept_slug)
    return render_template('concept.html', concept=concept, sub_concepts=sub_concepts)

@routes.route('/<concept_slug>/edit', methods=['GET', 'POST'])
@requires_auth
def edit_concept(concept_slug):
    concept = Concept.objects(slug=concept_slug).first()
    if not concept:
        concept = Concept()

    form_cls = model_form(Concept,  exclude=('created_at', 'slug'))

    if request.method == 'POST':
        form = form_cls(request.form, inital=concept._data)
        if form.validate():
            form.populate_obj(concept)
            concept.slug = concept_slug
            concept.save()
            return redirect(url_for('routes.concept', concept_slug=concept.slug))
    else:
        form = form_cls(obj=concept)

    return render_template('edit.html', concept=concept, form=form)    

@routes.route('/upload_file', methods=['GET', 'POST'])
@requires_auth
def upload_file():
    static_folder = os.getcwd() + '/App/static/uploaded_images'
    if request.method == 'POST':
        file = request.files['file']
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1] in ['pdf', 'png', 'jpg', 'jpeg', 'gif']:
            filename = secure_filename(file.filename)
            file.save(os.path.join(static_folder, filename))
    return render_template('file_uploader.html', files=os.listdir(static_folder))

@routes.route('/error')
@track_stats
def error():
    return render_template('error.html')


@routes.route('/stats')
@track_stats
def stats_view():
    stats = Stat.objects()
    return render_template('stats.html', stats=stats)
