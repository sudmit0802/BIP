from .ui_utils import *
from .struct import PlansForm
from database import get_plans_from_db, delete_plan, mute_plan, unmute_plan


def update_main(req):

    form = PlansForm()

    data = get_plans_from_db(current_user.id)
    form.data = data

    if form.validate_on_submit():
        if form.data is not None:
            for plan in form.data:
                if 'del' + plan['id'] in req.form.keys():
                    delete_plan(plan['id'])
                    return redirect(url_for('main'))
                if 'mute' + plan['id'] in req.form.keys():
                    mute_plan(plan['id'])
                    return redirect(url_for('main'))
                if 'unmute' + plan['id'] in req.form.keys():
                    unmute_plan(plan['id'])
                    return redirect(url_for('main'))
        return redirect(url_for('new_plan'))

    return render_template('main.html', form=form)
