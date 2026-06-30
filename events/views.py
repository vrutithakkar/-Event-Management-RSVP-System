from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, EventForm
from .models import Event, RSVP


def home(request):
    events = Event.objects.all()

    query = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()

    if query:
        events = events.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if location:
        events = events.filter(location__icontains=location)

    events = events.order_by("event_date", "event_time")

    rsvped_event_ids = set()
    if request.user.is_authenticated:
        rsvped_event_ids = set(
            RSVP.objects.filter(user=request.user).values_list("event_id", flat=True)
        )

    return render(request, "home.html", {
        "events": events,
        "query": query,
        "location": location,
        "rsvped_event_ids": rsvped_event_ids,
    })


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("home")

    else:
        form = RegisterForm()

    return render(request, "register.html", {
        "form": form
    })


@login_required
def create_event(request):

    if request.method == "POST":

        form = EventForm(request.POST)

        if form.is_valid():

            event = form.save(commit=False)

            event.created_by = request.user

            event.save()

            return redirect("home")

    else:

        form = EventForm()

    return render(request, "create_event.html", {
        "form": form
    })


@login_required
def event_detail(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    attendees = event.rsvp_set.select_related("user").all()
    is_rsvped = RSVP.objects.filter(user=request.user, event=event).exists()

    return render(request, "event_detail.html", {
        "event": event,
        "attendees": attendees,
        "is_rsvped": is_rsvped,
        "attendee_count": attendees.count(),
    })


@login_required
def update_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    if event.created_by != request.user:
        return redirect("home")

    if request.method == "POST":

        form = EventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = EventForm(instance=event)

    return render(request, "update_event.html", {
        "form": form
    })


@login_required
def delete_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    if event.created_by != request.user:
        return redirect("home")

    if request.method == "POST":
        event.delete()
        return redirect("home")

    return render(request, "delete_event.html", {
        "event": event
    })


@login_required
def toggle_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    rsvp = RSVP.objects.filter(user=request.user, event=event).first()

    if rsvp:
        rsvp.delete()
        messages.success(request, f"You cancelled your RSVP for {event.title}.")
    else:
        RSVP.objects.create(user=request.user, event=event)
        if request.user.email:
            send_mail(
                subject=f"RSVP confirmed: {event.title}",
                message=(
                    f"Hi {request.user.username}, you successfully RSVP'd for '{event.title}' "
                    f"on {event.event_date} at {event.event_time}."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,
            )
        messages.success(request, f"You RSVP'd for {event.title}.")

    return redirect(request.META.get("HTTP_REFERER", "home"))