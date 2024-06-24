from flask import Flask, render_template,Blueprint

views_bp = Blueprint('views', __name__, url_prefix='/views')

@views_bp.route('/comingList')
def cominglist():
    return render_template('comingList.html')

@views_bp.route('/infoedit')
def intoedit():
    return render_template('infoEdit.html')

@views_bp.route('/moviedetail')
def moviedetail():
    return render_template('moviedetail.html')

@views_bp.route('/movielist')
def movielist():
    return render_template('movieList.html')

@views_bp.route('/screen')
def screen():
    return render_template('screen.html')

@views_bp.route('/sitemap')
def sitemap():
    return render_template('sitemap.html')

@views_bp.route('/ticketdetail')
def ticketdetail():
    return render_template('ticketDetails.html')
