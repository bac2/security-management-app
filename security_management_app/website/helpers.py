from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

def send_vuln_notification(recipient, device, application):
    template = get_template("emails/vuln_notification.txt")
    render_context = Context({
            'device': device,
            'application': application,
        })
    render = template.render(render_context)
    send_mail("Vulnerability Detected", render, "admin@vulmo.nojones.net", [recipient], fail_silently=False)

if __name__ == "__main__":
    send_vuln_notification("nick@nojones.net", "Test Message")
