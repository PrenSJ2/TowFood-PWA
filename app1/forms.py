from django import forms
from app1.models import *

class addProd(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("collection","id", "brand", "name", "barcode","category","allergens", "weight", "quantity", "footprint","perishable")
        widgets = {
            # 'collection': forms.HiddenInput(),
            'barcode': forms.HiddenInput(),
            'quantity': forms.HiddenInput()
        }

class pickupProd(forms.ModelForm):
    class Meta:
        model = ProductOut
        fields = ("pickup","id", "brand", "name", "barcode","category","allergens", "weight", "quantity", "footprint","perishable")
        widgets = {
            # 'pickup': forms.HiddenInput(),
            'barcode': forms.HiddenInput(),
            'quantity': forms.HiddenInput()
        }
class addCollection(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ("id", "volunteer", "supplier", "larder")

class addPickup(forms.ModelForm):
    class Meta:
        model = Pickup
        fields = ("id", "volunteer", "larder", "member")


class createReport(forms.Form):
    start_date = forms.DateField(label="Start Date", widget=forms.SelectDateWidget(years=range(2016,2022)))
    end_date = forms.DateField(label="End Date", widget=forms.SelectDateWidget(years=range(2016,2022)))
