from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView

from visitingpurpose.forms import VisitingPurposeForm, VisitingPurposeUpdateForm
from visitingpurpose.models import VisitingPurpose
import sweetify
from sweetify.views import SweetifySuccessMixin
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.


class ReasonDataTable(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':
                dataList = VisitingPurpose.objects.all().order_by('purpose_name')
                search_value = request.POST['search[value]'].strip()
                startLimit = int(request.POST['start'])
                endLimit = startLimit + int(request.POST['length'])
                data_array = []
                totalLength = VisitingPurpose.objects.count()

                if search_value != '':
                    # Querying dataset
                    dataList = dataList.filter(
                        Q(purpose_name__contains=search_value)).order_by('-purpose_name')
                    dataFilter = dataList[startLimit:endLimit]
                    filterLength = dataList.count()
                else:
                    dataFilter = dataList[startLimit:endLimit]
                    filterLength = dataList.count()

                i = 0
                for key, item in enumerate(dataFilter):
                    for field in VisitingPurpose._meta.fields:
                        value = getattr(item, field.name)
                        if value is None:
                            setattr(item, field.name, "")

                    update_url = reverse(
                        'visitingpurposeupdatetview', args=[item.id])
                    delete_url = reverse('reason.delete', kwargs={
                                         'reason_id': item.id})
                    formatted_purpose_name = "<b class='text-sm' >" + item.purpose_name + "</b>"
                    action = f"""
                    <div class="d-flex justify-content-center gap-2">
                    <a class="btn btn-info btn-sm" href="{update_url}">Update</a>
                    <a class="btn btn-danger btn-sm" href="javascript:void(0);"onclick="deleteConfirmation('{delete_url}')">Delete</a>
                    </div>
                    """
                    # action += f"""<a class="btn btn-info btn-sm" href="{update_url}">Update</a>"""
                    # action += f"""<a class="m-2 btn btn-danger btn-sm" href="javascript:void(0);"onclick="deleteConfirmation('{delete_url}')">Delete</a>"""
                    row_array = [str(key + 1), formatted_purpose_name, action]
                    i += 1
                    data_array.append(row_array)

                response = {
                    "draw": request.POST['draw'],
                    "recordsTotal": totalLength,
                    "recordsFiltered": filterLength,
                    "data": data_array,
                }
                return JsonResponse(response)


class VisitingPurposeView(PermissionRequiredMixin, LoginRequiredMixin, SweetifySuccessMixin, View):
    permission_required = "visitingpurpose.custom_can_view_visiting_reason"
    form_class = VisitingPurposeForm
    initial = {'key': 'value'}
    template_name = 'visitingpurpose/purpose_crud.html'
    visiting_purpose_update_form = VisitingPurposeUpdateForm()

    def get(self, request, *args, **kwargs):
        allpurpose = VisitingPurpose.objects.all()
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'purposeform': form, "allpurpose": allpurpose, "visiting_purpose_update_form": self.visiting_purpose_update_form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            purpose_name = form.cleaned_data["purpose_name"]
            newpurpose = VisitingPurpose(purpose_name=purpose_name)
            newpurpose.save()
            sweetify.success(
                request, 'New visiting Reason added successfully!')
            return redirect('visitingpurpose')
        return render(request, self.template_name, {'purposeform': form})


class VisitingPurposeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SweetifySuccessMixin, UpdateView):
    permission_required = 'visitingpurpose.custom_can_update_visiting_reason'
    model = VisitingPurpose
    # fields = ['purpose_name']
    form_class = VisitingPurposeUpdateForm
    template_name = "visitingpurpose/purpose_update.html"
    success_message = 'Visiting Purpose successfully updated!'
    success_url = "/purpose/"


class VisitingPurposeDeleteView(PermissionRequiredMixin, LoginRequiredMixin, SweetifySuccessMixin, DeleteView):
    permission_required = 'visitingpurpose.custom_can_delete_visiting_reason'
    model = VisitingPurpose
    template_name = "visitingpurpose/purpose_crud.html"
    success_message = 'Visiting Purpose  Deleted!'
    success_url = "/purpose/"


@login_required
def reasoneDelete(request, reason_id):
    reason_instance = VisitingPurpose.objects.get(pk=reason_id)
    reason_instance.delete()
    return HttpResponseRedirect(reverse("visitingpurpose"))
