from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.trips import bp
from app.trips.forms import TripForm
from app import db
from app.models import Trip
from datetime import datetime

@bp.route('/')
def home():
    return render_template('trips/home.html')

@bp.route('/search')
def search():
    # Получаем параметры поиска
    from_loc = request.args.get('from', '')
    to_loc = request.args.get('to', '')
    date = request.args.get('date', '')
    
    # Проверяем, был ли поиск
    has_searched = bool(from_loc or to_loc or date)
    
    trips = []
    
    if has_searched:
        query = Trip.query.filter_by(status='active')
        
        if from_loc:
            query = query.filter(Trip.from_location.ilike(f'%{from_loc}%'))
        if to_loc:
            query = query.filter(Trip.to_location.ilike(f'%{to_loc}%'))
        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            query = query.filter(Trip.departure_date == date_obj)
        
        trips = query.order_by(Trip.departure_date.asc(), Trip.departure_time.asc()).all()
    
    return render_template('trips/search.html', trips=trips, has_searched=has_searched)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TripForm()
    if form.validate_on_submit():
        trip = Trip(
            from_location=form.from_location.data,
            to_location=form.to_location.data,
            departure_date=form.departure_date.data,
            departure_time=form.departure_time.data,
            available_seats=form.available_seats.data,
            price=form.price.data,
            description=form.description.data,
            driver_id=current_user.id
        )
        db.session.add(trip)
        db.session.commit()
        flash('Поездка успешно создана!', 'success')
        return redirect(url_for('trips.my_trips'))
    
    return render_template('trips/create.html', form=form)

@bp.route('/my')
@login_required
def my_trips():
    trips = Trip.query.filter_by(driver_id=current_user.id).order_by(Trip.departure_date.desc()).all()
    return render_template('trips/my_trips.html', trips=trips)

@bp.route('/<int:trip_id>')
def detail(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return render_template('trips/detail.html', trip=trip)