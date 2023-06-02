from .ui_utils import *
from .struct import NewPlanForm
from api_interface import get_faculties_routine, get_groups_on_faculties_by_id_routine


def create_plan(req):

    req_fac = req.args.get('faculty')
    req_gr = req.args.get('group')

    form = NewPlanForm()

    faculties = asyncio.run(get_faculties_routine())
    form.faculties.choices = [(faculty.id, faculty.abbr)
                              for faculty in faculties if faculty.abbr not in ['ИДО', 'ИФНиТ', 'УПКР', 'ИПММ']]

    groups = asyncio.run(
        get_groups_on_faculties_by_id_routine(req_fac if req_fac else faculties[0].id))
    form.groups.choices = [(group.id, group.name) for group in groups]

    if not req_fac or not req_gr:
        return redirect(url_for('new_plan', faculty=form.faculties.choices[0][0], group=form.groups.choices[0][0]))

    if form.validate_on_submit():
        return redirect(url_for('new_plan', faculty=form.faculties.data, group=form.groups.data))

    if req_fac and req_gr:
        form.faculties.default = req_fac
        form.groups.default = req_gr
        form.process(req.form)

    return render_template('new_plan.html', form=form)
