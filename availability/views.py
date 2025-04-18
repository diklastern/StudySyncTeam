from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import SoloAvailability, GroupAvailability
from datetime import datetime, timedelta
import json



@login_required
def solo_availability_grid(request):
    # Determine selected week from POST or GET
    if request.method == 'POST':
        week_start_str = request.POST.get('week_start')
    else:
        week_start_str = request.GET.get('week_start')

    try:
        raw_date = datetime.strptime(week_start_str, "%Y-%m-%d").date()
        week_start = raw_date - timedelta(days=raw_date.weekday() + 1 if raw_date.weekday() != 6 else 0)
    except (TypeError, ValueError):
        today = datetime.today().date()
        week_start = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)

    # Handle saving new availability
    if request.method == 'POST':
        selected_slots = request.POST.getlist('selected_slots[]')

        # Delete previous availability for that week
        SoloAvailability.objects.filter(user=request.user, week_start=week_start).delete()

        for slot in selected_slots:
            parts = slot.split('|')
            if len(parts) != 2:
                print(f"Skipping malformed slot (wrong format): {slot}")
                continue

            day, start_hour = parts
            try:
                start = datetime.strptime(start_hour, "%H").time()
                end = (datetime.strptime(start_hour, "%H") + timedelta(hours=1)).time()
            except ValueError:
                print(f"Skipping malformed time: {slot}")
                continue

            if day not in ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']:
                print(f"Skipping invalid day: {day}")
                continue

            SoloAvailability.objects.create(
                user=request.user,
                week_start=week_start,
                day=day,
                start_time=start,
                end_time=end
            )

        # Preserve selected week after redirect
        return redirect(f"{request.path}?week_start={week_start.strftime('%Y-%m-%d')}")

    # Load existing availability
    WEEK_DAYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    week_day_dates = [(day, week_start + timedelta(days=i)) for i, day in enumerate(WEEK_DAYS)]
    saved_slots = SoloAvailability.objects.filter(user=request.user, week_start=week_start)
    formatted_slots = [f"{slot.day}|{slot.start_time.strftime('%H')}" for slot in saved_slots]
    selected_slots_json = json.dumps(formatted_slots) 

    end_of_week = week_start + timedelta(days=6)
    return render(request, 'availability/solo_grid.html', {
        'week_start': week_start,
        'end_of_week': end_of_week,
        'week_day_dates': week_day_dates,
        'selected_slots': selected_slots_json
    })
    
    
@login_required
def group_availability_grid(request):
    if request.method == 'POST':
        week_start_str = request.POST.get('week_start')
    else:
        week_start_str = request.GET.get('week_start')

    try:
        raw_date = datetime.strptime(week_start_str, "%Y-%m-%d").date()
        week_start = raw_date - timedelta(days=raw_date.weekday() + 1 if raw_date.weekday() != 6 else 0)
    except (TypeError, ValueError):
        today = datetime.today().date()
        week_start = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)


    if request.method == 'POST':
        selected_slots = request.POST.getlist('selected_slots[]')
        GroupAvailability.objects.filter(user=request.user, week_start=week_start).delete()

        for slot in selected_slots:
            parts = slot.split('|')
            if len(parts) != 2:
                continue
            day, start_hour = parts
            try:
                start = datetime.strptime(start_hour, "%H").time()
                end = (datetime.strptime(start_hour, "%H") + timedelta(hours=1)).time()
            except ValueError:
                continue
            if day not in ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']:
                continue

            GroupAvailability.objects.create(
                user=request.user,
                week_start=week_start,
                day=day,
                start_time=start,
                end_time=end
            )

        return redirect(f"{request.path}?week_start={week_start.strftime('%Y-%m-%d')}")

    WEEK_DAYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    week_day_dates = [(day, week_start + timedelta(days=i)) for i, day in enumerate(WEEK_DAYS)]
    end_of_week = week_start + timedelta(days=6)
    saved_slots = GroupAvailability.objects.filter(user=request.user, week_start=week_start)
    formatted_slots = [f"{slot.day}|{slot.start_time.strftime('%H')}" for slot in saved_slots]
    selected_slots_json = json.dumps(formatted_slots) 

    return render(request, 'availability/group_grid.html', {
        'week_start': week_start,
        'end_of_week': end_of_week,
        'week_day_dates': week_day_dates,
        'selected_slots': selected_slots_json
    })