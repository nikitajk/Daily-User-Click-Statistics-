from flask import Flask, jsonify, json, abort
import requests


app = Flask(__name__)

@app.errorhandler(400)
def bad_request_error(error):
    """
    function to handle bad request error
    """
    return jsonify({'message': 'Bad Request'})

@app.errorhandler(403)
def forbidden_access_error(error): 
    """
	function to forbidden access error
	"""
    return jsonify({'message': 'Please provide correct access token'})

@app.errorhandler(404)
def page_not_found_error(error):
    """
	function to page not found error
    """
    return jsonify({'message': 'Page Not Found'})

@app.errorhandler(500)
def internal_error(error):
    """
	 function to internal error exception

	 """
    return jsonify({'message': 'Internal Error'})

@app.errorhandler(503)
def temporarily_unavailable(error):
    """
	 function to handle page temporarily unavailable exception

	 """
    return jsonify({'message': 'Page is temporarily_unavailable'})

@app.route('/getMetric/', methods=["GET"])
def get_clicks_by_country():
    """
	 function to return required json output containing average number of clicks, per country, within the last 30 days.

	 """
    
    url = "https://api-ssl.bitly.com/v4/user"    
    access_token="" #  update access_token variable with appropriate value
#    Example:  access_token="jkenviuernh"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer "+ access_token
        }
    links = []
    resp = {'facet':'countries', 'links':links,'unit':1, 'units': 'month'}
    get_user = requests.request("GET", url, headers=headers)
    
#    If URL is not correct
    if get_user.text.strip()=="404 page not found":
        abort(404)
    json_data = json.loads(get_user.text)
    
#    If user cannot be authenticated
    if 'message' in json_data:
    	if json_data['message']=="FORBIDDEN":
            abort(403)

    group_id =  json_data['default_group_guid']
    url = "https://api-ssl.bitly.com/v4/groups/"+group_id+"/bitlinks"
    get_bitlinks = requests.request("GET", url, headers=headers)
    json_data = json.loads(get_bitlinks.text)

#    If there are no Bitlinks created by the User
    if not json_data or json_data['links']==[]:
        resp['links']='No bitlinks found for default group'
        return jsonify(resp)

    bitlinks = json_data['links']
    for j in bitlinks:
        link_data = {}
        link_data['link'] = j['link']
        click_by_country="https://api-ssl.bitly.com/v4/bitlinks/"+j['id']+"/countries?unit=month&units=1"
        get_click_by_country = requests.request("GET", click_by_country, headers=headers)
        json_click_by_country = json.loads(get_click_by_country.text)
        click_by_country_metrics=json_click_by_country['metrics']

#        If there no clicks by the user for the respective link
        if not click_by_country_metrics or click_by_country_metrics==[]:
            link_data['metrics']='No metrics as of yet for this link'
            links.append(link_data)
            continue
        clicklist = []
        for c in click_by_country_metrics:
            clickDict = {
            'value': c['value'],
            'clicks': c['clicks']}
            clicklist.append(clickDict)
        link_data['metrics']=clicklist
        links.append(link_data)
    data  = jsonify(resp)
    return data



if __name__=="__main__":
    app.run(debug=True)
