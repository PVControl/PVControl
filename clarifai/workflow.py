from clarifai.rest import ClarifaiApp
from clarifai.rest import Workflow

app = ClarifaiApp(api_key='xxxxxxxx')

workflow = Workflow(app.api, workflow_id="PVControl-WF1")

response = workflow.predict_by_url('https://samples.clarifai.com/metro-north.jpg')
