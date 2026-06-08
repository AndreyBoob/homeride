from flask import redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.bookings import bp
from app import db
from app.models import Trip, Booking
from datetime import datetime

@bp.route('/create/<int:trip_id>', methods=['POST'])
@login_required
def create(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    if trip.driver_id == current_user.id:
        flash('Вы не можете забронировать свою поездку', 'danger')
        return redirect(url_for('trips.detail', trip_id=trip.id))
    
    if trip.available_seats <= 0:
        flash('В этой поездке нет свободных мест', 'danger')
        return redirect(url_for('trips.detail', trip_id=trip.id))
    
    seats = int(request.form.get('seats', 1))
    
    if seats > trip.available_seats:
        flash('Недостаточно свободных мест', 'danger')
        return redirect(url_for('trips.detail', trip_id=trip.id))
    
    # Создаем бронирование
    booking = Booking(
        trip_id=trip.id,
        passenger_id=current_user.id,
        seats=seats,
        status='pending'
    )
    db.session.add(booking)
    
    # Уменьшаем количество мест
    trip.available_seats -= seats
    
    db.session.commit()
    
    flash(f'Бронирование создано! Ожидайте подтверждения от водителя.', 'success')
    return redirect(url_for('bookings.my_bookings'))