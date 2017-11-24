import datetime
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import (login as auth_login, logout as auth_logout, authenticate)
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count

from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    View
)
from django.forms import ModelForm
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Order, Inventory
from .forms import RegistrationForm, EditProfileForm, OrderForm, OrderEditForm, InventoryForm
from settings import base

# third party apps
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


class HistoryView(ListView):
    model = Order
    context_object_name = 'user_order'
    template_name = 'ordering/order_history.html'
    ordering = ['-date']
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(ordered_by=self.request.user)


# FM app views
class DetailView(ListView):
    model = Order  # shorthand for setting queryset = models.Order.objects.all()
    template_name = 'ordering/detail.html'
    context_object_name = "all_order"
    paginate_by = 10

    def get_context_date(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        queryset = Order.objects.all()

        if self.request.GET.get('q'):
            queryset = queryset.filter(last_name=self.request.GET.get('q'))
        return queryset


class OrderCreateView(SuccessMessageMixin, AjaxCreateView):
    form_class = OrderForm
    model = Order
    success_message = "Successfully added an order."

    def form_valid(self, form):
        order = form.save(commit=False)
        order.ordered_by = self.request.user
        order.save()
        return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(SuccessMessageMixin, AjaxUpdateView):
    form_class = OrderEditForm
    model = Order
    success_message = "Successfully updated this order."
    pk_url_kwarg = 'order_id'


class OrderDeleteView(AjaxDeleteView):
    model = Order
    success_message = "Successfully updated this order."
    pk_url_kwarg = 'order_id'


class OrderSuccess(TemplateView):
    template_name = 'ordering/order_success.html'


class InventoryMenu(ListView):
    model = Inventory
    template_name = 'inventory/inventory_sample.html'
    context_object_name = "all_inventorys"
    paginate_by = 10

    def get_context_date(self, **kwargs):
        context = super(InventoryMenu, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        queryset = Inventory.objects.all()

        if self.request.GET.get('q'):
            queryset = queryset.filter(product=self.request.GET.get('q'))
        return queryset


class InventoryCreateView(SuccessMessageMixin, AjaxCreateView):
    form_class = InventoryForm
    success_message = "Successfully added an item to the inventory"


class InventoryDeleteView(AjaxDeleteView):
    model = Inventory
    pk_url_kwarg = 'inventory_id'


class InventoryUpdateView(SuccessMessageMixin, AjaxUpdateView):
    form_class = InventoryForm
    model = Inventory
    success_message = "Successfully updated this product."
    pk_url_kwarg = 'inventory_id'
# FM app views ends here


class LoginView(View):
    template_name = 'user_account/login_user.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.method == 'POST':
            _username = request.POST['username']
            _password = request.POST['password']
            user = authenticate(username=_username, password=_password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    user.last_login = datetime.datetime.now()
                    user.save(update_fields=['last_login'])
                    return redirect(reverse_lazy('ordering:home'))
                else:
                    messages.warning(request, 'Your account is not activated.')
            else:
                messages.error(request, 'Username or password are invalid.')
        return render(request, self.template_name)


class LogoutView(View):

    def get(self, request):
        auth_logout(request)
        messages.success(request, 'Your account has been logout successfully.')
        return redirect(reverse_lazy('ordering:login'))


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['date', 'product', 'stock_in', 'stock_out', 'balance', 'particulars']


def inventory_detail(request, inventory_id):
    inventory = get_object_or_404(Inventory, pk=inventory_id)
    context = {
        "inventory": inventory,
        }
    return render(request, "inventory/inventory_detail.html", context)


def home(request):
    return render(request, 'ordering/index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'user_account/register_success.html')
        else:
            return render(request, 'user_account/register.html', {'form': form})
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'user_account/register.html', args)


def register_success(request):
    return render(request, 'ordering:register_success')


def view_profile(request):
    args = {'user': request.user}
    return render(request, 'user_account/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('ordering:view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'user_account/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse_lazy('ordering:view_profile'))
        else:
            return redirect(reverse_lazy('ordering:change_password'))

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'user_account/change_password.html', args)
