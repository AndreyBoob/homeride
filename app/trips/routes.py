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

@bp.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchTripForm()
    query = Trip.query.filter_by(status='active')
    
    city = session.get('search_city')
    street = session.get('search_street')
    
    if request.method == 'POST':
        city = request.form.get('city')
        street = request.form.get('street')
        
        session['search_city'] = city
        session['search_street'] = street
        
        if city:
            query = query.filter(
                db.or_(
                    Trip.from_city.ilike(f'%{city}%'),
                    Trip.to_city.ilike(f'%{city}%')
                )
            )
        
        if street:
            query = query.filter(
                db.or_(
                    Trip.from_street.ilike(f'%{street}%'),
                    Trip.to_street.ilike(f'%{street}%')
                )
            )
    
    trips = query.order_by(Trip.departure_date, Trip.departure_time).all()
    return render_template('trips/search.html', form=form, trips=trips, city=city, street=street)

@bp.route('/search/clear')
def clear_search():
    session.pop('search_city', None)
    session.pop('search_street', None)
    return redirect(url_for('trips.search'))

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