import json
import os
import constants
from google.appengine.ext.webapp import template


from authhandler import AuthHandler
from models.point import Point
from models.whysaurusexception import WhysaurusException

class LinkPoint(AuthHandler):
    def post(self):
        resultJSON = json.dumps({'result': False})
        supportingPoint, supportingPointRoot = Point.getCurrentByUrl(self.request.get('supportingPointURL'))
        oldPoint, oldPointRoot = Point.getCurrentByUrl(self.request.get('parentPointURL'))
        user = self.current_user
        linkType = self.request.get('linkType')

        if user:
            try:
                newLink = [{'pointRoot':supportingPointRoot,
                            'pointCurrentVersion':supportingPoint,
                            'linkType':self.request.get('linkType')}
                            ]
                newVersion = oldPoint.update(
                    pointsToLink=newLink,
                    user=user
                )
            except WhysaurusException as e:
                resultJSON = json.dumps({'result': False, 'error': e.message})
            else:
                if newVersion:
                    newLinkPointHTML = json.dumps(
                        self.template_render('linkPoint.html', {
                            'point': supportingPoint, 
                            'linkType': linkType
                        }))
                    resultJSON = json.dumps({
                        'result': True,
                        'numLinkPoints': newVersion.linkCount(linkType),
                        'newLinkPoint':newLinkPointHTML,
                        'authorURL': self.current_user.url,
                        'author': newVersion.authorName, 
                        'dateEdited': newVersion.PSTdateEdited.strftime('%b. %d, %Y, %I:%M %p'),                                                      
                    })
                else:
                    json.dumps({'result': False, 'error': 'There was a problem updating the point.'})
        else:
            resultJSON = json.dumps({'result': 'ACCESS DENIED!'})
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(resultJSON)
