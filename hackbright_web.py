"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def homepage():
    """Link to all students and projects."""
    projects = hackbright.get_all_projects()
    students = hackbright.get_all_students()

    html = render_template("index.html", projects=projects, students=students)

    return html



@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github, grades=grades)
    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/new-student")
def get_new_student_info():
    """Show form for searching for a student."""

    return render_template("new-student.html")


@app.route("/enroll", methods=["POST"])
def add_student():
    """Add a new student to the database."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    html = render_template("student_info.html",
                           first=first_name,
                           last=last_name,
                           github=github)
    
    return html


@app.route("/project")
def display_project():
    """Display project info."""

    project = request.args.get('title')
    grades = hackbright.get_grades_by_title(project)
    
    name_grade = []
    for git, grade in grades: 
        first, last, github = hackbright.get_student_by_github(git)
        name_grade.append((first, github, grade))

    title, description, max_grade = hackbright.get_project_by_title(project)

    html = render_template("project_info.html", title=title,
                           description=description, max_grade=max_grade, 
                           grades=name_grade)
    
    return html


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
