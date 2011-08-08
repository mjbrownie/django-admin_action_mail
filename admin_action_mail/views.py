from django.contrib.auth.decorators import permission_required
from django import forms
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect

from admin_action_mail.tasks import send_email_batch, dotgetattr

class AdminMailForm(forms.Form):
    subject = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

@permission_required('admin_action_mail.can_admin_action_mail')
def mail_form (request):
    """Mail to Group Form"""

    opts = request.session['admin_action_mail']

    queryset = getattr(opts['model'],opts['manager']).filter(
            id__in = opts['ids']
            )

    emails = [dotgetattr(o,opts['email_dot_path']) \
            for o in queryset]

    if request.method == 'POST':
        form = AdminMailForm(request.POST)

        if form.is_valid():

            send_email_batch(queryset,form,opts)

            messages.add_message(request, messages.SUCCESS,
                "Mail has been sent to %s Users" % len(emails)
            )

            return HttpResponseRedirect(opts['return_addr'])
    else:
        form = AdminMailForm()

    return render_to_response('admin_action_mail/mail_form.html', locals(),
            context_instance=RequestContext(request)
    )
