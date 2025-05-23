import datetime
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


habits = ["wash clothes"]
completions = defaultdict(list)


@app.context_processor
def add_clac_date_range():
    def date_range(start: datetime.date):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    return {"date_range": date_range}


@app.route('/')
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    else:
        selected_date = datetime.date.today()
    return render_template('index.html', 
        title="Habit Tracker - Home", 
        habits=habits,
        selected_date=selected_date,
        completions=completions[selected_date]
    )


@app.route('/add',methods=["GET","POST"])
def add_habit():
    if request.method == "POST":
        content = request.form.get("content")
        if content is not None:
            habits.append(content)
    return render_template("add_habit.html", title="Habit Tracker - Add", selected_date = datetime.date.today(),)


@app.post("/complete")
def complete():
    date_string = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.date.fromisoformat(date_string)
    completions[date].append(habit)
    return redirect(url_for("index", date=date_string))

if __name__ == '__main__':
    app.run(debug=True)