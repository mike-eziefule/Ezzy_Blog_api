from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from schema.models import Blogs
from fastapi import Depends
from service.Blog_services import reusables_codes

client = TestClient(app)

def test_get_all_articles(db:Session = Depends(reusables_codes.get_db)):
    response = client.get("/view_all")
    assert response.status_code == 200
    assert response.type == dict
