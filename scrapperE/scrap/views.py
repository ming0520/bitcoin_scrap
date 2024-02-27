from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
# from django.core.serializers import serialize
from django.utils.timezone import make_aware
from django.db import connections
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import PostRaw,CommentRaw,ErrorPost,BitstampData,ErrorLog,BitstampDataHour,BitstampDataMinute
from .serializers import PostRawSerializer,BitstampDataSerializer,BitstampDataHourSerializer,ErrorLogSerializer, BitstampDataMinuteSerializer


import praw
from datetime import datetime, timedelta
import pandas as pd

import json
import requests
import pytz

import logging
# Setting the basic configuration for logging, such as the level, the format and the file name
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='C:\\Other Project\\Ads\\Bitcoin Scraping\\views.log')

# Creating a logger object
logger = logging.getLogger()

def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {})

# def dashboard_d3js(request):
#     # dataset = BitstampDataHour.objects.all()[0:3]
#     # data = serializers.serialize('json', dataset, fields=('local_date', 'close'))
#     return render(request, 'dashboard_d3js.html')


def bitcoin_hourly_data(request):
    dataset = BitstampDataHour.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

def post_raw(request):
    dataset = PostRaw.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

# def bitcoin_hourly_data_close(request):
#     dataset = BitstampDataHour.objects.all()[0:3]
#     data = serializers.serialize('json', dataset, fields=('local_date', 'close'))
#     return JsonResponse(data, safe=False)

currency_pair = "btcusd"
# ohlc_url = f"https://www.bitstamp.net/api/v2/ticker/{currency_pair}/"
ohlc_url = f'https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/?step=3600&limit=1'
minute_url = "http://127.0.0.1:8000/scrap/api/bitstampminute/add"
hour_url = "http://127.0.0.1:8000/scrap/api/bitstamphour/add"
day_url = "http://127.0.0.1:8000/scrap/api/bitstamp/add"
error_log_url = "http://127.0.0.1:8000/scrap/api/error_log/add/"


def call_bitsamp_api(ohlc_url,api_endpoint,error_log_url):
    ohlc_data_dict = {}

    try:
        data = requests.get(ohlc_url)

        bitstamp_data = data.json()['data']

        ohlc_data = bitstamp_data['ohlc'][0]
        ohlc_data['unix'] = ohlc_data.pop('timestamp')
        ohlc_data['volume_btc'] = ohlc_data.pop('volume')
        # Convert the Unix timestamp to UTC time
        ohlc_data['date'] = datetime.utcfromtimestamp(int(ohlc_data['unix'])).strftime('%Y-%m-%dT%H:%M:%S')
        
        # PROD
        # ohlc_data['symbol'] = bitstamp_data['pair']

        # TEST
        ohlc_data['symbol'] = 'SCHEDULER_TEST'
        # ohlc_data['symbol'] = 'HUMAN_TEST'

        # Convert the timestamp to datetime and localize it to UTC
        dt = datetime.fromtimestamp(int(ohlc_data['unix']), tz=pytz.UTC)
        # Convert the datetime to Kuala Lumpur time
        kl_time = dt.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))
        ohlc_data['local_date'] = kl_time.strftime('%Y-%m-%dT%H:%M:%S')

        # Convert 'volume' and 'close' to float before multiplication
        ohlc_data['volume_usd'] = round(float(ohlc_data['volume_btc']) * float(ohlc_data['close']), 10)
        
        ohlc_json = json.dumps(ohlc_data)

        # Convert the string to a dictionary
        ohlc_data_dict = json.loads(ohlc_json)

    except Exception as e:
        print(e)
        error = {
            "error_message": e.message if hasattr(e, 'message') else str(e),
            "error_source": 'when calling bitstamp official api',
            "error_type": 'bitstamp api error',
            "error_content": data.to_dict() if hasattr(data, 'to_dict') else str(data)
        }
        requests.post(error_log_url, data=error)
        
    try:
        response = requests.post(api_endpoint, json=ohlc_data_dict)
        print('api_endpoint:',api_endpoint, 'response:',response.status_code, 'response:',response.text)
        logger.info(f'api_endpoint: {api_endpoint} status: {response.status_code} response: {response.text}')
        if response.status_code == 200:
            print('Data successfully added to the database')
            logger.info('Data successfully added to the database')
        else:

            error_data = {
                "error_source": 'Bitstamp API',
                "error_type": response.text,
                "error_content": api_endpoint,
                "error_message": "Calling bitstamp store api"
            }
            requests.post(error_log_url, json=error_data)
    except requests.exceptions.RequestException as e:
        error_data = {
        "error_source": 'Bitstamp API',
        "error_type": response.text,
        "error_content": api_endpoint,
        "error_message": e.message if hasattr(e, 'message') else str(e),
        }
        requests.post(error_log_url, json=error_data)
        print(e)

@api_view(['GET'])
def save_bitstamp_hourly(request):
    call_bitsamp_api(ohlc_url,hour_url,error_log_url)
    return HttpResponse("Triggered Bitstamp API hourly data")

@api_view(['GET'])
def save_bitstamp_daily(request):
    call_bitsamp_api(ohlc_url,day_url,error_log_url)
    return HttpResponse("Triggered Bitstamp API daily data")

@api_view(['GET'])
def save_bitstamp_minutely(request):
    call_bitsamp_api(ohlc_url,minute_url,error_log_url)
    return HttpResponse("Triggered Bitstamp API minutely data")
           

@api_view(['GET'])
def all_post(request):
    all_post = PostRaw.objects.all()
    serializer = PostRawSerializer(all_post, many=True)
    # data = serializers.serialize('json', all_post)
    # return JsonResponse(data, safe=False)

    # data = serialize('json', all_post, ensure_ascii=False)
    # return JsonResponse(data, safe=False)
    # all_post = {'name'  : 'all_post','age' : 25, 'city' : 'New York'}
    return Response(serializer.data)


@api_view(['GET'])
def get_post_by_id(request, post_id):
    try:
        post = PostRaw.objects.get(post_id=post_id)
        serializer = PostRawSerializer(post)
        return Response(serializer.data)
    except PostRaw.DoesNotExist:
        # return HttpResponse(status=404)
        logger.error(f'Post with post_id {post_id} not found', status=status.HTTP_404_NOT_FOUND)
        return Response({'error': f'Post with post_id {post_id} not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_post_by_status(request, status):
    try:
        # posts = PostRaw.objects.filter(status=status)
        posts = PostRaw.objects.filter(status=status)[:20]
        if posts:
            serializer = PostRawSerializer(posts, many=True)
            return Response(serializer.data)
        else:
            logger.error(f'No posts with status {status} found', status=status.HTTP_404_NOT_FOUND)
            return Response({'error': f'No posts with status {status} found'}, status=status.HTTP_404_NOT_FOUND)
    except PostRaw.DoesNotExist:
        logger.error(f'Post with status {status} not found', status=status.HTTP_404_NOT_FOUND)
        return Response({'error': f'Post with status {status} not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_error_log(request):
    serializer = ErrorLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    logger.error(f'Failed to save error to database', status=status.HTTP_400_BAD_REQUEST)
    errorLog = ErrorLog.objects.create(
        error_message=serializer.errors,
        error_type="Failed to save error to database",
        error_source="add_error_log",
        error_content =  request.data
    )
    errorLog.save()
    return Response(serializer.errors)

@api_view(['POST'])
def add_bitstamp(request):
    serializer = BitstampDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def add_bitstamphour(request):
    serializer = BitstampDataHourSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def add_bitstampminute(request):
    serializer = BitstampDataMinuteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

def scrap_today(request):
    reddit = praw.Reddit(client_id='mTF5k367VUFFmQ', client_secret='mjhD5xlOjtzDM8uovN9mzkhVOC2KbA', user_agent='User-Agent: Mozilla/5.0')
    top_btc_subreddit = ['CryptoCurrencyTrading','btc','BitcoinBeginners','Bitcoin']
    now = datetime.now()

    for sub in top_btc_subreddit:
        subreddit = reddit.subreddit(sub)
        # Get the current date and time
        
        for submission in subreddit.hot(limit=5): 
            print('Scrapping from:',sub)
            # Convert the submission's timestamp to a datetime object
            submission_time = datetime.fromtimestamp(submission.created_utc)
            print("Processing submission:", submission.title, "url:", submission.permalink, "created at:", submission_time, "score:", submission.score)

            # If the submission was posted today
            # if (submission_time.date() == now.date()) or (submission_time.date() != now.date()):
            if submission_time.date() == now.date():
                # Check if the post_id already exists in the database
                if not PostRaw.objects.filter(post_id=str(submission.id)).exists():
                    # Get the date and time of the submission
                    created_at = make_aware(submission_time)
                    try:
                        # Save the data to your PostRaw model
                        post = PostRaw.objects.create(
                            post_id=str(submission.id),
                            title=submission.title,
                            raw_text=submission.selftext,
                            created_at=created_at,
                            platform_source='Reddit',
                            post_url=submission.permalink,
                            author_name=submission.author.name if submission.author else "None",
                            author_id=str(submission.author.id) if submission.author else "None",
                            # added_at=datetime.now(), # This will be automatically added by the model
                            post_score=submission.score
                        )
                        post.save()
                    except Exception as e:
                    # Just print(e) is cleaner and more likely what you want,
                    # but if you insist on printing message specifically whenever possible...
                        errorPost = ErrorPost.objects.create(
                            post_id=str(submission.id),
                            error_message=e.message if hasattr(e, 'message') else e
                        )
                        errorPost.save()
                        if hasattr(e, 'message'):
                            print(e.message)
                        else:
                            print(e)
                else:
                    print("Post already exists in the database")
            else:
                print("Post was not created today")

    return HttpResponse("Hello, World!")

# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Bitstamp
# from .forms import BitstampForm

# def bitstamp_list(request):
#     bitstamps = Bitstamp.objects.all()
#     return render(request, 'bitstamp/bitstamp_list.html', {'bitstamps': bitstamps})

# def bitstamp_detail(request, pk):
#     bitstamp = get_object_or_404(Bitstamp, pk=pk)
#     return render(request, 'bitstamp/bitstamp_detail.html', {'bitstamp': bitstamp})

# def bitstamp_create(request):
#     if request.method == "POST":
#         form = BitstampForm(request.POST)
#         if form.is_valid():
#             bitstamp = form.save(commit=False)
#             bitstamp.save()
#             return redirect('bitstamp_detail', pk=bitstamp.pk)
#     else:
#         form = BitstampForm()
#     return render(request, 'bitstamp/bitstamp_form.html', {'form': form})

# def bitstamp_update(request, pk):
#     bitstamp = get_object_or_404(Bitstamp, pk=pk)
#     if request.method == "POST":
#         form = BitstampForm(request.POST, instance=bitstamp)
#         if form.is_valid():
#             bitstamp = form.save(commit=False)
#             bitstamp.save()
#             return redirect('bitstamp_detail', pk=bitstamp.pk)
#     else:
#         form = BitstampForm(instance=bitstamp)
#     return render(request, 'bitstamp/bitstamp_form.html', {'form': form})

# def bitstamp_delete(request, pk):
#     bitstamp = get_object_or_404(Bitstamp, pk=pk)
#     bitstamp.delete()
#     return redirect('bitstamp_list')
