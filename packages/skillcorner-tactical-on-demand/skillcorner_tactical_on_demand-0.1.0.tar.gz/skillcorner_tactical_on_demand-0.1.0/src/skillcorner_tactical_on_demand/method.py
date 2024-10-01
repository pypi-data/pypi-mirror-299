from fitrequest.method_generator import RequestMethod

METHOD_DOCSTRING = (
    'Retrieve response from {endpoint} GET request. '
    'To learn more about it go to: https://tactical.skillcorner.com/api/docs/#{docs_url_anchor}.'
)


METHODS_BINDING = [
    {
        'name': 'get_all_requests',
        'endpoint': '/api/requests/',
        'docs_url_anchor': 'requests',
    },
    {
        'name': 'get_request',
        'endpoint': '/api/request/{}',
        'docs_url_anchor': 'request',
        'resource_name': 'request_id',
    },
    {
        'name': 'get_match_sheet',
        'endpoint': '/api/request/{}/match-sheet/',
        'docs_url_anchor': 'match_sheet',
        'resource_name': 'request_id',
    },
    {
        'name': 'post_match_sheet',
        'endpoint': '/api/request/{}/match-sheet/',
        'docs_url_anchor': 'match_sheet',
        'resource_name': 'request_id',
        'request_method': RequestMethod.post,
    },
    {
        'name': 'get_period_limits',
        'endpoint': '/api/request/{}/period-limits/',
        'docs_url_anchor': 'period_limits',
        'resource_name': 'request_id',
    },
    {
        'name': 'post_period_limits',
        'endpoint': '/api/request/{}/period-limits/',
        'docs_url_anchor': 'period_limits',
        'resource_name': 'request_id',
        'request_method': RequestMethod.post,
    },
    {
        'name': 'get_home_team_side',
        'endpoint': '/api/request/{}/home-team-side/',
        'docs_url_anchor': 'home_team_side',
        'resource_name': 'request_id',
    },
    {
        'name': 'post_home_team_side',
        'endpoint': '/api/request/{}/home-team-side/',
        'docs_url_anchor': 'home_team_side',
        'resource_name': 'request_id',
        'request_method': RequestMethod.post,
    },
    {
        'name': 'get_data_collection',
        'endpoint': '/api/match/{}/data_collection/',
        'docs_url_anchor': 'data_collection',
        'resource_name': 'match_id',
    },
    {
        'name': 'get_tracking',
        'endpoint': '/api/match/{}/tracking/',
        'docs_url_anchor': 'tracking',
        'resource_name': 'match_id',
    },
    {
        'name': 'get_match_data',
        'endpoint': '/api/match/{}/',
        'docs_url_anchor': 'match_data',
        'resource_name': 'match_id',
    },
]
