from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import SoloAvailability, GroupAvailability
from datetime import datetime, timedelta, time
import json


DAYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']


@login_required
def solo_availability_grid(request):
    week_start_str = request.POST.get('week_start') if request.method == 'POST' else request.GET.get('week_start')
    try:
        raw_date = datetime.strptime(week_start_str, "%Y-%m-%d").date()
        week_start = raw_date - timedelta(days=raw_date.weekday() + 1 if raw_date.weekday() != 6 else 0)
    except (TypeError, ValueError):
        today = datetime.today().date()
        week_start = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)

    user = request.user

    # --- DELETE SLOT ---
    if request.method == 'POST' and 'delete_slot' in request.POST:
        try:
            day, hour, scope = request.POST['delete_slot'].split('|')
            hour = int(hour)
            start_time = datetime.strptime(f"{hour:02d}", "%H").time()

            if scope == 'one':
                SoloAvailability.objects.filter(
                    user=user,
                    week_start=week_start,
                    day=day,
                    start_time=start_time
                ).delete()
            elif scope == 'all':
                SoloAvailability.objects.filter(
                    user=user,
                    week_start__gte=week_start,
                    day=day,
                    start_time=start_time
                ).delete()
        except Exception:
            pass

        return redirect(f"{request.path}?week_start={week_start.strftime('%Y-%m-%d')}")

    # --- SAVE SLOT ---
    if request.method == 'POST' and 'selected_slots[]' in request.POST:
        selected_slots = request.POST.getlist('selected_slots[]')
        repeat_weekly = request.POST.get('repeat_weekly') == 'true'

        # Remove existing for current week
        SoloAvailability.objects.filter(user=user, week_start=week_start).delete()

        clean_slots = set()
        for slot in selected_slots:
            try:
                day, hour = slot.split('|')
                if day not in DAYS:
                    continue
                hour = int(hour)
                start = datetime.strptime(f"{hour:02d}", "%H").time()
                end = (datetime.strptime(f"{hour:02d}", "%H") + timedelta(hours=1)).time()
                clean_slots.add((day, start, end))
            except ValueError:
                continue

        for offset in range(10 if repeat_weekly else 1):
            week_offset = week_start + timedelta(weeks=offset)
            for day, start, end in clean_slots:
                obj, _ = SoloAvailability.objects.get_or_create(
                    user=user,
                    week_start=week_offset,
                    day=day,
                    start_time=start,
                    end_time=end
                )
                if repeat_weekly:
                    obj.repeated = True
                    obj.save()

        return redirect(f"{request.path}?week_start={week_start.strftime('%Y-%m-%d')}")

    # --- LOAD VIEW ---
    week_day_dates = [(day, week_start + timedelta(days=i)) for i, day in enumerate(DAYS)]
    saved_slots = SoloAvailability.objects.filter(user=user, week_start=week_start)

    selected_slots = [f"{s.day}|{int(s.start_time.strftime('%H'))}" for s in saved_slots]
    repeated_slots = [f"{s.day}|{int(s.start_time.strftime('%H'))}" for s in saved_slots if getattr(s, 'repeated', False)]

    return render(request, 'availability/solo_grid.html', {
        'week_start': week_start,
        'end_of_week': week_start + timedelta(days=6),
        'week_day_dates': week_day_dates,
        'selected_slots': json.dumps(selected_slots),
        'repeated_slots': json.dumps(repeated_slots),
    })



@login_required
def group_availability_grid(request):
    week_start_str = request.POST.get('week_start') if request.method == 'POST' else request.GET.get('week_start')
    try:
        raw_date = datetime.strptime(week_start_str, "%Y-%m-%d").date()
        week_start = raw_date - timedelta(days=raw_date.weekday() + 1 if raw_date.weekday() != 6 else 0)
    except (TypeError, ValueError):
        today = datetime.today().date()
        week_start = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)

    user = request.user

    # --- DELETE SLOT ---
    if request.method == 'POST' and 'delete_slot' in request.POST:
        try:
            day, hour, scope = request.POST['delete_slot'].split('|')
            hour = int(hour)
            start_time = datetime.strptime(f"{hour:02d}", "%H").time()
            if scope == 'one':
                GroupAvailability.objects.filter(
                    user=user,
                    week_start=week_start,
                    day=day,
                    start_time=start_time
                ).delete()
            elif scope == 'all':
                GroupAvailability.objects.filter(
                    user=user,
                    week_start__gte=week_start,
                    day=day,
                    start_time=start_time
                ).delete()
        except Exception:
            pass

        return redirect(f"{request.path}?week_start={week_start.strftime('%Y-%m-%d')}")

    # --- SAVE SLOT ---
    if request.method == 'POST' and 'selected_slots[]' in request.POST:
        selected_slots = request.POST.getlist('selected_slots[]')
        repeat_weekly = request.POST.get('repeat_weekly') == 'true'

        # Remove existing for this week
        GroupAvailability.objects.filter(user=user, week_start=week_start).delete()

        clean_slots = set()
        for slot in selected_slots:
            try:
                day, hour = slot.split('|')
                if day not in DAYS:
                    continue
                hour = int(hour)
                start = datetime.strptime(f"{hour:02d}", "%H").time()
                end = (datetime.strptime(f"{hour:02d}", "%H") + timedelta(hours=1)).time()
                clean_slots.add((day, start, end))
            except ValueError:
                continue

        for offset in range(10 if repeat_weekly else 1):
            week_offset = week_start + timedelta(weeks=offset)
            for day, start, end in clean_slots:
                obj, _ = GroupAvailability.objects.get_or_create(
                    user=user,
                    week_start=week_offset,
                    day=day,
                    start_time=start,
                    end_time=end
                )
                if repeat_weekly:
                    obj.repeated = True 
                    obj.save()

        return redirect(f"{request.path}?week_start={week_start.strftime('%Y-%m-%d')}")

    # --- GET View: load data for grid ---
    week_day_dates = [(day, week_start + timedelta(days=i)) for i, day in enumerate(DAYS)]
    saved_slots = GroupAvailability.objects.filter(user=user, week_start=week_start)

    selected_slots = [f"{s.day}|{int(s.start_time.strftime('%H'))}" for s in saved_slots]
    repeated_slots = [f"{s.day}|{int(s.start_time.strftime('%H'))}" for s in saved_slots if getattr(s, 'repeated', False)]

    context = {
        'week_start': week_start,
        'end_of_week': week_start + timedelta(days=6),
        'week_day_dates': week_day_dates,
        'selected_slots': json.dumps(selected_slots),
        'repeated_slots': json.dumps(repeated_slots), 
    }
    return render(request, 'availability/group_grid.html', context)

