from flask import render_template
from . import login

@related.route('/related')
def related():
    return render_template('related_search.html',
        title = "関係者リストページ"
    )
