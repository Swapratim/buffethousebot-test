#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os
import sys
import psycopg2
#import urlparse
import emoji

from flask import Flask
from flask import request, render_template
from flask import make_response


# Flask should start in global layout
context = Flask(__name__)
# Facbook Access Token
ACCESS_TOKEN = "EAAEvanZCLUMcBAIZC2DXdZBVjmV7FtLsE1L0Tz1avpMqWtOq39Mlah6LgYbVTXCAjnlRU2kX8yExz9bnS8Muikt7sFA9aW9OcZB7uZC6pIPZAgZCmQqKsD3kPeTKpZBMorxLrGenFWxrXZAENWoJFF65ye25gVrmjN8fbplmo2jkqxQZDZD"
#ACCESS_TOKEN = "EAAWYbylWZA6wBADhibpOkrvZCMRNItJo0xDdjTkyCUdbhuo15q9pM0H16itMfwDcboCcPiJYUGzKar2Kgkvjr9aCfdbDvOGZAdItQsc7uJI47VedUFvDF0xyhoRXhxXY3yE8JpqyjDrLrZAI2p08ur9EZCZB7AMO4COik6i0nMVsojXUcq4Qsj"

#************************************************************************************#
#                                                                                    #
#    All Webhook requests lands within the method --webhook                          #
#                                                                                    #
#************************************************************************************#
# Webhook requests are coming to this method
@context.route('/webhook', methods=['POST'])
def webhook():
    reqContext = request.get_json(silent=True, force=True)
    print ("Within webhook method...!!!")
    #print (json.dumps(reqContext, indent=4))
    #print ("****************")
    #print (reqContext.get("result").get("action"))
    #print ("****************")
    if reqContext.get("result").get("action") == "input.welcome":
       return welcome()
    elif reqContext.get("result").get("action") == "danish.default.menu":
       return danishDefaultMenu(reqContext)
    elif reqContext.get("result").get("action") == "english.default.menu":
       return englishDefaultMenu(reqContext)
    elif reqContext.get("result").get("action") == "dan.Default.Main.Menu":  
       return danishDefaultMainMenu(reqContext)
    elif reqContext.get("result").get("action") == "eng.Default.Main.Menu": 
       return englishDefaultMainMenu(reqContext)
    elif reqContext.get("result").get("action") == "danish.Menu.Criteria.Menu":
       return danishMenuCriteriaMenu(reqContext)
    elif reqContext.get("result").get("action") == "english.Menu.Criteria.Menu":
       return englishMenuCriteriaMenu(reqContext)
    elif reqContext.get("result").get("action") == "danish.Menu.Criteria.Menu.Buffet":
       return danishMenuCriteriaMenuBuffet(reqContext)
    elif reqContext.get("result").get("action") == "english.Menu.Criteria.Menu.Buffet":
       return englishMenuCriteriaMenuBuffet(reqContext)
    elif reqContext.get("result").get("action") == "dan.Menu.Criteria.Menu.Items":
       return danMenuCriteriaMenuItems(reqContext)
    elif reqContext.get("result").get("action") == "eng.Menu.Criteria.Menu.Items":
       return engMenuCriteriaMenuItems(reqContext)
    elif reqContext.get("result").get("action") == "dan.Menu.Criteria.Menu.Items.Starter":
       return danMenuCriteriaMenuItemsStarter(reqContext)
    elif reqContext.get("result").get("action") == "eng.Menu.Criteria.Menu.Items.Starter":
       return engMenuCriteriaMenuItemsStarter(reqContext)
    elif reqContext.get("result").get("action") == "dan.Menu.Criteria.Menu.Items.MainDish":
       return danMenuCriteriaMenuItemsMainDish(reqContext)
    elif reqContext.get("result").get("action") == "eng.Menu.Criteria.Menu.Items.MainDish":
       return engMenuCriteriaMenuItemsMainDish(reqContext)
    elif reqContext.get("result").get("action") == "dan.Menu.Criteria.Menu.Items.Dessert":
       return danMenuCriteriaMenuItemsDessert(reqContext)
    elif reqContext.get("result").get("action") == "eng.Menu.Criteria.Menu.Items.Dessert":
       return engMenuCriteriaMenuItemsDessert(reqContext)
    elif reqContext.get("result").get("action") == "dan.Menu.Criteria.Special.Offer":
       return danMenuCriteriaMenuItemsSpecialMenu(reqContext)
    elif reqContext.get("result").get("action") == "eng.Menu.Criteria.Special.Offer":
       return engMenuCriteriaMenuItemsSpecialMenu(reqContext)
    elif reqContext.get("result").get("action") == "dan.default.menu.take.away":
       return danDefaultMenuTakeAway(reqContext)
    elif reqContext.get("result").get("action") == "eng.default.menu.take.away":
       return engDefaultMenuTakeAway(reqContext)
    elif reqContext.get("result").get("action") == "dan.default.menu.order.booking":
       return danDefaultMenuOrderBooking(reqContext)
    elif reqContext.get("result").get("action") == "eng.default.menu.order.booking": 
       return engDefaultMenuOrderBooking(reqContext)
    elif reqContext.get("result").get("action") == "dan.default.menu.opening.hours":
       return danDefaultMenuOpeningHours(reqContext)
    elif reqContext.get("result").get("action") == "eng.default.menu.opening.hours":
       return engDefaultMenuOpeningHours(reqContext)
    elif reqContext.get("result").get("action") == "dan.default.menu.contact.us": 
       return danDefaultMenuContactUs(reqContext)
    elif reqContext.get("result").get("action") == "eng.default.menu.contact.us": 
       return engDefaultMenuContactUs(reqContext)
    else:
       print("Good Bye")

 
#************************************************************************************#
#                                                                                    #
#   This method is to get the Facebook User Deatails via graph.facebook.com/v2.6     #
#                                                                                    #
#************************************************************************************#
user_name = ""
def welcome():
    print ("within welcome method")
    dataload = request.json
    id = dataload.get('originalRequest').get('data').get('sender').get('id')
    print ("id :" + id)
    fb_info = "https://graph.facebook.com/v2.6/" + id + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + ACCESS_TOKEN
    print (fb_info)
    result = urllib.request.urlopen(fb_info).read()
    #print (result)
    data = json.loads(result)
    first_name = data.get('first_name')
    print (first_name)
    user_name = data.get('first_name')
    speech = "Hi " + first_name + "! Welcome to Buffet House Restaurant" + emoji.emojize(':smiley:', use_aliases=True)
    res = {
          "speech": speech,
          "displayText": speech,
           "data" : {
              "facebook" : [
                   {
                    "sender_action": "typing_on"
                  },
                  {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Hi " + first_name + "! Welcome to Buffet House Restaurant" + emoji.emojize(':pray:', use_aliases=True),
                                   "image_url" : "http://gdurl.com/OelL",
                                 } 
                           ]
                       } 
                   }
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "Buffet House serves the best traditional Indian food in Aarhus."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "I'm the chatbot at your service."
                },
                {
                  "text": "Please select your language",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Danish",
                  "payload": "Danish",
                  "image_url": "http://hoster2.onlinebadgemaker.com/902ff56c336ac7f23146c70ed95d568d50c88192978f9.png"
                 },
                 {
                  "content_type": "text",
                  "title": "English",
                  "payload": "English",
                  "image_url": "https://cdn2.iconfinder.com/data/icons/world-flags-1-1/100/Britain-512.png"
                 }
                 ]
                }
               ]
              }
            };
    print (res)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print (r)
    return r

def reply(user_id, msg):
    print ("Within REPLY method")
    print ("user_id" + user_id)
    print ("msg" + msg)
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    print ("Data.........")
    print (data)
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

#************************************************************************************#
#                                                                                    #
#                English Default Menu                                                #
#                                                                                    #
#************************************************************************************#
def englishDefaultMenu(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                "text": "Thanks for choosing English and welcome again."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"http://gdurl.com/y0fi"
                     }
                 }
               },
                {
                  "text": "How can I help you?",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Menu",
                  "payload": "Menu",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Take Away",
                  "payload": "Take Away",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/66559-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Order Booking",
                  "payload": "Order Booking",
                  "image_url": "http://is5.mzstatic.com/image/thumb/Purple18/v4/77/13/96/771396f0-8059-c536-d17c-1806d9e22931/source/1200x630bb.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Opening Hours",
                  "payload": "Opening Hours",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
                 },
                 {
                  "content_type": "text",
                  "title": "Contact Us",
                  "payload": "Contact Us",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                 ]
                }
              ]
            }  
           };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                Main Menu - Quick Reply Options Only                                #
#                                                                                    #
#************************************************************************************#
def englishDefaultMainMenu(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                  "text": "Please select the below options:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Menu",
                  "payload": "Menu",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Take Away",
                  "payload": "Take Away",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/66559-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Order Booking",
                  "payload": "Order Booking",
                  "image_url": "http://is5.mzstatic.com/image/thumb/Purple18/v4/77/13/96/771396f0-8059-c536-d17c-1806d9e22931/source/1200x630bb.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Opening Hours",
                  "payload": "Opening Hours",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
                 },
                 {
                  "content_type": "text",
                  "title": "Contact Us",
                  "payload": "Contact Us",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                 ]
                }
              ]
            }  
           };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                MENU ITEMS = Buffet + Items + Special                               #
#                                                                                    #
#************************************************************************************#
def englishMenuCriteriaMenu(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Buffet House Menu",
                                   "image_url" : "http://gdurl.com/xdw5",
                                   "subtitle" : "Best in town dishes, only for you.",
                                   "buttons": [{
                                        "type": "postback",
                                        "title": "Buffet",
                                        "payload":"Buffet"
                                    },
                                    {
                                        "type": "postback",
                                        "title": "Menu Items",
                                        "payload": "Menu Items"
                                    },
                                    {
                                        "type": "postback",
                                        "title": "Special Offers",
                                        "payload": "Special Offers"
                                    }]
                                 }
                           ]
                       } 
                   }
                },
        {
      "text": "To view other options, please click below options:",
      "quick_replies": [
        {
          "content_type": "text",
          "title": "Home",
          "payload": "Home",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        },
        {
          "content_type": "text",
          "title": "Opening Hours",
          "payload": "Opening Hours",
          "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
          "content_type": "text",
          "title": "Contact Us",
          "payload": "Contact Us",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/66559-200.png"
        },
        {
          "content_type": "text",
          "title": "Start Over",
          "payload": "Start Over",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/72551-200.png"
        }
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#                            BUFFET                                                  #
#                                                                                    #
#************************************************************************************#
def englishMenuCriteriaMenuBuffet (reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Events",
            "displayText": "Events",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"http://gdurl.com/RyLb"
                     }
                 }
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Do not miss the great Indian delicious buffet!"
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Buffet is available everyday from 17:00-21:00 only at 99,- "
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "For children under 10 year, the buffet price is 59.- only"
               },
               
        {
      "text": "To view other options, please click below options:",
      "quick_replies": [
        {
         "content_type": "text",
         "title": "Menu",
         "payload": "Menu",
         "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
          "content_type": "text",
          "title": "Home",
          "payload": "Home",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        },
        {
         "content_type": "text",
         "title": "Start Over",
         "payload": "Start Over",
         "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/72551-200.png"
        }
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#                            ITEMS                                                   #
#                                                                                    #
#************************************************************************************#
def engMenuCriteriaMenuItems(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Taste the best - enjoy the variety  of dishes selected",
            "displayText": "Taste the best - enjoy the variety  of dishes selected",
            "data" : {
            "facebook" : [
                {
                   "sender_action": "typing_on"
                },
                {
                   "text": "Taste the best - enjoy the variety  of dishes selected",
                   "quick_replies": [
                {
                     "content_type": "text",
                     "title": "Starter",
                     "payload": "Starter",
                     "image_url": "https://cdn1.iconfinder.com/data/icons/food-drinks-set-2/96/Soup-512.png"
                },
                {
                     "content_type": "text",
                     "title": "Main Course",
                     "payload": "Main Course",
                     "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/1394544-200.png"
                },
                {
                     "content_type": "text",
                     "title": "Dessert",
                     "payload": "Dessert",
                     "image_url": "https://image.flaticon.com/icons/png/512/53/53628.png"
                },
                {
                     "content_type": "text",
                     "title": "Menu",
                     "payload": "Menu",
                     "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                },
                {
                     "content_type": "text",
                     "title": "Home",
                     "payload": "Home",
                     "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
                },
             ]
         }
      ]
    } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            STARTER                                                 #
#                                                                                    #
#************************************************************************************#
def engMenuCriteriaMenuItemsStarter(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Poppadom",
                                   "image_url" : "http://gdurl.com/5HcY",
                                   "subtitle" : "Indian snack speciality \nAvailable only at 39,-",
                                 },
                                 {
                                   "title" : "Chapli Kebab",
                                   "image_url" : "http://gdurl.com/p1Am",
                                   "subtitle" : "Pashtun-style minced kebab, originated from Peshawar \nAvailable only at 65,-",
                                 },
                                 {
                                   "title" : "Samosa",
                                   "image_url" : "http://gdurl.com/8qBs",
                                   "subtitle" : "Originated in Middle East back at 10th century \nAvailable only at 49,-",
                                 },
                                 {
                                   "title" : "Salad",
                                   "image_url" : "http://gdurl.com/n6Gl",
                                   "subtitle" : "An ancient Greek & Roman delicacy \nAvailable only at 29,-",
                                 },
                             ]
                       } 
                   }
                },
               
        {
      "text": "Please select any option below:",
      "quick_replies": [
        {
         "content_type": "text",
         "title": "Main Course",
         "payload": "Main Course",
         "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/1394544-200.png"
        },
        {
         "content_type": "text",
         "title": "Dessert",
         "payload": "Dessert",
         "image_url": "https://image.flaticon.com/icons/png/512/53/53628.png"
        },
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "Menu",
          "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
           "content_type": "text",
           "title": "Home",
           "payload": "Home",
           "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        },
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            MAIN DISH                                               #
#                                                                                    #
#************************************************************************************#
def engMenuCriteriaMenuItemsMainDish(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Nan/Garlic Nan",
                                   "image_url" : "http://gdurl.com/swcc",
                                   "subtitle" : "Fresh baked Nan from Tandoor oven \nAvailable only at 19 & 23,-",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Curry",
                                   "image_url" : "http://gdurl.com/76uW",
                                   "subtitle" : "Curry is a world famous dish across centuries \nAvailable only at 99, 109 & 119,-",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Korma",
                                   "image_url" : "http://gdurl.com/TQ2f",
                                   "subtitle" : "A Moghul dish of Indian origin from 16th century \nAvailable only at 85, 95 & 99,-",
                                 },
                                 {
                                   "title" : "Butter Chicken/Beef/Lamb",
                                   "image_url" : "http://gdurl.com/orET",
                                   "subtitle" : "Taste the century old passion for food-lovers \nAvailable only at 79, 99 & 109,-",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Roganjosh",
                                   "image_url" : "http://gdurl.com/RRTP",
                                   "subtitle" : "An Indian Moghul dish, influenced by Persian cuisine \nAvailable only at 89,-",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Kashmiri",
                                   "image_url" : "http://gdurl.com/chrv",
                                   "subtitle" : "Kasmiri cuisines always serve your taste bud \nAvailable only at 79, 89,-",
                                 },
                                 {
                                   "title" : "Palak Paneer",
                                   "image_url" : "http://gdurl.com/jFhH",
                                   "subtitle" : "A vegetarian dish from the Indian Subcontinent \nAvailable only at 79,-",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Sag",
                                   "image_url" : "http://gdurl.com/hKV1",
                                   "subtitle" : "A speciality you must try here \nAvailable only at 75, 79 & 109,-",
                                }
                        ]
                 } 
             }
        },
        {
      "text": "Please select any option below:",
      "quick_replies": [
        {
         "content_type": "text",
         "title": "Starter",
         "payload": "Starter",
         "image_url": "https://cdn1.iconfinder.com/data/icons/food-drinks-set-2/96/Soup-512.png"
        },
        {
         "content_type": "text",
         "title": "Dessert",
         "payload": "Dessert",
         "image_url": "https://image.flaticon.com/icons/png/512/53/53628.png"
        },
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "Menu",
          "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
          "content_type": "text",
          "title": "Home",
          "payload": "Home",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        }
       ]
     }
    ]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            DESSERT                                                 #
#                                                                                    #
#************************************************************************************#
def engMenuCriteriaMenuItemsDessert(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Vanilla Milkshake",
                                   "image_url" : "http://gdurl.com/V74H",
                                   "subtitle" : "Available only at 39,-",
                                 },
                                 {
                                   "title" : "Pistacie Milkshake",
                                   "image_url" : "http://gdurl.com/JjAF",
                                   "subtitle" : "Available only at 39,-",
                                 },
                                 {
                                   "title" : "Strawberry Milkshake",
                                   "image_url" : "http://gdurl.com/rU7E",
                                   "subtitle" : "Available only at 39,-",
                                 },
                                 {
                                   "title" : "Chocolate Milkshake",
                                   "image_url" : "http://gdurl.com/sA7I",
                                   "subtitle" : "Available only at 39,-",
                                 },
                                 {
                                   "title" : "Mango Lasse Yoghurt",
                                   "image_url" : "http://gdurl.com/kslO",
                                   "subtitle" : "Available only at 39,-",
                                 },
                                 {
                                   "title" : "0,5L Sodawater",
                                   "image_url" : "http://gdurl.com/zKOf",
                                   "subtitle" : "Available only at 25,-",
                                 },
                                 {
                                   "title" : "1,5L Sodavand",
                                   "image_url" : "http://gdurl.com/hH4c",
                                   "subtitle" : "Available only at 35,-",
                                 },
                                 {
                                   "title" : "Cold Water",
                                   "image_url" : "http://gdurl.com/Xs_K",
                                   "subtitle" : "Available only at 25,-",
                                 }
                             ]
                       } 
                   }
                },
               
        {
      "text": "Please select any option below:",
      "quick_replies": [
        {
         "content_type": "text",
         "title": "Starter",
         "payload": "Starter",
         "image_url": "https://cdn1.iconfinder.com/data/icons/food-drinks-set-2/96/Soup-512.png"
        },
        {
         "content_type": "text",
         "title": "Main Course",
         "payload": "Main Course",
         "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/1394544-200.png"
        },
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "Menu",
          "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
          "content_type": "text",
          "title": "Home",
          "payload": "Home",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        }
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            SPECIAL                                                 #
#                                                                                    #
#************************************************************************************#
def engMenuCriteriaMenuItemsSpecialMenu(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Sabzi Biriyani",
                                   "image_url" : "http://gdurl.com/QpGk",
                                   "subtitle" : "Available only at 119,-",
                                 },
                                 {
                                   "title" : "Chicken Biriyani",
                                   "image_url" : "http://gdurl.com/pRyi",
                                   "subtitle" : "Available only at 119,-",
                                 },
                                 {
                                   "title" : "Chicken Tikka Biriyani",
                                   "image_url" : "http://gdurl.com/RH5I",
                                   "subtitle" : "Available only at 119,-",
                                 },
                                 {
                                   "title" : "Lamb Biriyani",
                                   "image_url" : "http://gdurl.com/89Of",
                                   "subtitle" : "Available only at 139,-",
                                 },
                                 {
                                   "title" : "Beef Biriyani",
                                   "image_url" : "http://gdurl.com/dHh8",
                                   "subtitle" : "Available only at 119,-",
                                 },
                                 {
                                   "title" : "Luxury Biriyani",
                                   "image_url" : "http://gdurl.com/EUAwK",
                                   "subtitle" : "Available only at 139,-",
                                 }
                             ]
                       } 
                   }
                },
               
        {
      "text": "Please select any option below:",
      "quick_replies": [
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "Menu",
          "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
          "content_type": "text",
          "title": "Home",
          "payload": "Home",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        },
        {
          "content_type": "text",
          "title": "Start Over",
          "payload": "Start Over",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/72551-200.png"
        }
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            TAKE AWAY                                               #
#                                                                                    #
#************************************************************************************#
def engDefaultMenuTakeAway(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "People love to take away our food to enjoy at home"
               },
               {
                "text": "That’s why we have created special packages for take away."
               },
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"http://gdurl.com/HNzO"
                     }
                 }
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "We also take wholesale order for parties or gathering. We deliver food at your doorstep just in time nearby Aarhus."
               },
               {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "M1-Butter Chicken & Sag Allo",
                                   "image_url" : "http://gdurl.com/ZuLh",
                                   "subtitle" : "Available only at 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M2-Lamb Korma & Chicken Curry",
                                   "image_url" : "http://gdurl.com/x77y",
                                   "subtitle" : "Available only at 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Order Now"
                                    }],
                                 },
                                 {
                                   "title" : "M3-Beef Roganjosh & Chicken Kofta",
                                   "image_url" : "http://gdurl.com/2VdE",
                                   "subtitle" : "Available only at 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M4-Chicken Tikka & Samosa",
                                   "image_url" : "http://gdurl.com/NkeOL",
                                   "subtitle" : "Available only at 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M5-Kofta Butter Masala & Samosa (Veg)",
                                   "image_url" : "http://gdurl.com/Hq0P",
                                   "subtitle" : "Available only at 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M6-Lamb Korma & Beef Roganjosh",
                                   "image_url" : "http://gdurl.com/ZuLh",
                                   "subtitle" : "Available only at 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M7-Chicken Tikka & Beef Roganjosh",
                                   "image_url" : "http://gdurl.com/x77y",
                                   "subtitle" : "Available only at 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M8-Beef Roganjosh & Chicken Curry",
                                   "image_url" : "http://gdurl.com/2VdE",
                                   "subtitle" : "Available only at 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M9-Lamb Korma & Chicken Kofta",
                                   "image_url" : "http://gdurl.com/NkeOL",
                                   "subtitle" : "Available only at 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M10-Kofta Curry & Samosa (Veg)",
                                   "image_url" : "http://gdurl.com/Hq0P",
                                   "subtitle" : "Available only at 99,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Order Now"
                                    }]
                                 }
                             ]
                       } 
                   }
                },
        {
      "text": "Please select any option below:",
      "quick_replies": [
        {
          "content_type": "text",
          "title": "Home",
          "payload": "Home",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        },
        {
          "content_type": "text",
          "title": "Opening Hours",
          "payload": "Opening Hours",
          "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
        },
        {
           "content_type": "text",
           "title": "Contact Us",
           "payload": "Contact Us",
           "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
        }
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            ORDER BOOKING                                           #
#                                                                                    #
#************************************************************************************#
def engDefaultMenuOrderBooking(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                "text": "Do you want to spend a beautiful evening at our place? Call us now for table booking."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "We also take order for party. Don't worry! We'll deliver food at your doorstep."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"http://gdurl.com/QFrQ"
                     }
                 }
               },
                {
                   "attachment":{
                   "type":"template",
                   "payload":{
                   "template_type":"button",
                   "text":"Need further assistance? Talk to a representative",
                   "buttons":[
                       {
                        "type":"phone_number",
                        "title":"Call Buffet House",
                        "payload":"+4570707649"
                       }
                     ]
                   }
                  }
                },
                {
                  "text": "You can select the below options also",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Menu",
                  "payload": "Menu",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Take Away",
                  "payload": "Take Away",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/66559-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Opening Hours",
                  "payload": "Opening Hours",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
                 },
                 {
                  "content_type": "text",
                  "title": "Contact Us",
                  "payload": "Contact Us",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  },
                 {
                  "content_type": "text",
                  "title": "Home",
                  "payload": "Home",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
                 },
                 ]
                }
              ]
            }  
           };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            OPENING HOURS                                           #
#                                                                                    #
#************************************************************************************#
def engDefaultMenuOpeningHours(reqContext):
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                "text": "We are open everyday. We invite you to taste the best Indian cuisines here."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "Monday-Thursday: 16:00 - 21:00\nFriday-Sunday: 16:00 - 21:30 "
                },
                {
                    "sender_action": "typing_on"
                },
                {
                  "text": "You can select the below options also",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Menu",
                  "payload": "Menu",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Take Away",
                  "payload": "Take Away",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/66559-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Order Booking",
                  "payload": "Order Booking",
                  "image_url": "http://is5.mzstatic.com/image/thumb/Purple18/v4/77/13/96/771396f0-8059-c536-d17c-1806d9e22931/source/1200x630bb.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Contact Us",
                  "payload": "Contact Us",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  },
                  {
                   "content_type": "text",
                   "title": "Home",
                   "payload": "Home",
                   "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
                  }
                 ]
                }
              ]
            }  
           };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            CONTACT US                                              #
#                                                                                    #
#************************************************************************************#
def engDefaultMenuContactUs(reqContext):
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                "text": "Experience the best Indian cuisine here at Buffet House"
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "We are located within walking distance of Rutebilstation and Dokk1"
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "We also have sufficient parking facility, so don’t hesitate to bring your group for best Indian dining in Aarhus."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"http://gdurl.com/QFrQ"
                     }
                 }
                },
                {
                   "attachment":{
                   "type":"template",
                   "payload":{
                   "template_type":"button",
                   "text":"Need further assistance? Talk to a representative",
                   "buttons":[
                       {
                        "type":"phone_number",
                        "title":"Call Buffet House",
                        "payload":"+4570707649"
                       }
                     ]
                   }
                  }
                },
                {
                  "text": "You can select the below options also",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Menu",
                  "payload": "Menu",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Take Away",
                  "payload": "Take Away",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/66559-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Order Booking",
                  "payload": "Order Booking",
                  "image_url": "http://is5.mzstatic.com/image/thumb/Purple18/v4/77/13/96/771396f0-8059-c536-d17c-1806d9e22931/source/1200x630bb.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Home",
                  "payload": "Home",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Start Over",
                  "payload": "Start Over",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/72551-200.png"
                  }
                 ]
                }
              ]
            }  
           };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************************************************************#
#                                                                                                                                    #
#                                                                                                                                    #
#                      DANISH - ALL THE FUNCTIONS BELOW WILL BE RELATED TO DANISH LANGUAGE                                           #
#                                                                                                                                    #
#                                                                                                                                    #
#************************************************************************************************************************************#
#************************************************************************************#
#                                                                                    #
#                Danish Default Menu                                                #
#                                                                                    #
#************************************************************************************#
def danishDefaultMenu(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                "text": "Tak for at vælge dansk og velkommen igen."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"http://gdurl.com/y0fi"
                     }
                 }
               },
                {
                  "text": "Hvordan kan jeg hjælpe dig?",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Menu",
                  "payload": "danskmenu",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Tag Væk",
                  "payload": "dansktakeaway",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/66559-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Bestille Bestilling",
                  "payload": "Bestille Bestilling",
                  "image_url": "http://is5.mzstatic.com/image/thumb/Purple18/v4/77/13/96/771396f0-8059-c536-d17c-1806d9e22931/source/1200x630bb.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Åbningstider",
                  "payload": "Åbningstider",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
                 },
                 {
                  "content_type": "text",
                  "title": "Kontakt Os",
                  "payload": "Kontakt Os",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                 ]
                }
              ]
            }  
           };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                Main Menu - Quick Reply Options Only                                #
#                                                                                    #
#************************************************************************************#
def danishDefaultMainMenu(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                  "text": "Vælg venligst nedenstående muligheder:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Menu",
                  "payload": "danskmenu",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Tag Væk",
                  "payload": "dansktakeaway",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/66559-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Bestille Bestilling",
                  "payload": "Bestille Bestilling",
                  "image_url": "http://is5.mzstatic.com/image/thumb/Purple18/v4/77/13/96/771396f0-8059-c536-d17c-1806d9e22931/source/1200x630bb.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Åbningstider",
                  "payload": "Åbningstider",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
                 },
                 {
                  "content_type": "text",
                  "title": "Kontakt Os",
                  "payload": "Kontakt Os",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                 ]
                }
              ]
            }  
           };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                MENU ITEMS = Buffet + Items + Special                               #
#                                                                                    #
#************************************************************************************#
def danishMenuCriteriaMenu(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Buffet House Menu",
                                   "image_url" : "http://gdurl.com/xdw5",
                                   "subtitle" : "Bedste i byen retter, valgt kun til dig",
                                   "buttons": [{
                                        "type": "postback",
                                        "title": "Buffet",
                                        "payload":"danskbuffet"
                                    },
                                    {
                                        "type": "postback",
                                        "title": "Retter",
                                        "payload": "retter"
                                    },
                                    {
                                        "type": "postback",
                                        "title": "Special Tilbud",
                                        "payload": "tilbudspecial"
                                    }]
                                 }
                           ]
                       } 
                   }
                },
        {
      "text": "Vælg venligst et af nedenstående valgmuligheder:",
      "quick_replies": [
        {
          "content_type": "text",
          "title": "Hjem",
          "payload": "Hjem",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        },
        {
          "content_type": "text",
          "title": "Åbningstider",
          "payload": "Åbningstider",
          "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
        },
        {
          "content_type": "text",
          "title": "Kontakt Os",
          "payload": "Kontakt Os",
          "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
        },
        {
          "content_type": "text",
          "title": "Start Forfra",
          "payload": "Start Forfra",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/72551-200.png"
        }
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            BUFFET                                                  #
#                                                                                    #
#************************************************************************************#
def danishMenuCriteriaMenuBuffet (reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Events",
            "displayText": "Events",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"http://gdurl.com/RyLb"
                     }
                 }
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Gå ikke glip af den store indiske lækre buffet!"
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Buffet er tilgængelig hver dag fra kl. 17.00 til 21.00 kun for 99, - "
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "For børn under 10 år er buffetprisen 59.- kun"
               },
               
        {
      "text": "For at se andre muligheder, skal du klikke for nedenstående valgmuligheder:",
      "quick_replies": [
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "danskmenu",
          "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
          "content_type": "text",
          "title": "Hjem",
          "payload": "Hjem",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        },
        {
          "content_type": "text",
          "title": "Start Forfra",
          "payload": "Start Forfra",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/72551-200.png"
        }
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            ITEMS                                                   #
#                                                                                    #
#************************************************************************************#
def danMenuCriteriaMenuItems(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Taste the best - enjoy the variety  of dishes selected",
            "displayText": "Taste the best - enjoy the variety  of dishes selected",
            "data" : {
            "facebook" : [
                {
                   "sender_action": "typing_on"
                },
                {
                   "text": "Smag det bedste - nyd vores udvalg af retter",
                   "quick_replies": [
                {
                     "content_type": "text",
                     "title": "Forretter",
                     "payload": "Forretter",
                     "image_url": "https://cdn1.iconfinder.com/data/icons/food-drinks-set-2/96/Soup-512.png"
                },
                {
                     "content_type": "text",
                     "title": "Hovedret",
                     "payload": "Hovedret",
                     "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/1394544-200.png"
                },
                {
                     "content_type": "text",
                     "title": "Dessert",
                     "payload": "Dessert dansk",
                     "image_url": "https://image.flaticon.com/icons/png/512/53/53628.png"
                },
                {
                     "content_type": "text",
                     "title": "Menu",
                     "payload": "danskmenu",
                     "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                },
                {
                     "content_type": "text",
                     "title": "Hjem",
                     "payload": "Hjem",
                     "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
                },
             ]
         }
      ]
    } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            STARTER                                                 #
#                                                                                    #
#************************************************************************************#
def danMenuCriteriaMenuItemsStarter(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Poppadom",
                                   "image_url" : "http://gdurl.com/5HcY",
                                   "subtitle" : "Indisk snack specialitet \nKun tilgængelig for 35,-",
                                 },
                                 {
                                   "title" : "Chapli Kebab",
                                   "image_url" : "http://gdurl.com/p1Am",
                                   "subtitle" : "Pashtun-stil hakket kebab, der stammer fra Peshawar \nKun tilgængelig for 65,-",
                                 },
                                 {
                                   "title" : "Samosa",
                                   "image_url" : "http://gdurl.com/8qBs",
                                   "subtitle" : "Oprindelse i Mellemøsten tilbage for 10 århundrede \nKun tilgængelig for 49,-",
                                 },
                                 {
                                   "title" : "Salat",
                                   "image_url" : "http://gdurl.com/n6Gl",
                                   "subtitle" : "En gammel græsk og romersk delikatesse \nKun tilgængelig for 29,-",
                                 },
                             ]
                       } 
                   }
                },
               
        {
      "text": "Vælg venligst et af nedenstående valgmuligheder:",
      "quick_replies": [
        {
          "content_type": "text",
          "title": "Hovedret",
          "payload": "Hovedret",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/1394544-200.png"
        },
        {
          "content_type": "text",
          "title": "Dessert",
          "payload": "Dessert dansk",
          "image_url": "https://image.flaticon.com/icons/png/512/53/53628.png"
        },
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "danskmenu",
          "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
           "content_type": "text",
           "title": "Hjem",
           "payload": "Hjem",
           "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        },
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            MAIN DISH                                               #
#                                                                                    #
#************************************************************************************#
def danMenuCriteriaMenuItemsMainDish(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Nan/Garlic Nan",
                                   "image_url" : "http://gdurl.com/swcc",
                                   "subtitle" : "Friskbagt Nan fra Tandoor Ovn \nKun tilgængelig for 19 & 23,-",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Curry",
                                   "image_url" : "http://gdurl.com/76uW",
                                   "subtitle" : "Curry er en verdensberømt skål i århundreder \nKun tilgængelig for 99, 109 & 119,-",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Korma",
                                   "image_url" : "http://gdurl.com/TQ2f",
                                   "subtitle" : "En Moghul skål af indisk oprindelse fra det 16. århundrede \nKun tilgængelig for 85, 95 & 99,-",
                                 },
                                 {
                                   "title" : "Butter Chicken/Beef/Lamb",
                                   "image_url" : "http://gdurl.com/orET",
                                   "subtitle" : "Smag århundredets gamle passion for mad-elskere \nKun tilgængelig for 79, 99 & 109,-",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Roganjosh",
                                   "image_url" : "http://gdurl.com/RRTP",
                                   "subtitle" : "En Indisk Moghul skål, forvirket af persisk køkken \nKun tilgængelig for at 89,-",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Kashmiri",
                                   "image_url" : "http://gdurl.com/chrv",
                                   "subtitle" : "Kasmiri køkkener serverer altid din smagsløg \nKun tilgængelig for 79, 89,-",
                                 },
                                 {
                                   "title" : "Palak Paneer",
                                   "image_url" : "http://gdurl.com/jFhH",
                                   "subtitle" : "En vegetarisk skål fra det Indiske subkontinent \nKun tilgængelig for at 79,-",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Sag",
                                   "image_url" : "http://gdurl.com/hKV1",
                                   "subtitle" : "En specialitet du skal prøve her \nKun tilgængelig for 75, 79 & 109,-",
                                }
                        ]
                 } 
             }
        },
        {
      "text": "Vælg venligst et af nedenstående valgmuligheder:",
      "quick_replies": [
        {
         "content_type": "text",
         "title": "Forretter",
         "payload": "Forretter",
         "image_url": "https://cdn1.iconfinder.com/data/icons/food-drinks-set-2/96/Soup-512.png"
        },
        {
         "content_type": "text",
         "title": "Dessert",
         "payload": "Dessert dansk",
         "image_url": "https://image.flaticon.com/icons/png/512/53/53628.png"
        },
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "danskmenu",
          "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
          "content_type": "text",
          "title": "Hjem",
          "payload": "Hjem",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        }
       ]
     }
    ]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            DESSERT                                                 #
#                                                                                    #
#************************************************************************************#
def danMenuCriteriaMenuItemsDessert(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Vanilije Milkshake",
                                   "image_url" : "http://gdurl.com/V74H",
                                   "subtitle" : "Kun tilgængelig for 39,-",
                                 },
                                 {
                                   "title" : "Pistacie Milkshake",
                                   "image_url" : "http://gdurl.com/JjAF",
                                   "subtitle" : "Kun tilgængelig for 39,-",
                                 },
                                 {
                                   "title" : "Jordbær Milkshake",
                                   "image_url" : "http://gdurl.com/rU7E",
                                   "subtitle" : "Kun tilgængelig for 39,-",
                                 },
                                 {
                                   "title" : "Chocolade Milkshake",
                                   "image_url" : "http://gdurl.com/sA7I",
                                   "subtitle" : "Kun tilgængelig for 39,-",
                                 },
                                 {
                                   "title" : "Mango Lasse Yoghurt",
                                   "image_url" : "http://gdurl.com/kslO",
                                   "subtitle" : "Kun tilgængelig for 39,-",
                                 },
                                 {
                                   "title" : "0,5L Sodavand",
                                   "image_url" : "http://gdurl.com/zKOf",
                                   "subtitle" : "Kun tilgængelig for 25,-",
                                 },
                                 {
                                   "title" : "1,5L Sodavand",
                                   "image_url" : "http://gdurl.com/hH4c",
                                   "subtitle" : "Kun tilgængelig for 35,-",
                                 },
                                 {
                                   "title" : "Kildevand",
                                   "image_url" : "http://gdurl.com/Xs_K",
                                   "subtitle" : "Kun tilgængelig for 25,-",
                                 }
                             ]
                       } 
                   }
                },
               
        {
      "text": "Vælg venligst et af nedenstående valgmuligheder:",
      "quick_replies": [
        {
         "content_type": "text",
         "title": "Forretter",
         "payload": "Forretter",
         "image_url": "https://cdn1.iconfinder.com/data/icons/food-drinks-set-2/96/Soup-512.png"
        },
        {
         "content_type": "text",
         "title": "Hovedret",
         "payload": "Hovedret",
         "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/1394544-200.png"
        },
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "danskmenu",
          "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
          "content_type": "text",
          "title": "Hjem",
          "payload": "Hjem",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        }
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            SPECIAL                                                 #
#                                                                                    #
#************************************************************************************#
def danMenuCriteriaMenuItemsSpecialMenu(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Sabzi Biriyani",
                                   "image_url" : "http://gdurl.com/QpGk",
                                   "subtitle" : "Kun tilgængelig for 119,-",
                                 },
                                 {
                                   "title" : "Chicken Biriyani",
                                   "image_url" : "http://gdurl.com/pRyi",
                                   "subtitle" : "Kun tilgængelig for 119,-",
                                 },
                                 {
                                   "title" : "Chicken Tikka Biriyani",
                                   "image_url" : "http://gdurl.com/RH5I",
                                   "subtitle" : "Kun tilgængelig for 119,-",
                                 },
                                 {
                                   "title" : "Lamb Biriyani",
                                   "image_url" : "http://gdurl.com/89Of",
                                   "subtitle" : "Kun tilgængelig for 139,-",
                                 },
                                 {
                                   "title" : "Beef Biriyani",
                                   "image_url" : "http://gdurl.com/dHh8",
                                   "subtitle" : "Kun tilgængelig for 119,-",
                                 },
                                 {
                                   "title" : "Luksus Biriyani",
                                   "image_url" : "http://gdurl.com/EUAwK",
                                   "subtitle" : "Kun tilgængelig for 139,-",
                                 }
                             ]
                       } 
                   }
                },
               
        {
      "text": "Vælg venligst et af nedenstående valgmuligheder:",
      "quick_replies": [
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "danskmenu",
          "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
          "content_type": "text",
          "title": "Hjem",
          "payload": "Hjem",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        },
        {
          "content_type": "text",
          "title": "Start Forfra",
          "payload": "Start Forfra",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/72551-200.png"
        }
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            TAKE AWAY                                               #
#                                                                                    #
#************************************************************************************#
def danDefaultMenuTakeAway(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Folk elsker at tage vores mad med for at nyde hjemme"
               },
               {
                "text": "Derfor har vi lavet specielle pakker til afhentning."
               },
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"http://gdurl.com/HNzO"
                     }
                 }
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Vi tager også engrosordre til fester eller samling. Vi leverer mad lige ved døren lige i nærheden Aarhus."
               },
               {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "M1-Butter Chicken og Sag Allo",
                                   "image_url" : "http://gdurl.com/ZuLh",
                                   "subtitle" : "Kun tilgængelig for 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Bestil nu"
                                    }]
                                 },
                                 {
                                   "title" : "M2-Lam Korma og Chicken Curry",
                                   "image_url" : "http://gdurl.com/x77y",
                                   "subtitle" : "Kun tilgængelig for 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Bestil nu"
                                    }],
                                 },
                                 {
                                   "title" : "M3-Beef Roganjosh og Chicken Kofta",
                                   "image_url" : "http://gdurl.com/2VdE",
                                   "subtitle" : "Kun tilgængelig for 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Bestil nu"
                                    }]
                                 },
                                 {
                                   "title" : "M4-Chicken Tikka og Samosa",
                                   "image_url" : "http://gdurl.com/NkeOL",
                                   "subtitle" : "Kun tilgængelig for 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Bestil nu"
                                    }]
                                 },
                                 {
                                   "title" : "M5-Kofta Butter Masala og Samosa (Veg)",
                                   "image_url" : "http://gdurl.com/Hq0P",
                                   "subtitle" : "Kun tilgængelig for 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Bestil nu"
                                    }]
                                 },
                                 {
                                   "title" : "M6-Lam Korma og Beef Roganjosh",
                                   "image_url" : "http://gdurl.com/ZuLh",
                                   "subtitle" : "Kun tilgængelig for 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Bestil nu"
                                    }]
                                 },
                                 {
                                   "title" : "M7-Chicken Tikka og Beef Roganjosh",
                                   "image_url" : "http://gdurl.com/x77y",
                                   "subtitle" : "Kun tilgængelig for 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Bestil nu"
                                    }]
                                 },
                                 {
                                   "title" : "M8-Beef Roganjosh og Chicken Curry",
                                   "image_url" : "http://gdurl.com/2VdE",
                                   "subtitle" : "Kun tilgængelig for 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Bestil nu"
                                    }]
                                 },
                                 {
                                   "title" : "M9-Lamb Korma og Chicken Kofta",
                                   "image_url" : "http://gdurl.com/NkeOL",
                                   "subtitle" : "Kun tilgængelig for 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Bestil nu"
                                    }]
                                 },
                                 {
                                   "title" : "M10-Kofta Curry og Samosa (Veg)",
                                   "image_url" : "http://gdurl.com/Hq0P",
                                   "subtitle" : "Kun tilgængelig for 99,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "http://buffet-house.dk/Menu",
                                        "title": "Bestil nu"
                                    }]
                                 }
                             ]
                       } 
                   }
                },
        {
      "text": "Vælg venligst et af nedenstående valgmuligheder:",
      "quick_replies": [
        {
          "content_type": "text",
          "title": "Hjem",
          "payload": "Hjem",
          "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
        },
        {
          "content_type": "text",
          "title": "Åbningstider",
          "payload": "Åbningstider",
          "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
        },
        {
          "content_type": "text",
          "title": "Kontakt Os",
          "payload": "Kontakt Os",
          "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
        }
       ]
     }]
   } 
 };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            ORDER BOOKING                                           #
#                                                                                    #
#************************************************************************************#
def danDefaultMenuOrderBooking(reqContext):
    print (reqContext.get("result").get("resolvedQuery"))
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                "text": "Vil du tilbringe en smuk aften for vores sted? Ring til os nu for bordbestilling."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "Vi tager også ordre til fest. Bare rolig! Vi leverer mad lige uden for døren."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"http://gdurl.com/QFrQ"
                     }
                 }
               },
                {
                   "attachment":{
                   "type":"template",
                   "payload":{
                   "template_type":"button",
                   "text":"Har du brug for yderligere assistance? Tal med en repræsentant",
                   "buttons":[
                       {
                        "type":"phone_number",
                        "title":"Ring Buffet House",
                        "payload":"+4570707649"
                       }
                     ]
                   }
                  }
                },
                {
                  "text": "Du kan også vælge nedenstående valgmuligheder",
                  "quick_replies": [
                  {
                  "content_type": "text",
                  "title": "Hjem",
                  "payload": "Hjem",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Menu",
                  "payload": "danskmenu",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Tag Væk",
                  "payload": "dansktakeaway",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/66559-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Bestille Bestilling",
                  "payload": "Bestille Bestilling",
                  "image_url": "http://is5.mzstatic.com/image/thumb/Purple18/v4/77/13/96/771396f0-8059-c536-d17c-1806d9e22931/source/1200x630bb.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Åbningstider",
                  "payload": "Åbningstider",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
                 },
                 {
                  "content_type": "text",
                  "title": "Kontakt Os",
                  "payload": "Kontakt Os",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                 ]
                }
              ]
            }  
           };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            OPENING HOURS                                           #
#                                                                                    #
#************************************************************************************#
def danDefaultMenuOpeningHours(reqContext):
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                "text": "Vi har åbnet hver dag. Vi inviterer dig til at smage de bedste indiske retter her."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "Mandag-Torsdag: 16:00-21:00\nFredag-Søndag: 16:00-21:30"
                },
                {
                    "sender_action": "typing_on"
                },
                {
                  "text": "Du kan også vælge nedenstående valgmuligheder",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Hjem",
                  "payload": "Hjem",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/77002-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Menu",
                  "payload": "danskmenu",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Tag Væk",
                  "payload": "dansktakeaway",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/66559-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Bestille Bestilling",
                  "payload": "Bestille Bestilling",
                  "image_url": "http://is5.mzstatic.com/image/thumb/Purple18/v4/77/13/96/771396f0-8059-c536-d17c-1806d9e22931/source/1200x630bb.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Kontakt Os",
                  "payload": "Kontakt Os",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                 ]
                }
              ]
            }  
           };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#                            CONTACT US                                              #
#                                                                                    #
#************************************************************************************#
def danDefaultMenuContactUs(reqContext):
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    res = {
            "speech": "Main Menu",
            "displayText": "Main Menu",
            "data" : {
            "facebook" : [
                {
                    "sender_action": "typing_on"
                },
                {
                "text": "Oplev det bedste indiske retter her for Buffet House"
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "Vi er beliggende inden for gåafstand fra Rutebilstation og Dokk1"
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "Vi har også tilstrækkelig parkeringsplads, så tøv ikke med at bringe din gruppe til den bedste indiske spisestue i Århus."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"http://gdurl.com/QFrQ"
                     }
                 }
                },
                {
                   "attachment":{
                   "type":"template",
                   "payload":{
                   "template_type":"button",
                   "text":"Har du brug for yderligere assistance? Tal med en repræsentant",
                   "buttons":[
                       {
                        "type":"phone_number",
                        "title":"Ring Buffet House",
                        "payload":"+4570707649"
                       }
                     ]
                   }
                  }
                },
                {
                  "text": "Du kan også vælge nedenstående valgmuligheder",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Menu",
                  "payload": "danskmenu",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Tag Væk",
                  "payload": "dansktakeaway",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/66559-200.png"
                 },
                 {
                  "content_type": "text",
                  "title": "Bestille Bestilling",
                  "payload": "Bestille Bestilling",
                  "image_url": "http://is5.mzstatic.com/image/thumb/Purple18/v4/77/13/96/771396f0-8059-c536-d17c-1806d9e22931/source/1200x630bb.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Åbningstider",
                  "payload": "Åbningstider",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
                 },
                 {
                  "content_type": "text",
                  "title": "Start Forfra",
                  "payload": "Start Forfra",
                  "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/72551-200.png"
                 }
                 ]
                }
              ]
            }  
           };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 7000))
    print("Starting APPLICATION on port %d" % port)
    context.run(debug=True, port=port, host='0.0.0.0')