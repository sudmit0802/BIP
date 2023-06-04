from .ui_utils import *
from .struct import NewPlanForm, get_subject_form_class
from api_interface import get_faculties_routine, get_groups_on_faculties_by_id_routine
from database import push_plan, delete_deadline, delete_plan, get_subjects_for_plan, get_stored_deadlines_for_subject, push_deadline


def create_plan(req):

    req_fac = req.args.get('faculty')
    req_gr = req.args.get('group')

    form = NewPlanForm()

    faculties = asyncio.run(get_faculties_routine())
    form.faculties.choices = [(faculty.id, faculty.abbr)
                              for faculty in faculties if faculty.abbr not in ['ИДО', 'ИФНиТ', 'УПКР', 'ИПММ', 'ИППТ']]

    groups = asyncio.run(
        get_groups_on_faculties_by_id_routine(req_fac if req_fac else faculties[0].id))
    form.groups.choices = [(group.id, group.name) for group in groups]

    if not req_fac or not req_gr:
        return redirect(url_for('new_plan', faculty=form.faculties.choices[0][0], group=form.groups.choices[0][0]))

    if form.validate_on_submit():
        if form.confirm.data:
            if form.plan_name.data:
                plan_id = push_plan(form.plan_name.data,
                                    req_gr, current_user.id)
                if plan_id == 0:
                    return render_template('new_plan.html', form=form, message="План с таким названием уже существует")
                return redirect(url_for('subjects', plan_id=plan_id))
            else:
                return render_template('new_plan.html', form=form, message="Введите название плана")

        new_groups = asyncio.run(
            get_groups_on_faculties_by_id_routine(form.faculties.data))
        id_list = [str(group.id) for group in new_groups]
        new_group = form.groups.data if form.groups.data in id_list else new_groups[0].id
        return redirect(url_for('new_plan', faculty=form.faculties.data, group=new_group))

    if req_fac and req_gr:
        form.faculties.default = req_fac
        form.groups.default = req_gr
        form.process(req.form)

    return render_template('new_plan.html', form=form)


def set_deadlines(req):

    forms = dict()
    stored_deadlines = dict()

    if req.referrer is not None and req.args.get('plan_id') is not None:
        if str(req.referrer).startswith('http://localhost:5000/new_plan') or str(req.referrer).startswith('http://localhost:5000/main'):

            subjects = get_subjects_for_plan(req.args.get('plan_id'))
            if subjects is None:
                delete_plan(req.args.get('plan_id'))
                return "Нет смысла делать план, если у группы вообще нет занятий"

            for id, subject in subjects.items():
                form_class = get_subject_form_class(id)
                form = form_class()
                stored_deadlines[subject] = get_stored_deadlines_for_subject(
                    id)
                forms[subject] = form

            for subject, form in forms.items():
                if form.validate_on_submit():
                    if form.deadline.name.data and form.deadline.time.data and form.add.id in req.form.keys():
                        push_deadline(
                            form.add.id[3:], form.deadline.name.data, form.deadline.time.data)
                        return redirect(url_for('subjects', plan_id=req.args.get('plan_id')))

                    for deadline in stored_deadlines[subject]:
                        if 'del' + str(deadline['id']) in req.form.keys():
                            delete_deadline(deadline['id'])
                            return redirect(url_for('subjects', plan_id=req.args.get('plan_id')))

            return render_template('deadlines.html', forms=forms, stored_deadlines=stored_deadlines)

    return redirect(url_for('new_plan'))
