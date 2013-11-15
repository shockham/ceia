from flask import Blueprint, render_template, request
from model import Sanc
from flask.ext.mongoengine.wtf import model_form

sanc = Blueprint('sanc', __name__, template_folder='../template')


@sanc.route('/sanc/', methods=['GET', 'POST'])
def sanc_route():
	
	#get all the sancs
	sancs = Sanc.objects()

	#create the object
	item = Sanc()

    #model the form
	form_cls = model_form(Sanc,  exclude=('created_at'))

	if request.method == 'POST':
		form = form_cls(request.form, inital=item._data)
		if form.validate():
			form.populate_obj(item)
			item.save()
	else:
		form = form_cls(obj=item)
	return render_template('sanc.html', sancs=sancs, form=form)