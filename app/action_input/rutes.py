# app/action_input/routes.py

from flask import Blueprint, render_template, request, redirect, url_for

action_input_bp = Blueprint('action_input', __name__)

@action_input_bp.route('/action_input', methods=['GET', 'POST'])
def action_input():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        transport = request.form.get('transport')
        departure = request.form.get('departure')
        layovers = request.form.getlist('layover[]')
        destination = request.form.get('destination')
        congestion = request.form.get('congestion')
        comments = request.form.get('comments')
        companions = request.form.get('companions')

        companion_names = []
        companion_relations = []
        companion_masks = []

        if companions == 'yes':
            companion_names = request.form.getlist('companion_names[]')
            companion_relations = request.form.getlist('companion_relations[]')
            companion_masks = request.form.getlist('companion_masks[]')

        # ここで受け取ったデータの処理を行う（例えばデータベースに保存するなど）

        return redirect(url_for('action_input.action_input'))  # リダイレクト先のURLを適切に設定する

    return render_template('action_input.html')

