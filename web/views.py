import os
from flask import render_template, request, send_from_directory
from web import app
from web.models import Workflow
from web.helper import save_workflow, transform


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
            info = "Save success"
        except Exception as e:
            err = "Sava error,{}".format(e.args)
        return render_template("upload.html", info=info, err=err)


@app.route('/search', methods=['GET'])
def search():
    name = request.args.get("name")
    found = Workflow.query.filter(Workflow.name.like("%{}%".format(name))).all()
    workflows = list()
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
