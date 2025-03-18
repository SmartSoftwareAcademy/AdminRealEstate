from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import *
from .models import *

# Property Owner views
class PropertyOwnerList(View):
    def get(self, request):
        owners = PropertyOwner.objects.all()
        return render(request, 'owners/owner_list.html', {'owners': owners})

class PropertyOwnerDetail(View):
    def get(self, request, pk):
        owner = get_object_or_404(PropertyOwner, pk=pk)
        return render(request, 'owners/owner_detail.html', {'owner': owner})

# Agent views
class AgentList(View):
    def get(self, request):
        agents = Agent.objects.all()
        return render(request, 'core/agents.html', {'agents': agents})

class AgentDetail(View):
    def get(self, request, pk):
        agent = get_object_or_404(Agent, pk=pk)
        return render(request, 'core/agent_detail.html', {'agent': agent})
