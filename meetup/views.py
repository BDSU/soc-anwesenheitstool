import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseForbidden, Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView

from .forms import MeetingForm
from .models import Meeting, Participant


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MeetingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect("index")

    form = MeetingForm()
    meetings = Meeting.objects.all()

    return render(request, 'index.html', {'form': form, "meetings": meetings})


class MeetingDetailView(DetailView):
    model = Meeting
    slug_field = "pk"
    template_name = "meeting_details.html"
    context_object_name = "meeting"


def update_meeting(request, pk):
    meeting = Meeting.objects.get(id=pk)

    form = MeetingForm(instance=meeting)

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect("index")
    return render(request, "update_meeting.html", {"meeting_edit_form": form})


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

    try:
        participant = user.participant_set.filter(meeting_id=meeting.pk).get()
    except Participant.DoesNotExist:
        return HttpResponseForbidden("Benutzer ist nicht zur Veranstaltung eingeladen")

    context = {'meeting': meeting}
    if request.method == "GET":
        return render(request, template_name="checkin/checkin_dialog.html", context={**context, 'checked_in': participant.attendant})
    else:
        assert request.method == "POST"
        if participant.attendant:
            return HttpResponseBadRequest("Benutzer ist bereits als anwesend markiert")

        participant.attendant = True
        participant.save()

        return render(request, template_name="checkin/checkin_success.html", context=context)

