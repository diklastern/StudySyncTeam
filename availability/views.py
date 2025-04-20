from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from availability.models import SoloAvailability, GroupAvailability

DAYS = ['sun','mon','tue','wed','thu','fri','sat']

@login_required
def availability_grid_view(request, mode='solo'):
    Model = SoloAvailability if mode == 'solo' else GroupAvailability
    template_name = 'availability/availability_grid.html'

    week_start_str = request.GET.get('week_start') or request.POST.get('week_start')
    try:
        raw_date = datetime.strptime(week_start_str, "%Y-%m-%d").date()
        week_start = raw_date - timedelta(days=raw_date.weekday() + 1 if raw_date.weekday() != 6 else 0)
    except (TypeError, ValueError):
        today = datetime.today().date()
        week_start = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)

    week_day_dates = [(d, week_start + timedelta(days=i)) for i, d in enumerate(DAYS)]
    end_of_week = week_start + timedelta(days=6)

    selected_slots = set()
    repeated_slots = set()
    qs = Model.objects.filter(user=request.user).filter(Q(week_start=week_start) | Q(repeated=True))
    for slot in qs:
        start_hour = slot.start_time.hour
        end_hour = slot.end_time.hour
        for hour in range(start_hour, end_hour):
            key = f"{slot.day}|{hour}"
            selected_slots.add(key)
            if slot.repeated:
                repeated_slots.add(key)

    if request.method == 'POST':
        delete_key = request.POST.get('delete_slot')
        if delete_key:
            day, hour, scope = delete_key.split('|')
            target_time = datetime.strptime(f"{hour}:00", "%H:%M").time()
            if scope == 'one':
                Model.objects.filter(user=request.user, week_start=week_start, day=day, start_time=target_time).delete()
            else:
                Model.objects.filter(user=request.user, day=day, start_time=target_time, repeated=True).delete()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'ok'})
            else:
                return redirect(request.path + f'?week_start={week_start}')

        repeat_weekly = request.POST.get('repeat_weekly') in ['true', 'on', '1']
        slots = request.POST.getlist('selected_slots[]')
        for slot_key in slots:
            day, hour = slot_key.split('|')
            start = datetime.strptime(hour + ':00', '%H:%M').time()
            end = (datetime.strptime(hour, '%H') + timedelta(hours=1)).time()
            obj, created = Model.objects.get_or_create(
                user=request.user,
                week_start=week_start,
                day=day,
                start_time=start,
                defaults={
                    'end_time': end,
                    'repeated': repeat_weekly,
                }
            )
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})
        return redirect(request.path + f'?week_start={week_start}')

    return render(request, template_name, {
        'week_start': week_start,
        'end_of_week': end_of_week,
        'week_day_dates': week_day_dates,
        'selected_slots': list(selected_slots),
        'repeated_slots': list(repeated_slots),
        'title': 'Solo' if mode == 'solo' else 'Group',
    })