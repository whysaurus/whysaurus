import json
from authhandler import AuthHandler
from models.point import Point
from models.whysaurusexception import WhysaurusException

class LinkPoint(AuthHandler):
    def post(self):
        resultJSON = json.dumps({'result': False})
        supportingPoint, supportingPointRoot = Point.getCurrentByUrl(self.request.get('supportingPointURL'))
        oldPoint, oldPointRoot = Point.getCurrentByUrl(self.request.get('parentPointURL'))
        user = self.current_user

        if user:
            try:
                oldPoint.update(
                    newSupportingPoint=supportingPointRoot,
                    user=user
                )
            except WhysaurusException as e:
                resultJSON = json.dumps({'result': False, 'error': str(e)})
            else:
                resultJSON = json.dumps({'result': True})
        else:
            resultJSON = json.dumps({'result': 'ACCESS DENIED!'})
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(resultJSON)