from flask_app import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_app.models import *

admin = Admin(
    app,
    name='Flask-admin laboratory',
    template_mode='bootstrap4',
)

admin.add_view(ModelView(Account, db.session))
admin.add_view(ModelView(Address, db.session))
admin.add_view(ModelView(Sex, db.session))
admin.add_view(ModelView(MovieCategory, db.session))
admin.add_view(ModelView(Movie, db.session))
admin.add_view(ModelView(Cast, db.session))
admin.add_view(ModelView(AgeLimit, db.session))
admin.add_view(ModelView(Screen, db.session))
admin.add_view(ModelView(Showing, db.session))
admin.add_view(ModelView(Price, db.session))
admin.add_view(ModelView(Discount, db.session))
admin.add_view(ModelView(Reservation, db.session))
admin.add_view(ModelView(ShowTime, db.session))

if __name__ == '__main__':
    app.run(debug=True)
    # host='localhost',port=8000,