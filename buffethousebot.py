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
    print (json.dumps(reqContext, indent=4))
    print ("****************")
    print (reqContext.get("result").get("action"))
    print ("****************")
    if reqContext.get("result").get("action") == "input.welcome":
       return welcome()
    elif reqContext.get("result").get("action") == "english.default.menu": 
       return englishDefaultMenu()
    elif reqContext.get("result").get("action") == "english.Menu.Criteria.Menu":
       return englishMenuCriteriaMenu()
    elif reqContext.get("result").get("action") == "english.Menu.Criteria.Menu.Buffet":
       return englishMenuCriteriaMenu()
    elif reqContext.get("result").get("action") == "eng.Menu.Criteria.Menu.Items":
       return engMenuCriteriaMenuItems()
    elif reqContext.get("result").get("action") == "eng.Menu.Criteria.Menu.Items.Starter":
       return engMenuCriteriaMenuItemsStarter()
    elif reqContext.get("result").get("action") == "eng.Menu.Criteria.Menu.Items.MainDish":
       return engMenuCriteriaMenuItemsMainDish()
    elif reqContext.get("result").get("action") == "eng.Menu.Criteria.Menu.Items.Dessert":
       return engMenuCriteriaMenuItemsDessert()
    elif reqContext.get("result").get("action") == "eng.default.menu.take.away":
       return engDefaultMenuTakeAway()
    elif reqContext.get("result").get("action") == "eng.default.menu.order.booking": 
       return engDefaultMenuOrderBooking()
    elif reqContext.get("result").get("action") == "eng.default.menu.opening.hours":
       return engDefaultMenuOpeningHours()
    elif reqContext.get("result").get("action") == "eng.default.menu.contact.us":
       return engDefaultMenuContactUs()
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
    data = request.json
    print (data)
    if data is None:
        return {}
    entry = data.get('originalRequest')
    dataall = entry.get('data')
    print (dataall)
    sender = dataall.get('sender')
    id = sender.get('id')
    #print ("id :" + id)
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
                                   "title" : "Hi " + first_name + "! Welcome to Buffet House Restaurant" + emoji.emojize(':smiley:', use_aliases=True),
                                   "image_url" : "http://www.pdcdc.org/wp-content/uploads/2016/03/restaurant-939435_960_720.jpg",
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
                 "text": "I’m Indiskbot at your service."
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
def englishDefaultMenu():
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
                        "url":"http://www.thehindubusinessline.com/multimedia/dynamic/02973/BL16_MAHARAJA_AIRI_2973400e.jpg"
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
#                MENU ITEMS = Buffet + Items + Special                               #
#                                                                                    #
#************************************************************************************#
def englishMenuCriteriaMenu(reqContext):
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
                                   "image_url" : "http://gdurl.com/NyZL",
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
      "text": "Please select any of the menu from above. \nTo view other options, please click below options:",
      "quick_replies": [
        {
          "content_type": "text",
          "title": "Start Over",
          "payload": "Start Over",
          "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
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
                        "url":"BUFFET DSLR IMAGE"
                     }
                 }
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Try our big delicious buffet with a wide variety of dishes, appetizers and salads"
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Buffet available all day from 17-21 for only 99 dk.\nFor children under 10 year, it is 59 dk only "
               },
               {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Nan",
                                   "image_url" : "Nan image",
                                   "subtitle" : "Fresh baked Nan from Tandoor oven",
                                 },
                                 {
                                   "title" : "Pulav Rice",
                                   "image_url" : "Pulav Rice Image",
                                   "subtitle" : "Tasty Pulav Rice",
                                 },
                                 {
                                   "title" : "Samosa",
                                   "image_url" : "Samosa Image",
                                   "subtitle" : "Authentic Indian Sanck - cannot eat just one",
                                 },
                                 {
                                   "title" : "Chicken Tandoori",
                                   "image_url" : "Chicken Tandoori Image",
                                   "subtitle" : "Invented in 1950s, this is an iconic Indian starter",
                                 },
                                 {
                                   "title" : "Chicken Butter Masala",
                                   "image_url" : "Chicken Butter Masala Image",
                                   "subtitle" : "A century old delicious dish - still favorite to food lovers",
                                 },
                                 {
                                   "title" : "Beef Roganjosh",
                                   "image_url" : "Beef Roganjosh Image",
                                   "subtitle" : "An aromatic dish of Persian origin - one of the signature recipes of Kashmiri cuisine",
                                 },
                                 {
                                   "title" : "Chicken Kofta Korma",
                                   "image_url" : "Chicken Kofta Korma Image",
                                   "subtitle" : "Tasty and spicy equivalent of famous meatballs, originated in Middle East",
                                 },
                                 {
                                   "title" : "Chicken Curry",
                                   "image_url" : "Chicken Curry Image",
                                   "subtitle" : "A global cuisine, with Indian origin from heart - a must try dish",
                                 },
                                 {
                                   "title" : "Sag Allo",
                                   "image_url" : "Sag Allo Image",
                                   "subtitle" : "Do not miss the tasty vegeterian dish",
                                 },
                                 {
                                   "title" : "Allo Dum",
                                   "image_url" : "Allo Dum Image",
                                   "subtitle" : "Do not miss the tasty vegeterian dish",
                                 }
                           ]
                       } 
                   }
                },
        {
      "text": "Taste our Chef's special excuisite dishes at reasonable price. \nTo view other options, please click below options:",
      "quick_replies": [
        {
         "content_type": "text",
         "title": "Menu",
         "payload": "Menu",
         "image_url": "https://cdn1.iconfinder.com/data/icons/hotel-restaurant/512/16-512.png"
        },
        {
         "content_type": "text",
         "title": "Start Over",
         "payload": "Start Over",
         "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREBeHDCh_So0LEhyWapjjilpDFiRLXMaeuwUfc1rrxu3qShTCUqQ"
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
def engMenuCriteriaMenuItems():
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
      "text": "Taste the best - enjoy the variety  of dishes selected",
      "quick_replies": [
        {
          "content_type": "text",
          "title": "Starter",
          "payload": "Starter",
          "image_url": "Starter icon"
        },
        {
          "content_type": "text",
          "title": "Main Dish",
          "payload": "Main Dish",
          "image_url": "Main Dish icon"
        },
        {
          "content_type": "text",
          "title": "Dessert",
          "payload": "Dessert",
          "image_url": "Dessert icon"
        },
        {
          "content_type": "text",
          "title": "Back",
          "payload": "Back",
          "image_url": "Back icon"
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
#                            STARTER                                                 #
#                                                                                    #
#************************************************************************************#
def engMenuCriteriaMenuItemsStarter():
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
                                   "image_url" : "Poppadom image",
                                   "subtitle" : "Fresh baked Nan from Tandoor oven",
                                 },
                                 {
                                   "title" : "Chapli Kebab",
                                   "image_url" : "Chapli Kebab Image",
                                   "subtitle" : "Tasty Pulav Rice",
                                 },
                                 {
                                   "title" : "Samosa",
                                   "image_url" : "Samosa Image",
                                   "subtitle" : "Authentic Indian Sanck - cannot eat just one",
                                 },
                                 {
                                   "title" : "Salat",
                                   "image_url" : "Salat Image",
                                   "subtitle" : "Invented in 1950s, this is an iconic Indian starter",
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
          "title": "Back",
          "payload": "Back",
          "image_url": "Back icon"
        },
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "Menu",
          "image_url": "Menu icon"
        },
        {
          "content_type": "text",
          "title": "Start Over",
          "payload": "Start Over",
          "image_url": "Start Over icon"
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
#                            MAIN DISH                                               #
#                                                                                    #
#************************************************************************************#
def engMenuCriteriaMenuItemsMainDish():
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
                                   "image_url" : "Chicken Curry image",
                                   "subtitle" : "Available only at 19 & 23 dk",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Curry",
                                   "image_url" : "Chicken Curry image",
                                   "subtitle" : "Available only at 99, 109 & 119 dk",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Korma",
                                   "image_url" : "Lamb Curry Image",
                                   "subtitle" : "Available only at 85, 95 & 99 dk",
                                 },
                                 {
                                   "title" : "Butter Chicken/Lamb/Beef",
                                   "image_url" : "Beef Curry Image",
                                   "subtitle" : "Available only at 79, 99 & 109 dk",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Kashmiri",
                                   "image_url" : "Chicken Kofta Curry Image",
                                   "subtitle" : "Available only at 79, 89 & 89 dk",
                                 },
                                 {
                                   "title" : "Beef/Lamb Roganjosh",
                                   "image_url" : "Chicken Kofta Curry Image",
                                   "subtitle" : "Available only at 89 dk",
                                 },
                                 {
                                   "title" : "Palak Paneer",
                                   "image_url" : "Chicken Kofta Curry Image",
                                   "subtitle" : "Available only at 79 dk",
                                 },
                                 {
                                   "title" : "Sag Allo",
                                   "image_url" : "Chicken Kofta Curry Image",
                                   "subtitle" : "Available only at 69 dk",
                                 },
                                 {
                                   "title" : "Chicken/Beef/Lamb Sag",
                                   "image_url" : "Chicken Kofta Curry Image",
                                   "subtitle" : "Available only at 75, 79 & 109 dk",
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
          "title": "Back",
          "payload": "Back",
          "image_url": "Back icon"
        },
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "Menu",
          "image_url": "Menu icon"
        },
        {
          "content_type": "text",
          "title": "Start Over",
          "payload": "Start Over",
          "image_url": "Start Over icon"
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
#                            DESSERT                                                 #
#                                                                                    #
#************************************************************************************#
def engMenuCriteriaMenuItemsDessert():
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
                                   "image_url" : "Vanilla Milkshake image",
                                   "subtitle" : "Available only at 39,-",
                                 },
                                 {
                                   "title" : "Pistacie Milkshake",
                                   "image_url" : "Pistacie Milkshake image",
                                   "subtitle" : "Available only at 39,-",
                                 },
                                 {
                                   "title" : "Strawberry Milkshake",
                                   "image_url" : "Strawberry Milkshake Image",
                                   "subtitle" : "Available only at 39,-",
                                 },
                                 {
                                   "title" : "Chocolate Milkshake",
                                   "image_url" : "Chocolate Milkshake Image",
                                   "subtitle" : "Available only at 39,-",
                                 },
                                 {
                                   "title" : "Mango Lasse Yoghurt",
                                   "image_url" : "Chicken Kofta Curry Image",
                                   "subtitle" : "Available only at 39,-",
                                 },
                                 {
                                   "title" : "0,5L Sodavand",
                                   "image_url" : "0,5L Sodavand Image",
                                   "subtitle" : "Available only at 25,-",
                                 },
                                 {
                                   "title" : "1,5L Sodavand",
                                   "image_url" : "1,5L Sodavand Image",
                                   "subtitle" : "Available only at 35,-",
                                 },
                                 {
                                   "title" : "Cold Water",
                                   "image_url" : "Cold Water Image",
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
          "title": "Back",
          "payload": "Back",
          "image_url": "Back icon"
        },
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "Menu",
          "image_url": "Menu icon"
        },
        {
          "content_type": "text",
          "title": "Start Over",
          "payload": "Start Over",
          "image_url": "Start Over icon"
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
def engMenuCriteriaMenuItemsSpecialMenu():
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
                                   "image_url" : "Sabzi Biriyani image",
                                   "subtitle" : "Available only at 119,-",
                                 },
                                 {
                                   "title" : "Chicken Biriyani",
                                   "image_url" : "Chicken Biriyani image",
                                   "subtitle" : "Available only at 119,-",
                                 },
                                 {
                                   "title" : "Chicken Tikka Biriyani",
                                   "image_url" : "Chicken Tikka Biriyani Image",
                                   "subtitle" : "Available only at 119,-",
                                 },
                                 {
                                   "title" : "Lamb Biriyani",
                                   "image_url" : "Lamb Biriyani Image",
                                   "subtitle" : "Available only at 139,-",
                                 },
                                 {
                                   "title" : "Beef Biriyani",
                                   "image_url" : "Beef Biriyani Image",
                                   "subtitle" : "Available only at 119,-",
                                 },
                                 {
                                   "title" : "Luxury Biriyani",
                                   "image_url" : "Luxury Biriyani Image",
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
          "title": "Back",
          "payload": "Back",
          "image_url": "Back icon"
        },
        {
          "content_type": "text",
          "title": "Menu",
          "payload": "Menu",
          "image_url": "Menu icon"
        },
        {
          "content_type": "text",
          "title": "Start Over",
          "payload": "Start Over",
          "image_url": "Start Over icon"
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
def engDefaultMenuTakeAway():
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
                "text": "People love to take away our food to enjoy at home./nThat’s why we have created special packages for take away."
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
                                   "image_url" : "Sabzi Biriyani image",
                                   "subtitle" : "Available only at 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://indiskbuffet.dk/",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M2-Lamb Korma & Chicken Curry",
                                   "image_url" : "Sabzi Biriyani image",
                                   "subtitle" : "Available only at 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://indiskbuffet.dk/",
                                        "title": "Order Now"
                                    }],
                                 },
                                 {
                                   "title" : "M3-Beef Roganjosh & Chicken Kofta",
                                   "image_url" : "Sabzi Biriyani image",
                                   "subtitle" : "Available only at 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://indiskbuffet.dk/",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M4-Chicken Tikka & Samosa",
                                   "image_url" : "Sabzi Biriyani image",
                                   "subtitle" : "Available only at 79,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://indiskbuffet.dk/",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M5-Kofta Butter Masala & Samosa (Veg)",
                                   "image_url" : "Sabzi Biriyani image",
                                   "subtitle" : "Available only at 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://indiskbuffet.dk/",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M6-Lamb Korma & Beef Roganjosh",
                                   "image_url" : "Sabzi Biriyani image",
                                   "subtitle" : "Available only at 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://indiskbuffet.dk/",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M7-Chicken Tikka & Beef Roganjosh",
                                   "image_url" : "Sabzi Biriyani image",
                                   "subtitle" : "Available only at 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://indiskbuffet.dk/",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M8-Beef Roganjosh & Chicken Curry",
                                   "image_url" : "Sabzi Biriyani image",
                                   "subtitle" : "Available only at 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://indiskbuffet.dk/",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M9-Lamb Korma & Chicken Kofta",
                                   "image_url" : "Sabzi Biriyani image",
                                   "subtitle" : "Available only at 89,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://indiskbuffet.dk/",
                                        "title": "Order Now"
                                    }]
                                 },
                                 {
                                   "title" : "M10-Kofta Curry & Samosa (Veg)",
                                   "image_url" : "Sabzi Biriyani image",
                                   "subtitle" : "Available only at 99,-",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://indiskbuffet.dk/",
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
          "title": "Start Over",
          "payload": "Start Over",
          "image_url": "Start Over icon"
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
def engDefaultMenuOrderBooking():
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
                "text": "Do you want to spend a beautiful evening at our place? Please book table beforehand."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "You can also book order for any party. Don't worry! We'll deliver food at your doorstep."
                },
                {
                    "sender_action": "typing_on"
                },
                {
                 "text": "Please call us our representative"
                },
                {
                 "type":"phone_number",
                 "title":"Call Buffet House",
                 "payload":"+4570707649"
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
def engDefaultMenuOpeningHours():
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
def engDefaultMenuContactUs():
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
                 "text": "We are within walking distance of Central Station and Dokk1"
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
                 "text": "Please call us our representative"
                },
                {
                 "type":"phone_number",
                 "title":"Call Buffet House",
                 "payload":"+4570707649"
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
                  "title": "Start Over",
                  "payload": "Start Over",
                  "image_url": "Start Over icon"
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