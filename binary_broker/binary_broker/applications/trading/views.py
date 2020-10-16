from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import json

from binary_broker.applications.accounts.models import *
from .serializers import *
from .auxiliary import *
from .models import *
from .forms import *

class AssetPartialUpdateView(GenericAPIView, UpdateModelMixin):

    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def patch(self, request, *args, **kwargs):
        print('calling asset partial update w/patch')
        instances = Asset.objects.all()
        serializer = AssetSerializer(instances, many=True)
        return Response(serializer.data)

class AssetListView(ListView):

    template_name = 'Asset/list.html'

    def get_queryset(self):
        return Asset.objects.all()

def get_profile_from_request(request):
    return request.user.profile

class AssetDetailView(DetailView):

    model = Asset
    template_name = 'asset/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        asset = kwargs['object']
        account = get_profile_from_request(self.request)
        context['price_plot'] = create_price_plot(asset, account)
        context['bet_form'] = PartialBetForm()
        return context

def create_bet(request, pk):
    print('creating bet')
    partial_form = PartialBetForm(request.POST)
    partial_errors = json.loads(partial_form.errors.as_json())
    if partial_form.is_valid():
        print('PARTIAL FORM VALID')
        # add 'direction', 'owner', 'Asset', 'is_real_account')
        bet_info = partial_form.clean()
        user = request.user
        asset = Asset.objects.get(pk=pk)
        bet_info['owner'] = user.profile
        bet_info['direction_up'] = dict([i[::-1]
            for i in settings.BET_DIRECTIONS]).get(request.POST['direction'])
        bet_info['asset'] = asset
        bet_info['is_real_account'] = user.profile.selected_account_type == \
            Profile.ACCOUNT_TYPES[1][0]
        print(bet_info)
        full_form = BetForm(bet_info)
        full_errors = json.loads(full_form.errors.as_json())
        if full_form.is_valid():
            print('FULL FORM VALID')
            bet = Bet.objects.create(**bet_info)
        else:
            print('FULL FORM INVALID')
            print(full_form.errors)
        print('BET CREATION DONE')
        return HttpResponse(json.dumps(full_errors, ensure_ascii=False))
    else:
        print('PARTIAL FORM INVALID')
        return HttpResponse(json.dumps(partial_errors, ensure_ascii=False))

def create_price_plot_response(request, pk):
    asset = Asset.objects.get(pk=pk)
    account = get_profile_from_request(request)
    return create_mp_price_plot_response(asset, account)

def create_price_plot(asset, account):
    return create_mp_price_plot(asset, account)

def create_mp_price_plot(asset, account):
    price_history = asset.get_last_records(
        datetime.timedelta(seconds=60))
    return create_mp_price_plot_figure(price_history, account, title=asset.name)

def create_mp_price_plot_response(asset, account):
    print('create mp price plot response')
    plot = create_mp_price_plot(asset, account)
    canvas = FigureCanvas(plot)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
