from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import SoloAvailability
from datetime import datetime, timedelta


def solo_availability_view(request):
    return render(request, "availability/solo_form.html", {})

def group_availability_view(request):
    return render(request, "availability/group_form.html", {})


@login_required
def solo_availability_grid(request):
    # Determine default Sunday
    today = datetime.today().date()
    sunday = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)

    if request.method == 'POST':
        week_start_str = request.POST.get('week_start')
        selected_slots = request.POST.getlist('selected_slots[]')

        try:
            week_start = datetime.strptime(week_start_str, "%Y-%m-%d").date()
        except ValueError:
            # Fallback to current Sunday if input is bad
            week_start = sunday

        # Remove previous availability entries for the selected week
        SoloAvailability.objects.filter(user=request.user, week_start=week_start).delete()

        # Save valid slots only
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

        return redirect('solo_availability_grid')

    # GET request
    WEEK_DAYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    return render(request, 'availability/solo_grid.html', {
        'week_start': sunday,
        'week_days': WEEK_DAYS
    })