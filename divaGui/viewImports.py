import random
import requests
import json
import pprint
import base64

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from time import sleep
from uploader.models import UploadForm,Upload
from links.links import *






