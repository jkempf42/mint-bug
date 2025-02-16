import azure.functions as func
import datetime
import importlib
import json
import logging

app = func.FunctionApp()

@app.route(route="mint_bug_example", auth_level=func.AuthLevel.ANONYMOUS)
def mint_bug_example(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
            
    if name == "Darth_Vader":

        # Show how dynamic loading caused mint-processed containers to
        # fail.
        module = importlib.import_module("darth_vader")
        return module.enter_darth_vader(name)


    elif name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
