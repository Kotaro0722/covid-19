from flask import Blueprint, render_template, request, redirect, url_for, flash
from your_app.models import Condition, Action  # Assuming you have models for Condition and Action
from your_app import db

condition_bp = Blueprint('condition', __name__)

@condition_bp.route('/condition_input', methods=['GET', 'POST'])
def condition_input():
    if request.method == 'POST':
        date = request.form['date']
        temperature = request.form.get('temperature')
        symptoms = {
            'joint_pain': request.form.get('joint_pain') == 'on',
            'fatigue': request.form.get('fatigue') == 'on',
            'headache': request.form.get('headache') == 'on',
            'sore_throat': request.form.get('sore_throat') == 'on',
            'shortness_of_breath': request.form.get('shortness_of_breath') == 'on',
            'cough_sneeze': request.form.get('cough_sneeze') == 'on',
            'nausea_vomiting': request.form.get('nausea_vomiting') == 'on',
            'stomach_ache_diarrhea': request.form.get('stomach_ache_diarrhea') == 'on',
            'taste_disorder': request.form.get('taste_disorder') == 'on',
            'smell_disorder': request.form.get('smell_disorder') == 'on'
        }

        # 少なくとも1つの症状が入力されているか確認
        if not any(symptoms.values()):
            flash('少なくとも1つの症状をチェックしてください！', 'danger')
            return redirect(url_for('condition.condition_input'))

        new_condition = Condition(
            date=date,
            temperature=temperature,
            symptoms=symptoms
        )
        db.session.add(new_condition)
        db.session.commit()
        return redirect(url_for('condition.condition_output'))

    return render_template('condition_input.html')

@condition_bp.route('/condition_output', methods=['GET'])
def condition_output():
    conditions = Condition.query.all()
    actions = Action.query.all()  # Assuming you have an Action model and data
    return render_template('user_output.html', conditions=conditions, actions=actions)

