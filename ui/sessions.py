from .struct import SessionsForm
from .ui_utils import *
from database import get_sessions_from_db, disable_user, close_session


def update_sessions(req):
    form = SessionsForm()

    if current_user is None:
        return redirect(url_for('signin'))

    data = get_sessions_from_db(current_user.id)

    if data is None:
        return redirect(url_for('signin'))

    form.data = data
    if form.validate_on_submit():
        for login in form.data:
            if login['id'] in req.form.keys():
                close_session(login['ip'], current_user.id)
                return redirect(url_for('sessions'))

        disable_user(current_user.id)
        return redirect(url_for('logout'))

    return render_template('sessions.html', form=form)
