from flask import render_template, request, redirect, url_for, flash
from departments_app import db
from . import main_bp
from departments_app.service.services import DepartmentService
from departments_app.models.department import Department


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
        DepartmentService.update_one_department(uuid=uuid, data={"name": name})
        flash("Department Updated Successfully")
        return redirect(url_for('main.get_departments'))


@main_bp.route("/department/add/", methods=["GET", "POST"])
def add_department():
    if request.method == 'POST':
        department_name = request.form.get("name")
        if department_name:
            DepartmentService.add_one({"name": department_name})
            return redirect(url_for('main.get_departments'))
