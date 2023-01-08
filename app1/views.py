from cgi import test
from collections import namedtuple
import imp
from math import prod
from re import X
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import get_object_or_404, render, redirect
from app1.models import *
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from app1.forms import *
from django.utils import timezone
from rest_framework import viewsets
from .serializers import ProductSerializer
from django.http.request import HttpRequest
from datetime import datetime
from django.db import connection
import re


# API for product Pick up, product autofill with barcode
# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        super(ProductViewSet, self).get_queryset()
        barcode = self.request.query_params.get('barcode', None)
        print("Barcode = ", barcode)
        print(self)
        queryset = Product.objects.all()
        if barcode:
            queryset = Product.objects.filter(barcode=barcode)
        return queryset


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "home.html", {'nbar': 'home'})
        else:
            return render(request, "login.html", {'nbar': 'login'})
    return render(request, "login.html")


def logout_view(request):
    return render(request, "logout.html")


def register_view(request):
    return render(request, "login.html")


def home(request):
    return render(request, "home.html", {'nbar': 'home'})


def stock(request):
    return render(request, "stock.html", {'nbar': 'stock'})


def scan_in_1(request):

    print("Adding Collection")
    # print(request.POST)
    c_form = addCollection(request.POST or None)
    if request.method == "POST" and c_form.is_valid():
        collection = c_form.save(commit=False)
        collection.log_data = timezone.now()
        collection.save()
        form = addProd(initial={"collection": collection.id})
        return render(request, "scan_in.html", {'nbar': 'scan_in', "form": form})
    else:
        print("Form is not valid")
        print(c_form.errors)
        return render(request, "scan_in_1.html", {'nbar': 'scan_in', "c_form": c_form})


def add_product(request):
    # from database
    # today = timezone.today()
    # year = today.year
    # month = today.month
    # day = today.day
    # product_qs_today = Product.objects.filter(created_at=today)
    context = {
        # "product_qs_today": product_qs_today,
    }
    print("Adding Product")
    # print(request.POST)
    form = addProd(request.POST or None)
    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        # Check if a product with the same barcode already exists
        existing_product = Product.objects.filter(barcode=product.barcode).first()
        if existing_product:
            # If a product with the same barcode exists, increase its quantity by 1
            existing_product.quantity += 1
            existing_product.save()
        else:
            # If a product with the same barcode does not exist, save the new product
            product.log_data = timezone.now()
            product.save()
        form = addProd(initial={"collection": product.collection})
        return render(request, "scan_in.html", {'nbar': 'scan_in', "form": form, "context": context})
    else:
        form = addProd()
        print("Form is not valid")
        print(form.errors)
        return render(request, "scan_in.html", {'nbar': 'scan_in', "form": form, "context": context})


def total_stock(request):
    # from database
    with connection.cursor() as cursor2:
        cursor2.execute("DROP TABLE IF EXISTS current_stock")
        cursor2.execute("CREATE TABLE current_stock (id int, brand varchar(100), name varchar(100), barcode int, category varchar(500), perishable bool, allergens varchar(500), weight real, quantity int, footprint real) ;")
        cursor2.execute(
            "INSERT INTO current_stock SELECT id, brand, name, barcode, category, perishable, allergens, weight, quantity, footprint FROM app1_product;")
        cursor2.execute("Select * FROM current_stock;")

        def namedtuplefetchall(cursor2):
            "Return all rows from a cursor as a namedtuple"
            desc = cursor2.description
            nt_result = namedtuple('Result', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor2.fetchall()]
        current_stock_data = namedtuplefetchall(cursor2)
    context = {
        "product_qs": current_stock_data,
    }

    HTML_String = render_to_string("total_stock.html", context=context)
    return HttpResponse(HTML_String)
    # return render(request, "total_stock.html", {'nbar': 'stock'}, context=context)


def people(request):
    return render(request, "people.html", {'nbar': 'people'})


def members(request):
    members = Member.objects.all()
    return render(request, "members.html", {'nbar': 'members', 'members': members})


def searchAjax(request, q):
    print(q)
    memberList = Member.objects.filter(lastName__contains=q)
    n = len(memberList)
    print(n)
    if (n > 0):
        # table key
        out = "<table class='table table-compact w-full px-4'><thead><tr><th>ID</th><th>First Name</th><th>Last Name</th><th>Adults</th><th>Children</th><th>Address</th><th>Post Code</th><th>Food Allergies</th><th>Collected this week</th></tr></thead><tbody>"
        for x in memberList:
            out += "<tr>"
            out += "<th>"+str(x.id)+"</th>"
            out += "<td>"+x.firstName+"</td>"
            out += "<td>"+x.lastName+"</td>"
            out += "<td>"+str(x.noAdults)+"</td>"
            out += "<td>"+str(x.noChildren)+"</td>"
            out += "<td>"+x.addressFirstLine+"</td>"
            out += "<td>"+x.postCode+"</td>"
            out += "<td>"+x.foodAllergies+"</td>"
            out += "</tr>"
        out += "</tbody>"
        out += "</table>"
    else:
        out = "<table class='table table-compact w-full px-4'><thead>"
        out += "<th>no matching results</th>"
        out += "</thead>"
        out += "</table>"
    print(out)
    return HttpResponse(out)


def p_search(request, p):
    print(p)

    # create current stock table
    # with connection.cursor() as cursor:
    with connection.cursor() as cursor2:
        cursor2.execute("DROP TABLE current_stock")
        cursor2.execute("CREATE TABLE current_stock (id int, brand varchar(100), name varchar(100), barcode int, category varchar(500), perishable bool, allergens varchar(500), weight real, quantity int, footprint real) ;")
        cursor2.execute(
            "INSERT INTO current_stock SELECT id, brand, name, barcode, category, perishable, allergens, weight, quantity, footprint FROM app1_product;")
        cursor2.execute(
            "Select * FROM current_stock WHERE CONTAINS(name, '"+p+"');")

        def namedtuplefetchall(cursor2):
            "Return all rows from a cursor as a namedtuple"
            desc = cursor2.description
            nt_result = namedtuple('Result', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor2.fetchall()]
        current_stock_data = namedtuplefetchall(cursor2)

    n = len(current_stock_data)
    print(n)
    if (n > 0):
        # table key
        out = "<table class='table table-compact w-full px-4'><thead><tr><th>Name</th><th>Brand</th><th>Category</th><th>Perishable</th><th>Weight</th><th>Barcode</th></tr></thead><tbody>"
        for x in current_stock_data:
            out += "<tr>"
            out += "<td>"+x.name+"</td>"
            out += "<td>"+x.brand+"</td>"
            out += "<td>"+x.category+"</td>"
            out += "<td>"+str(x.perishable)+"</td>"
            out += "<td>"+str(x.weight)+"</td>"
            out += "<td>"+str(x.barcode)+"</td>"
            out += "</tr>"
        out += "</tbody>"
        out += "</table>"
    else:
        out = "<table class='table table-compact w-full px-4'><thead>"
        out += "<th>no matching results</th>"
        out += "</thead>"
        out += "</table>"
    print(out)
    return HttpResponse(out)


def add_member(request):
    return render(request, "add_member.html", {'nbar': 'add_member'})

# def product_view(request, id):
#     context = {

#     }

#     context["data"] = Product.objects.get(id = id)

#     return render(request, "product_view.html", {'nbar': 'stock'}, context=context)

# def update_product(request, id):
#         context = {

#         }

#         product = get_object_or_404(Product, id = id)

#         form = addProd(request.POST or None, instance = product)

#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/stock/" + id)
#         context["form"] = form
#         return render(request, "update_product.html", {'nbar': 'stock'})


def scan_out_1(request):

    print("Adding Pickup")
    # print(request.POST)
    p_form = addPickup(request.POST or None)
    if request.method == "POST" and p_form.is_valid():
        pickup = p_form.save(commit=False)
        pickup.log_data = timezone.now()
        pickup.save()
        p2_form = pickupProd(initial={"pickup": pickup.id})
        return render(request, "scan_out.html", {'nbar': 'scan_out', "p2_form": p2_form})
    else:
        print("Form is not valid")
        print(p_form.errors)
        return render(request, "scan_out_1.html", {'nbar': 'scan_out', "p_form": p_form})


def scan_out(request):
    # from database
    # today = timezone.today()
    # year = today.year
    # month = today.month
    # day = today.day
    # product_qs_today = Product.objects.filter(created_at=today)
    context = {
        # "product_qs_today": product_qs_today,
    }
    print("Adding Product to Pickup")
    # print(request.POST)
    p2_form = pickupProd(request.POST or None)
    if request.method == "POST" and p2_form.is_valid():
        product = p2_form.save(commit=False)
        # Check if a product with the same barcode already exists
        existing_product = ProductOut.objects.filter(barcode=product.barcode).first()
        if existing_product:
            # If a product with the same barcode exists, decrease its quantity by 1
            existing_product.quantity -= 1
            existing_product.save()
        else:
            # If a product with the same barcode does not exist, save the new product
            product.log_data = timezone.now()
            product.save()
        p2_form = pickupProd(initial={"pickup": product.pickup})
        return render(request, "scan_out.html", {'nbar': 'scan_out', "p2_form": p2_form, "context": context})
    else:
        p2_form = pickupProd()
        print("Form is not valid")
        print(p2_form.errors)
        return render(request, "scan_out.html", {'nbar': 'scan_out', "p2_form": p2_form, "context": context})

def reports(request):
    alert = " "
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    return render(request, "reports.html", {'nbar': 'reports', "alert": alert})


def larder_report(request):
    alert = "No date range selected"
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    if start_date == " " or end_date == " ":
        return render(request, "reports.html", {'nbar': 'reports', "alert": alert})
    default_ms = '.000000'
    start_datetime = str(datetime.strptime(
        start_date, '%d/%m/%Y')) + default_ms
    end_datetime = str(datetime.strptime(end_date, '%d/%m/%Y')) + default_ms
    print("Start Date & Time: " + start_date + start_datetime +
          "\n End Date & Time: " + end_date + end_datetime)

    # Larder Location
    larder = 'Towcester Community Center'

    # from database

    with connection.cursor() as cursor:
        # Larder ID
        cursor.execute("SELECT id FROM app1_larder WHERE name = %s", [larder])
        larder_id = cursor.fetchone()[0]
        # print(larder_id)
        # New Members in date range
        cursor.execute('SELECT COUNT(*) FROM app1_member WHERE created_at BETWEEN %s AND %s AND prefLarder_id = %s',
                       [start_datetime, end_datetime, larder_id])
        new_members = cursor.fetchone()[0]
        # print(new_members)
        # New Volunteers in date range
        cursor.execute('SELECT COUNT(*) FROM app1_volunteer WHERE created_at BETWEEN %s AND %s AND prefLarder_id = %s',
                       [start_datetime, end_datetime, larder_id])
        new_volunteers = cursor.fetchone()[0]
        # print(new_volunteers)

        # Collections in date range
        cursor.execute('SELECT id FROM app1_collection WHERE created_at BETWEEN %s AND %s AND larder_id = %s', [
                       start_datetime, end_datetime, larder_id])
        collection_ids = re.findall(r'\d+', str(cursor.fetchall()))
        collection_ids_string = "'"+"','".join(collection_ids)+"'"
        # print(collection_ids_string)
        # Total weight of products in date range from collections
        cursor.execute(
            "SELECT SUM(weight) FROM app1_product WHERE collection_id IN ("+collection_ids_string+")")
        total_weight_in = cursor.fetchone()[0]
        # print(total_weight_in)

        # Pickups in date range
        cursor.execute('SELECT id FROM app1_pickup WHERE created_at BETWEEN %s AND %s AND larder_id = %s', [
                       start_datetime, end_datetime, larder_id])
        pickup_ids = re.findall(r'\d+', str(cursor.fetchall()))
        pickup_ids_string = "'"+"','".join(pickup_ids)+"'"
        # print(pickup_ids_string)
        # Total weight of products in date range from pickups
        cursor.execute(
            "SELECT SUM(weight) FROM app1_productout WHERE pickup_id IN ("+pickup_ids_string+")")
        total_weight_out = cursor.fetchone()[0]
        # print(total_weight_out)

        # Collections in date range into temp table collection_q
        cursor.execute('DROP TABLE IF EXISTS collection_q')
        cursor.execute(
            'CREATE TABLE collection_q(collection_id int, larder_id int, supplier_id int)')
        cursor.execute('INSERT INTO collection_q SELECT id,larder_id, supplier_id FROM app1_collection WHERE created_at BETWEEN %s AND %s AND larder_id = %s', [
                       start_datetime, end_datetime, larder_id])
        collections = re.findall(r'\d+', str(cursor.fetchall()))
        collections_string = "'"+"','".join(collections)+"'"
        # print("Collections: " + collections_string)

        # Suppliers weight of products in date range from collections in descending order
        cursor.execute("SELECT * FROM(SELECT  C.[collection_id], S.[name], S.[addressFirstLine], S.[type], SUM(P.[weight]) as TotalWeight FROM app1_supplier S, app1_product P, collection_q C WHERE  S.[id] = C.[supplier_id] AND P.[collection_id] = C.[collection_id] GROUP BY S.[name]) ORDER BY TotalWeight DESC")

        def namedtuplefetchall(cursor):
            "Return all rows from a cursor as a namedtuple"
            desc = cursor.description
            nt_result = namedtuple('Result', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]
        supplier_data = namedtuplefetchall(cursor)

        largest_supplier = f'{supplier_data[0].name} | {supplier_data[0].addressFirstLine}'
        # print(largest_supplier)

        # pickups in date range into temp table pickup_q
        cursor.execute('DROP TABLE IF EXISTS pickup_q')
        cursor.execute(
            'CREATE TABLE pickup_q(pickup_id int, larder_id int, member_id int)')
        cursor.execute('INSERT INTO pickup_q SELECT id,larder_id, member_id FROM app1_pickup WHERE created_at BETWEEN %s AND %s AND larder_id = %s', [
                       start_datetime, end_datetime, larder_id])
        pickups = re.findall(r'\d+', str(cursor.fetchall()))
        pickups_string = "'"+"','".join(pickups)+"'"
        # Members weight of products in date range from pickups in descending order
        cursor.execute("SELECT * FROM(SELECT  U.[pickup_id], M.[id], M.[firstName], M.[lastName], SUM(M.[noAdults] + M.[noChildren]) as numInHousehold ,SUM(P.[weight]) as TotalWeight FROM app1_member M, app1_productout P, pickup_q U WHERE  M.[id] = U.[member_id] AND P.[pickup_id] = U.[pickup_id] GROUP BY M.[firstName]) ORDER BY TotalWeight DESC")
        member_data = namedtuplefetchall(cursor)
        # print(member_data[0].name)

    volunteer_qs = Volunteer.objects.filter(
        created_at__range=[start_datetime, end_datetime], prefLarder_id=larder_id)
    supplier_qs = Supplier.objects.all()
    pickup_qs = Pickup.objects.all()
    member_qs = Member.objects.filter(
        created_at__range=[start_datetime, end_datetime], prefLarder_id=larder_id)
    larder_address = Larder.objects.get(name=larder).addressFirstLine
    larder_name = Larder.objects.get(name=larder).name
    context = {
        "larder_name": larder_name,
        "larder_address": larder_address,
        "total_weight_out": total_weight_out,
        "total_weight_in": total_weight_in,
        "net_weight": total_weight_in - total_weight_out,
        "new_volunteers": new_volunteers,
        "new_members": new_members,
        "start_date": start_date,
        "end_date": end_date,
        "member_qs": member_qs,
        "largest_supplier": largest_supplier,
        "supplier_qs": supplier_qs,
        "volunteer_qs": volunteer_qs,
        "supplier_data": supplier_data,
        "member_data": member_data,
    }

    HTML_String = render_to_string("larder_report.html", context=context)
    return HttpResponse(HTML_String)
