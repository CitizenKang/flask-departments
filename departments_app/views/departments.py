from flask import render_template, request, redirect, jsonify, url_for, flash
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
        return render_template("index.html", data=data)


@main_bp.route("/department/delete/<uuid>/")
def delete_department(uuid):
    db_record = Department.get_by_uuid(uuid)
    Department.delete(db_record)
    flash("Department Deleted Successfully")
    return redirect(url_for('main.get_departments'))


@main_bp.route("/department/update/", methods=["POST"])
def update_department():
    if request.method == "POST":
        uuid = request.form.get("uuid")
        name = request.form.get("name")
        DepartmentService.update_one_department(uuid=uuid, json_data={"name": name})
        flash("Department Updated Successfully")
        return redirect(url_for('main.get_departments'))


@main_bp.route("/department/add/", methods=["GET", "POST"])
def add_department():
    if request.method == 'POST':
        department_name = request.form.get("name")
        if department_name:
            DepartmentService.add_one({"name": department_name})
            return redirect(url_for('main.get_departments'))


# #
# @main_bp.route("/department/<uuid>", methods=["GET", "POST"])
# def get_department(uuid: str):
#     # fetch all departments
#     if request.method == 'GET':
#         data, department_name = EmployeeService.fetch_all_department_employees(department_uuid=uuid)
#         return render_template("department_employees.html", data=data, department_name=department_name)
#
#     first_name = request.form.get("first_name")
#     last_name = request.form.get("last_name")
#     date_of_birth = request.form.get("date_of_birth")
#     phone_number = request.form.get("phone_number")
#     email = request.form.get("email")
#     salary = request.form.get("salary")
#     input = {"first_name": first_name,
#              "last_name": last_name,
#              "date_of_birth": date_of_birth,
#              "phone_number": phone_number,
#              "email": email,
#              "salary": salary,
#              "department": {"uuid": uuid}}
#     EmployeeService.add_one_employee(data=input)
#     return redirect(url_for('main.get_department'))
#
#
@main_bp.route("/employee", methods=["GET", "POST"])
def get_employees():
    # fetch all departments
    if request.method == 'GET':
        data = EmployeeService.fetch_all_employees()
        return render_template("employees.html", data=data)
