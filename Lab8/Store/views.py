from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import SellsForm, UserSignForm, StorageForm, ItemForm, SellerForm, SellerPlanForm, StoragePlanForm
from .models import Sells, Seller, Item, SellerPlan, StoragePlan, Storage


### functions
def sell_item(request):
    id_item = int(request.POST.get('item'))
    cnt = int(request.POST.get('cnt'))

    curr_item = Item.objects.get(id_item=id_item)
    curr_item.cnt -= cnt
    curr_item.save()


def return_item(curr_sell):
    curr_item = Item.objects.get(id_item=curr_sell.item.id_item)
    curr_item.cnt += curr_sell.cnt
    curr_item.save()


def seller_wrong_storage(request):
    return Seller.objects.get(id_seller=int(request.POST.get('seller'))).id_storage != int(request.POST.get('storage'))


def get_table(request):
    return Seller.objects.get(id_seller=int(request.POST.get('seller'))).id_storage != int(request.POST.get('storage'))


def table_template(request, Table, template_names, table_name, Form):
    table = Table.objects.all()
    context = dict()
    form = Form()

    attr_names = [field.name for field in Table._meta.fields]
    table_lines = []
    for line in table:
        table_lines.append("<tr>")
        for attr_name in attr_names:
            table_lines.append(f"<td>{getattr(line, attr_name)}</td>")
        table_lines.append("</tr>")

    form_lines = []
    for attr_name in attr_names[1:]:
        form_lines.append(form[attr_name])

    id_lines = [f'<select name="{attr_names[0]}">']
    for line in table:
        id_lines.append(f'<option value="{getattr(line, attr_names[0])}">{getattr(line, attr_names[0])}</option>')
    id_lines.append('</select>')

    form.use_required_attribute = False
    context['table'] = table
    context['template_names'] = template_names
    context['table_lines'] = table_lines
    context['form_lines'] = form_lines
    context['id_lines'] = id_lines
    context['table_name'] = table_name
    return context


### classes

class RegisterView(FormView):
    form_class = UserSignForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


### pages

def index(request):
    return render(request, 'index.html')


@login_required
def sells_table(request):
    template_names = ["Sell ID",
                      "Storage",
                      "Item",
                      "Amount",
                      "Seller",
                      "Date"]
    table_name = "Sells"
    Form = SellsForm
    context = table_template(request, Sells, template_names, table_name, Form)
    return render(request, 'table.html', context)

@login_required
def storage_table(request):
    Table = Storage
    template_names = [field.name for field in Table._meta.fields]
    table_name = "Storage"
    Form = StorageForm
    context = table_template(request, Table, template_names, table_name, Form)
    return render(request, 'table.html', context)

@login_required
def item_table(request):
    Table = Item
    template_names = [field.name for field in Table._meta.fields]

    table_name = "Item"
    Form = ItemForm
    context = table_template(request, Table, template_names, table_name, Form)
    return render(request, 'table.html', context)

@login_required
def seller_table(request):
    Table = Seller
    template_names = [field.name for field in Table._meta.fields]

    table_name = "Seller"
    Form = SellerForm
    context = table_template(request, Table, template_names, table_name, Form)
    return render(request, 'table.html', context)

@login_required
def seller_plan_table(request):
    Table = SellerPlan
    template_names = [field.name for field in Table._meta.fields]

    table_name = "Seller Plan"
    Form = SellerPlanForm
    context = table_template(request, Table, template_names, table_name, Form)
    return render(request, 'table.html', context)

@login_required
def storage_plan_table(request):
    Table = StoragePlan
    template_names = [field.name for field in Table._meta.fields]

    table_name = "Storage Plan"
    Form = StoragePlanForm
    context = table_template(request, Table, template_names, table_name, Form)
    return render(request, 'table.html', context)


def submit(request):
    previous_page = str(request.META.get('HTTP_REFERER', None))
    curr_table = previous_page.split("/")[-2]
    Form = None
    match (curr_table):
        case "sells_table":
            Form = SellsForm
        case "item_table":
            Form = ItemForm
        case "storage_table":
            Form = StorageForm
        case "seller_table":
            Form = SellerForm
        case "seller_plan_table":
            Form = SellerPlanForm
        case "storage_plan_table":
            Form = StoragePlanForm

    if request.method == 'POST':
        id_str = list([field.name for field in Form._meta.model._meta.fields])[0]
        id_sell = request.POST.get(id_str)
        action = request.POST.get('action')

        if action == 'add':
            post_form = Form(request.POST)
            if post_form.is_valid():
                if 0:  #seller_wrong_storage(request):
                    name = self.objects.get(id_seller=int(request.POST.get("seller")))
                    messages.error(request, f"{name.second_name} {name.first_name} doesnt work at that storage")
                else:
                    post_form.save()

                    if curr_table == "sells_table":
                        sell_item(request)

                    messages.success(request, 'Sell was added successfully')
            else:
                messages.error(request, 'Something went wrong. Check your input')
        elif action == 'delete':
            try:
                sell = get_object_or_404(Form.Meta.model, pk=id_sell)

                if curr_table == "sells_table":
                    return_item(sell)

                sell.delete()

                messages.success(request, 'Sell was deleted successfully')
            except:
                messages.error(request, 'Sell does not exist')

        elif action == 'update':
            try:
                sell = get_object_or_404(Form.Meta.model, pk=id_sell)
                update_form = Form(request.POST, instance=sell)
                if update_form.is_valid():
                    if 0: #seller_wrong_storage(request):
                        name = Seller.objects.get(id_seller=int(request.POST.get("seller")))
                        messages.error(request, f"{name.second_name} {name.first_name} doesnt work at that storage")
                    else:
                        if curr_table == "sells_table":
                            return_item(sell)
                        update_form.save()
                        if curr_table == "sells_table":
                            sell_item(request)

                        messages.success(request, 'Sell was updated successfully')
                else:
                    messages.error(request, 'Something went wrong. Check your input')
            except:
                messages.error(request, 'Sell does not exist')
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect('index')
