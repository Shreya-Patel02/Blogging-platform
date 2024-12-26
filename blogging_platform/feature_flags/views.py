from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from fastapi import Response
from rest_framework.views import APIView
from feature_flags.models import FeatureFlags
from users.permissions import IsOwner, IsAdmin, IsMember

class toggle_feature_flags(APIView):
    permission_classes = [IsOwner]  # Use IsOwner to allow only the owner to toggle flags

    def get(self, request):
        flags = FeatureFlags.objects.first()  # Get the feature flags object
        if not flags:
            # Create a new FeatureFlags object if none exists
            flags = FeatureFlags.objects.create(
                llm_article_generation=False, 
                llm_tags_generation=False
            )
        return render(request, 'feature_flags/feature_flags.html', {'flags': flags})

    def post(self, request):
        flags = FeatureFlags.objects.first()  # Get the feature flags object
        if not flags:
            # Create a new FeatureFlags object if none exists
            flags = FeatureFlags.objects.create(
                llm_article_generation=False, 
                llm_tags_generation=False
            )
        llm_article_generation = request.POST.get('llm_article_generation')
        llm_tags_generation = request.POST.get('llm_tags_generation')

        # Convert 'on'/'off' to True/False if necessary
        llm_article_generation = llm_article_generation == 'on'
        llm_tags_generation = llm_tags_generation == 'on'
        # Update the flags
        flags.llm_article_generation = llm_article_generation
        flags.llm_tags_generation = llm_tags_generation
        flags.save()
        return redirect('/')
    
    


