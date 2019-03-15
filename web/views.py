import os
from flask import render_template, request, send_from_directory
from web import app, whooshee
from web.models import Workflow
from web.helper import save_workflow, transform, SaveWorkflowException
from config import BASE_DIR


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/workflow/<int:id>', methods=['GET'])
def workflow(id):
    found = Workflow.query.filter_by(id=id).first()
    return render_template("workflow.html", workflow=transform(found))


@app.route('/browse', methods=['GET'])
def browse():
    workflows = Workflow.query.order_by(Workflow.name).all()
    return render_template("browse.html", workflows=workflows)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else:
        info = None
        err = None
        try:
            save_workflow(request)
            info = "save success"
        except SaveWorkflowException as e:
            err = "save error:{}".format(e.msg)
        except Exception as e:
            err = "save error"
            app.logger.exception(e)
        return render_template("upload.html", info=info, err=err)


@app.route('/search', methods=['GET'])
def search():
    name = request.args.get("name", type=str)
    workflows = list()
    if len(name.strip()) != 0:
        if not os.path.exists(os.path.join(BASE_DIR, "workflow")):
            whooshee.reindex()
        found = Workflow.query.whooshee_search(name).all()
        for item in found:
            workflow = dict()
            workflow["name"] = item.name
            workflow["description"] = item.description
            workflow["path"] = "workflow" + "/" + str(item.id)
            workflows.append(workflow)
    return render_template("search.html", workflows=workflows)


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(directory=app.config.get("WORKFLOWS_DIR"), filename=filename)
