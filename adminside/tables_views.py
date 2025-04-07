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
        seats = request.POST.get("seats")
        branch_id = request.POST.get("branch")

        print("branch_id")
        status = "Vacant"

        if not seats:
            messages.error(request, "Please select a table type before adding.")
            return redirect("adminside:tables")

        branch = Branch.objects.filter(branch_id=branch_id).first() if branch_id else None

        Table.objects.create(seats=seats, status=status, branch=branch)

        return redirect("adminside:tables")

    # GET: Filter by selected branch
    selected_branch = request.GET.get("branch_id")
    print("selected_branch",selected_branch)
    branches = Branch.objects.all()

    staff_role = request.session.get("staff_role")

    tables = []
    if staff_role == "manager":
        manager_branch_id = request.session.get("branch")
        if manager_branch_id:
            selected_branch = str(int(manager_branch_id))
            branches = Branch.objects.filter(branch_id=selected_branch)
            tables = Table.objects.filter(branch_id=selected_branch)
    elif selected_branch:
        try:
            selected_branch = str(int(selected_branch))  # ensure it's valid
            tables = Table.objects.filter(branch_id=selected_branch)
        except ValueError:
            selected_branch = None
            tables = []
    else:
        tables = []

    # Update statuses
    for table in tables:
        has_orders = Cart.objects.filter(table=table).exists()
        if has_orders:
            table.status = "Occupied"
        elif table.status != "Reserved":
            table.status = "Vacant"

    context = {
        "tables": tables,
        "branches": branches,
        "selected_branch": selected_branch,
    }

    return render_page(request, 'adminside/tables.html', context)