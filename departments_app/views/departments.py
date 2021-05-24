from flask import render_template, request, redirect, jsonify, url_for
from departments_app import create_app, db
from . import main_bp
from departments_app.service.services import DepartmentService, EmployeeService

from departments_app.models.department import Department
from departments_app.service.schemas import departments_schema


@main_bp.route("/", methods=["GET", "POST"])
def get_departments():
    # fetch all departments
    if request.method == 'GET':
        data = DepartmentService.fetch_all_departments_avg_salary_num_employees(db.session)
        return render_template("departments.html", data=data)
    # add new department:
    if request.method == 'POST':
        department_name = request.form.get("name")
        DepartmentService.add_one({"name": department_name})
        return redirect(url_for('main.get_departments'))


@main_bp.route("/department/<uuid>", methods=["GET", "POST"])
def get_department(uuid: str):
    # fetch all departments
    if request.method == 'GET':
        data, department_name = EmployeeService.fetch_all_department_employees(department_uuid=uuid)
        return render_template("department_employees.html", data=data, department_name=department_name)


@main_bp.route("/employee", methods=["GET", "POST"])
def get_employees():
    # fetch all departments
    if request.method == 'GET':
        data = EmployeeService.fetch_all_employees()
        return render_template("employees.html", data=data)
