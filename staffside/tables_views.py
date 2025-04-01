from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from adminside.models import*
from adminside.forms import*

def render_page(request, template, data=None):
    data=data or {}
    session_key = request.GET.get("session_key")
    if session_key:
        try:
            session_data = Session.objects.get(session_key=session_key)  # Fetch session
            session_store = request.session.__class__(session_key)  # Load session store
            session_store.load()  # Load session data
            request.session.update(session_store)  # Apply session data to request.session
        except Session.DoesNotExist:
            print("Session not found, using default session.")
    data.update({"template": template, "today_date": now().strftime("%Y-%m-%d"),"staff_username": request.session.get("staff_username", "Guest"),})
    return render(request, "staffside/base.html", data)

def tables(request):
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
    return render_page(request, 'staffside/tables.html', context)
