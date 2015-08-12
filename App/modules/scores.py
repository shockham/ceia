from flask import Blueprint, jsonify, request
from .model import Score
from .salt import requires_salt

scores = Blueprint('scores', __name__, template_folder='../template')


@scores.route('/update_score/<tag>', methods=['POST'])
@requires_salt
def update_score(tag):
    score = Score.objects(tag=tag, user=request.form.get('user')).first()
    score_val = request.form.get('score')
    
    if not score:
        score = Score(
                user=request.form.get('user'),
                score=score_val,
                tag=tag
            )
    elif int(score_val) > score.score: 
        score.score = score_val
    
    success = score.save()

    return jsonify({ 'success': success })


@scores.route('/get_scores/<tag>')
def get_scores(tag):
    scores = Score.objects(tag=tag)[:10] 
    str_score = ''.join("%s. %s - %s\n" % (i, s.user, s.score) for i,s in enumerate(scores, start=1))
    return "global:\n%s" % str_score
