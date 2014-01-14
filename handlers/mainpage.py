import os
import constants
import logging
import json

from google.appengine.ext.webapp import template

from authhandler import AuthHandler
from models.point import PointRoot, FeaturedPoint

class MainPage(AuthHandler):
    def getMainPageLeft(self):
        
        newPoints = PointRoot.getRecentCurrentPoints()
        featuredPoint = FeaturedPoint.getFeaturedPoint()
            
        vals = {
            'recentlyActive': newPoints,
            'featuredPoint': featuredPoint,
            'user': self.current_user
        }
        self.response.headers["Content-Type"] = 'application/json; charset=utf-8'        
        html = self.template_render('mainPageLeftColumn.html', vals)
        resultJSON = json.dumps({
            'result': True,
            'html': html,
        }) 
        self.response.out.write(resultJSON) 
        
    def getMainPageRight(self):      
        user = self.current_user
        self.response.headers["Content-Type"] = 'application/json; charset=utf-8'        

        if user:
            recentlyViewedPoints = user.getRecentlyViewed()
        else:
            recentlyViewedPoints = []
            
        vals = {
            'recentlyViewed': recentlyViewedPoints,
            'user': user
        }
        html = self.template_render('mainPageRightColumn.html', vals)
        

        resultJSON = json.dumps({
            'result': True,
            'html': html,
        }) 
        self.response.out.write(resultJSON) 
    
    def get(self):

        newPoints = PointRoot.getRecentCurrentPoints()
        featuredPoint = FeaturedPoint.getFeaturedPoint()
        user = None

        if self.logged_in:
            user = self.current_user

        # GET RECENTLY VIEWED
        if user:
            recentlyViewedPoints = user.getRecentlyViewed()
            user.getActiveNotifications()
        else:
            recentlyViewedPoints = []
        
        template_values = {
            'recentlyActive': newPoints,
            'recentlyViewed': recentlyViewedPoints,
            'featuredPoint': featuredPoint,
            'user': user,
            'thresholds': constants.SCORETHRESHOLDS,
            'currentArea':self.session.get('currentArea')
        }
        self.response.out.write(self.template_render('index.html', template_values))
