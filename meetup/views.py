import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth import logout

import csv


from .forms import MeetingForm
from .models import Meeting, Participant


@staff_member_required
def export(request, pk):
    response = HttpResponse(content_type='text/csv')
    teilnehmer_list = Participant.objects.filter(meeting=pk)
    meeting = Meeting.objects.get(id=pk)

    writer = csv.writer(response)
    writer.writerow(['Vorname', 'Nachname', 'Anwesenheit'])

    for teilnehmer in teilnehmer_list:
        attendance = "anwesend" if teilnehmer.attendant else "nicht anwesend"

        writer.writerow([teilnehmer.user.first_name,
                        teilnehmer.user.last_name, attendance])

    csv_name = meeting.name + " - " + str(meeting.date) + ".csv"
    response['Content-Disposition'] = 'attachment; filename=' + csv_name
    return response


@login_required
def index(request):
    assert request.user.is_authenticated
    user = request.user

    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MeetingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect("index")

    meetings = Meeting.objects.filter(participant__user=user)

    return render(request, 'index.html',
                  {"meetings": meetings, 'user_is_admin': user.is_superuser})


class MeetingDetailView(DetailView):
    model = Meeting
    slug_field = "pk"
    template_name = "meeting_details.html"
    context_object_name = "meeting"


@staff_member_required
def update_meeting(request, pk):
    meeting = Meeting.objects.get(id=pk)

    form = MeetingForm(instance=meeting)

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect("index")
    return render(request, "legacy/update_meeting.html", {"meeting_edit_form": form})


@staff_member_required
def delete_meeting(request, pk):
    meeting = Meeting.objects.get(id=pk)
    meeting.delete()
    return redirect("index")


@login_required
@require_http_methods(["GET", "POST"])
def checkin_view(request: HttpRequest, slug: uuid.UUID):
    # This is a function-based view, because form-submission without an actual form is not really
    # supported by any generic view :(
    meeting = get_object_or_404(Meeting, presence_registration_uuid=slug)

    assert request.user.is_authenticated
    user = request.user
    context = {'meeting': meeting}

    try:
        participant = user.participant_set.filter(meeting_id=meeting.pk).get()
    except Participant.DoesNotExist:
        return render(request, template_name="checkin/checkin_not_allowed.html", context=context)

    if request.method == "GET":
        return render(request, template_name="checkin/checkin_dialog.html",
                      context={**context, 'checked_in': participant.attendant})
    else:
        assert request.method == "POST"
        if participant.attendant:
            return HttpResponseBadRequest("Benutzer ist bereits als anwesend markiert")

        participant.attendant = True
        participant.save()

        return render(request, template_name="checkin/checkin_success.html", context=context)


def logout_view(request):
    logout(request)
    return redirect("index")
