import pytest

from osa.globals import  response

def test_basic_route(api):
    @api.route("/hom2e")
    def home():
        response.text = "YOLO" 
           
    @api.route("/home2")
    def home2():
        response.text = "YOLO"
    
def test_duplicate_route_throws_exception(api):
    @api.route("/home2")
    def home2():
        response.text = "YOLO"  
    
    # Test that the method will raise an exception error 
    with pytest.raises(AssertionError):
        @api.route("/home2")
        def home2():
            response.text = "YOLO"


def test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @api.route("/hey", methods=["GET"])
    def cool():
        response.text = RESPONSE_TEXT
    print(client.get("http://testserver/hey").text)
    assert client.get("http://testserver/hey").text == RESPONSE_TEXT

def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello( name):
        response.text = f"hey {name}"

    assert client.get("http://testserver/osama").text == "hey osama"
    assert client.get("http://testserver/man").text == "hey man"
    
def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")

    assert response.status_code == 404
    
    
def test_class_based_handler_get(api,client):
    txt = "YOLO"
    @api.route("/home", methods=["GET"])
    class Home:
        def get(self):
            response.text = txt
    assert client.get("http://testserver/home").text == txt
    
    
def test_class_based_handler_post(api,client):
    txt = "YOLO"
    @api.route("/home", methods=["POST"])
    class Home:
        def post(self):
            response.text = txt
        
    assert client.post("http://testserver/home").text == txt
    
def test_class_based_handler_not_allowed(api,client):
    @api.route("/testClass")
    class testClass:
        def post(self):
            response.text = "POST"
    res = client.get("http://testserver/testClass")
    assert res.status_code == 405
    
