from collections import defaultdict
from adminside.models import Inventory, Staff
from django.utils.timezone import now

def expired_items(request):
    if not request.session.get("staff_id"):
        return {}

    try:
        staff_user = Staff.objects.get(staff_id=request.session["staff_id"])
    except Staff.DoesNotExist:
        return {}

    today = now().date()
    if staff_user.staff_role.lower() == "admin":
        items = Inventory.objects.filter(exp_date__lte=today).order_by('branch__branch_name', 'exp_date')
    else:
        items = Inventory.objects.filter(exp_date__lte=today, branch=staff_user.branch).order_by('exp_date')

    grouped = defaultdict(list)
    for item in items:
        branch_name = item.branch.branch_name if item.branch else "No Branch"
        grouped[branch_name].append(item)

    return {
        "expired_items_grouped": dict(grouped)
    }
