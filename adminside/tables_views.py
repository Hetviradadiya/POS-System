from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib import messages
from adminside.models import*
from adminside.forms import*

def render_page(request, template, data=None):
    data=data or {}
    # Retrieve session key from URL and apply it
    session_key = request.GET.get("session_key")
    if session_key:
        try:
            session_data = Session.objects.get(session_key=session_key)  # Fetch session
            session_store = request.session.__class__(session_key)  # Load session store
            session_store.load()  # Load session data
            request.session.update(session_store)  # Apply session data to request.session
        except Session.DoesNotExist:
            print("Session not found, using default session.")

    # Debug session data
    # print(f"Current session data in render_page: {request.session.items()}")
    data.update({"template": template, "today_date": now().strftime("%Y-%m-%d"),"staff_username": request.session.get("staff_username", "Guest"),})
    return render(request, "adminside/base.html", data)


def tables(request):
    if request.method == "POST":
        # print("Form Data:", request.POST) 
        # table_number = request.POST.get("table_number")
        seats = request.POST.get("seats")
        status = "Vacant"  # Default status

        if not seats:  # Ensure seats is not empty
            # print("not seats selected.")
            messages.error(request, "Please select a table type before adding.")
            return redirect("adminside:tables")

        # Save to Database
        Table.objects.create(seats=seats, status=status)
        # print("Table added with seats:", seats)
        # Redirect back to the tables page to refresh the list
        return redirect("adminside:tables")
    tables = Table.objects.all()

    for table in tables:
        has_orders = Cart.objects.filter(table=table).exists()
        if has_orders:
            table.status = "Occupied"
        elif table.status != "Reserved":
            table.status = "Vacant"

    context = {
        "tables": tables,
    }
    return render_page(request, 'adminside/tables.html', context)
