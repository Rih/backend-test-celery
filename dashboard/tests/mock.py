

BOT_RESPONSE = {
    'success': {
        'ok': True,
        'channel': 'C02757KU9DJ',
        'ts': '1625258795.000600',
        'message': {
            'bot_id': 'B026Z27QMBL',
            'type': 'message',
            'text': 'hola',
            'user': 'U027586HNR2',
            'ts': '1625258795.000600',
            'team': 'T026Z1GC2R0',
            'bot_profile': {
                'id': 'B026Z27QMBL',
                'deleted': False,
                'name': 'Nora bot',
                'updated': 1625250098,
                'app_id': 'A02757Q2E92',
                'icons': {
                    'image_36': 'https://a.slack-edge.com/80588/img/plugins/app/bot_36.png',
                    'image_48': 'https://a.slack-edge.com/80588/img/plugins/app/bot_48.png',
                    'image_72': 'https://a.slack-edge.com/80588/img/plugins/app/service_72.png'
                },
                'team_id': 'T026Z1GC2R0'}
        },
        'warning': 'missing_charset',
        'response_metadata': {'warnings': ['missing_charset']}
    },
    'error': {
        'ok': False,
        'error': 'invalid_error',
        'warning': 'missing_charset',
        'response_metadata': {
            'warnings': ['missing_charset']}
    }
}


class RequestMock:

    def __init__(self, **kwargs):
        self.mode = kwargs.get('mode', 'success')

    def json(self):
        return BOT_RESPONSE[self.mode]
