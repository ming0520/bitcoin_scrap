from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
# from django.core.serializers import serialize
from django.utils.timezone import make_aware
from django.db import connections
from django.db.models import Count
from django.contrib.auth.decorators import login_required

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

@login_required    
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



# This function is used to call the Bitstamp API, process the data and post it to the specified endpoint.
# If any error occurs during the process, it is logged to the specified error log URL.
def call_bitsamp_api(ohlc_url,api_endpoint,error_log_url):
    ohlc_data_dict = {}

    try:
        # Fetch data from the Bitstamp API
        data = requests.get(ohlc_url)

        # Extract the relevant data
        bitstamp_data = data.json()['data']

        # Process the data
        ohlc_data = bitstamp_data['ohlc'][0]
        ohlc_data['unix'] = ohlc_data.pop('timestamp')
        ohlc_data['volume_btc'] = ohlc_data.pop('volume')

        # Convert the Unix timestamp to UTC time
        ohlc_data['date'] = datetime.utcfromtimestamp(int(ohlc_data['unix'])).strftime('%Y-%m-%dT%H:%M:%S')
        
        # Set the symbol for the data
        ohlc_data['symbol'] = 'SCHEDULER_TEST'

        # Convert the timestamp to datetime and localize it to UTC
        dt = datetime.fromtimestamp(int(ohlc_data['unix']), tz=pytz.UTC)

        # Convert the datetime to Kuala Lumpur time
        kl_time = dt.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))
        ohlc_data['local_date'] = kl_time.strftime('%Y-%m-%dT%H:%M:%S')

        # Calculate the volume in USD
        ohlc_data['volume_usd'] = round(float(ohlc_data['volume_btc']) * float(ohlc_data['close']), 10)
        
        # Convert the data to JSON
        ohlc_json = json.dumps(ohlc_data)

        # Convert the JSON to a dictionary
        ohlc_data_dict = json.loads(ohlc_json)

    except Exception as e:
        # Log any errors that occur when calling the Bitstamp API
        error = {
            "error_message": e.message if hasattr(e, 'message') else str(e),
            "error_source": 'when calling bitstamp official api',
            "error_type": 'bitstamp api error',
            "error_content": data.to_dict() if hasattr(data, 'to_dict') else str(data)
        }
        requests.post(error_log_url, data=error)
        
    try:
        # Post the processed data to the specified endpoint
        response = requests.post(api_endpoint, json=ohlc_data_dict)

        # Log the response
        if response.status_code == 200:
            print('Data successfully added to the database')
        else:
            # Log any errors that occur when posting the data
            error_data = {
                "error_source": 'Bitstamp API',
                "error_type": response.text,
                "error_content": api_endpoint,
                "error_message": "Calling bitstamp store api"
            }
            requests.post(error_log_url, json=error_data)
    except requests.exceptions.RequestException as e:
        # Log any exceptions that occur when posting the data
        error_data = {
        "error_source": 'Bitstamp API',
        "error_type": response.text,
        "error_content": api_endpoint,
        "error_message": e.message if hasattr(e, 'message') else str(e),
        }
        requests.post(error_log_url, json=error_data)
        print(e)

"""
Saves 5minutely,hourly,daily data from the Bitstamp API.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: A response indicating that the Bitstamp API minutely data has been triggered.
"""
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
    call_bitsamp_api(ohlc_url, minute_url, error_log_url)
    return HttpResponse("Triggered Bitstamp API minutely data")
      
           
"""
Retrieve all posts.

This function retrieves all posts from the database and returns them as a JSON response.

Parameters:
- request: The HTTP request object.

Returns:
- Response: A JSON response containing all the posts.

Example:
GET /all_post/
Response:
[
    {
            "id": 13,
            "post_id": "1ax2n22",
            "title": "SHA-256 Under the Hood",
            "raw_text": "",
            "created_at": "2024-02-22T17:46:47Z",
            "added_at": "2024-02-22T10:08:08.580246Z",
            "platform_source": "Reddit",
            "post_url": "/r/Bitcoin/comments/1ax2n22/sha256_under_the_hood/",
            "author_name": "pickeydotai",
            "author_id": "7kgjzha1s",
            "post_score": 1,
            "status": "PENDING"
        },
]
"""
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
    """
    Retrieve a post by its ID.

    Args:
        request (HttpRequest): The HTTP request object.
        post_id (int): The ID of the post to retrieve.

    Returns:
        Response: The serialized data of the retrieved post.

    Raises:
        PostRaw.DoesNotExist: If the post with the given ID does not exist.
    """
    try:
        post = PostRaw.objects.get(post_id=post_id)
        serializer = PostRawSerializer(post)
        return Response(serializer.data)
    except PostRaw.DoesNotExist:
        logger.error(f'Post with post_id {post_id} not found', status=status.HTTP_404_NOT_FOUND)
        return Response({'error': f'Post with post_id {post_id} not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_post_by_status(request, status):
    """
    Retrieve posts by status.

    Args:
        request (HttpRequest): The HTTP request object.
        status (str): The status of the posts to retrieve.

    Returns:
        Response: The HTTP response containing the serialized posts.

    Raises:
        PostRaw.DoesNotExist: If no posts with the given status are found.
    """
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
    """
    API view to add an error log to the database.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the serializer is valid, returns the serialized data with a response status of 200.
    - If the serializer is invalid, returns the serialized errors with a response status of 400.
    """
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
    """
    Add Bitstamp data to the database.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the serializer is valid, returns the serialized data.
    - If the serializer is invalid, returns the serializer errors.
    """
    serializer = BitstampDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def add_bitstamphour(request):
    """
    Add Bitstamp data for an hour.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Response: The HTTP response object containing the serialized data if valid, 
        or the errors if invalid.
    """
    serializer = BitstampDataHourSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def add_bitstampminute(request):
    """
    Add a new Bitstamp minute data entry.

    Parameters:
    - request: The HTTP request object containing the data to be serialized.

    Returns:
    - If the data is valid, returns the serialized data of the newly created entry.
    - If the data is invalid, returns the errors from the serializer.

    """
    serializer = BitstampDataMinuteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

def scrap_today(request):
    """
    Scrapes the top 100 hot submissions from specified Bitcoin-related subreddits and saves them to the database if they were posted today.

    Args:
        request: The HTTP request object.

    Returns:
        An HTTP response with the message "Hello, World!".
    """
    reddit = praw.Reddit(client_id='mTF5k367VUFFmQ', client_secret='mjhD5xlOjtzDM8uovN9mzkhVOC2KbA', user_agent='User-Agent: Mozilla/5.0')
    top_btc_subreddit = ['CryptoCurrencyTrading','btc','BitcoinBeginners','Bitcoin']
    now = datetime.now()

    for sub in top_btc_subreddit:
        subreddit = reddit.subreddit(sub)
        # Get the current date and time
        
        for submission in subreddit.hot(limit=100): 
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