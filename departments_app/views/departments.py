from flask import render_template, request, redirect, jsonify, url_for, flash
from departments_app import create_app, db
from . import main_bp
from departments_app.service.services import DepartmentService, EmployeeService
from departments_app.models.department import Department
from departments_app.models.employee import Employee


@main_bp.route("/", methods=["GET", "POST"])
def get_departments():
    # fetch all departments
    if request.method == 'GET':
        data = DepartmentService.fetch_all_departments_aggregated(db.session)
        return render_template("index.html", data=data)


@main_bp.route("/department/delete/<uuid>/", methods=["GET", "POST"])
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


@main_bp.route("/employee", methods=["GET", "POST"])
def get_employees():
    # fetch all employees
    if request.method == 'GET':
        data = EmployeeService.fetch_all_employees()
        departments = DepartmentService.fetch_all()
        return render_template("employees.html", data=data, departments=departments)


@main_bp.route("/employee/add/", methods=["GET", "POST"])
def add_employee():
    # fetch all employees
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        date_of_birth = request.form.get("date_of_birth")
        phone_number = request.form.get("phone_number")
        salary = request.form.get("salary")
        email = request.form.get("email")
        department_uuid = request.form.get("department_name").split()[1]
        department_name = request.form.get("department_name").split()[0]
        data = {"first_name": first_name,
                "last_name": last_name,
                "date_of_birth": date_of_birth,
                "phone_number": phone_number,
                "salary": salary,
                "email": email,
                "department": {"uuid": department_uuid, "name": department_name}}
        result = EmployeeService.add_one_employee(data)
        if result:
            flash("Employee added!!!")
            return redirect(url_for('main.get_employees'))


@main_bp.route("/employee/delete/<uuid>/")
def delete_employee(uuid):
    db_record = Employee.get_by_uuid(uuid)
    Employee.delete(db_record)
    flash("Employee deleted successfully")
    return redirect(url_for('main.get_employees'))


@main_bp.route("/employee/update/", methods=["POST"])
def update_employee():
    if request.method == "POST":
        uuid = request.form.get("uuid")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        date_of_birth = request.form.get("date_of_birth")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email")
        salary = request.form.get("salary")
        department_uuid = request.form.get("department_uuid")
        data = {"first_name": first_name,
                "last_name": last_name,
                "date_of_birth": date_of_birth,
                "phone_number": phone_number,
                "salary": salary,
                "email": email,
                "department": {"uuid": department_uuid}}
        EmployeeService.update(uuid=uuid, data=data)

        flash("Employee updated successfully")
        return redirect(url_for('main.get_employees'))


@main_bp.route("/department/<uuid>/employees", methods=["GET"])
def get_department_employees(uuid):
    if request.method == "GET":
        data, department_name = EmployeeService.fetch_all_department_employees(uuid)

        return render_template("department_employees.html", data=data, department_name=department_name)
