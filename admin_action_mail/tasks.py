from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def dotgetattr(instance, attstring):
    """
    This is to convert a fk relationship specified as a string eg 'relative.to.user'
    """
    for att in attstring.split('.'):
        try:
            instance = getattr(instance,att)
        except:
            return None

    return instance

def send_email_batch(queryset,form, opts):
    """
    email batch routine. This should be asynced
    """

    for o in queryset:
        addr = dotgetattr(o,
                opts['email_dot_path'])

        email_text  = render_to_string(
                opts['email_template_text'],
                {
                    'object':o,
                    'addr':addr,
                    'content': form.cleaned_data['content'] }
                )

        email_html = render_to_string(
                opts['email_template_html'],
                {
                    'object':o,
                    'addr':addr,
                    'content': form.cleaned_data['content'] }
                )

        email  = EmailMultiAlternatives(
                form.cleaned_data['subject'],
                email_text,
                opts['reply_to'],
                [addr]
                )
        email.attach_alternative(email_html,'text/html')
        email.send()
