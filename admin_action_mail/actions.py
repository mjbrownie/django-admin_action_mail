#mail to group admin action
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def mail_action(description="Mail to selected Users",
        email_dot_path='email',
        email_template_html = 'admin_action_mail/email.html',
        email_template_text = 'admin_action_mail/email.txt',
        manager = '_default_manager',
        reply_to = None):
    """
    Example Usage:
    class SomeModelAdmin:
        class Meta:
            actions=[
                admin_action_mail_action(
                description='Email Selected Users',
                email_dot_path = 'profile.user.email',
                )
            ]
    """

    def admin_action_mail(modeladmin,request,queryset):

        request.session['admin_action_mail']= {
            'ids'            : [v[0] for v in queryset.values_list('pk')],
            'model'          : modeladmin.model,
            'email_dot_path' : email_dot_path,
            'email_template_html' : email_template_html,
            'email_template_text' : email_template_text,
            'manager'        : manager,
            'return_addr'    : request.META['HTTP_REFERER'],
            'reply_to'       : reply_to or request.user.email,
        }

        return HttpResponseRedirect(reverse('admin_action_mail-form'))

    admin_action_mail.short_description = description

    return admin_action_mail
