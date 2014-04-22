from django import forms

class AddDeviceForm(forms.Form):
    """
    Form used to process answers to challenges
    """
    uid = forms.CharField(max_length=50)
    nickname = forms.CharField(max_length=50)