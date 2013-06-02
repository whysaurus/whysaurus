import json
from authhandler import AuthHandler
from models.point import Point

class NewPoint(AuthHandler):
    def post(self):
        user = self.current_user
        resultJSON = json.dumps({'result': False, 'error': 'Not authorized'})
        if user:
            newPoint, newPointRoot = Point.create(
                title=self.request.get('title'),
                content=self.request.get('content'),
                summaryText=self.request.get('plainText'),
                user=user,
                imageURL=self.request.get('imageURL'),
                imageAuthor=self.request.get('imageAuthor'),
                imageDescription=self.request.get('imageDescription'))
        if newPoint:
            resultJSON = json.dumps({'result': True, 'pointURL': newPoint.url})
        else:
            resultJSON = json.dumps({'result': False, 'error': 'Failed to create point.'})
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(resultJSON)
