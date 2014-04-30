from website.models import Vulnerability

def find_vulnerabilities(update):
    return Vulnerability.objects.filter(application__updateapplications__update=update)
    
    
