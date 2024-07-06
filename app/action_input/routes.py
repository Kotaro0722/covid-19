# app/action_input/routes.py

from flask import Blueprint, render_template, request, redirect, url_for

action_input_bp = Blueprint('action_input', __name__)

@action_input_bp.route('/action_input', methods=['GET', 'POST'])
def action_input():
    dbcon,cur = my_open( **dsn )
    
    action_date = request.form["date"]
    action_time = request.form["time"]
    movement_method = request.form["method"]
    place_of_departure = request.form["departure"]
    place_of_transit = request.form["mid"]
    place_of_arrival = request.form["arrival"]
    companion = True if request.form.get("companion") == "yes" else False
    companion_person = request.form["companion_person"]
    mask = True if request.form.get("mask") == "yes" else False
    import datetime
    dt_now = datetime.datetime.now()
    
    sqlstring = f"""
        INSERT INTO action_table 
        (date, time, method, departure, arrival, 
        companion, companion_person, mask, lastupdate)
        VALUES 
        ('{date}', '{time}', '{method}', '{departure}', 
        '{arrival}', {companion}, '{companion_person}', {mask}, '{dt_now}')
    """
    my_query(sqlstring,cur)
    dbcon.commit()
    my_close( dbcon,cur )

    # ここで受け取ったデータの処理を行う（例えばデータベースに保存するなど）

        return redirect(url_for('action_input.action_input'))  # リダイレクト先のURLを適切に設定する

    return render_template('action_input.html')