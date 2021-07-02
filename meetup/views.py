from django.shortcuts import redirect, render
from .forms import MeetingForm
from .models import Meeting


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