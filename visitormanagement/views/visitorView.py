from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin

from visitor_token.models import VisitorToken
from visitormanagement.forms import VisitorCreateForm
from visitormanagement.models import Visitors


class Visitor(LoginRequiredMixin, View):
    # permission_required = 'visitormanagement.view_visitors'
    form_class = VisitorCreateForm
    initial = {'key': 'value'}
    template_name = 'visitormanagement/add_new_visitor.html'

    def get(self, request, *args, **kwargs):
        allvisitor = Visitors.objects.all()
        form = self.form_class(initial=self.initial)
        # breakpoint()
        return render(request, self.template_name, {'visitorform': form})

    '''
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            visitor_name = form.cleaned_data["visitor_name"]
            visitor_address = form.cleaned_data["visitor_address"]
            to_which_department = form.cleaned_data["to_which_department"]
            visitor_purpose = form.cleaned_data["visitor_purpose"]
            to_employee = form.cleaned_data["to_employee"]
            visitor_phone_number = form.cleaned_data["visitor_phone_number"]
            visitor_email = form.cleaned_data["visitor_email"]
            #new_token = VisitorToken(token_for = visitor_name, token =  VisitorToken.get_token)
            new_visitor = Visitors( visitor_name = visitor_name, visitor_address = visitor_address,visitor_phone_number=visitor_phone_number,
            visitor_email=visitor_email,to_which_department = to_which_department,visitor_purpose = visitor_purpose,to_employee = to_employee)
            new_visitor.save()
            #return redirect('visitor')
            return redirect('tokenpdf')

        return render(request, self.template_name, {'visitorform': form})
        '''
