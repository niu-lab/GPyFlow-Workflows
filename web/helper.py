import os
import uuid
from werkzeug import secure_filename
from web.models import Workflow
from web import app, db
import io
import re

ALLOWED_EXTENSIONS = set(['zip'])
MACRO_PATTERN = re.compile("[A-Z0-9_]+:.+")


class SaveWorkflowException(Exception):
    def __init__(self, msg):
        self.msg = msg


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def save_workflow(request):
    name = request.form.get("name")
    if name is None or name == "":
        error = "{} can't be empty".format("Workflow name")
        raise SaveWorkflowException(error)
    description = request.form.get("description")
    if description is None or description == "":
        error = "{} can't be empty".format("Workflow description")
        raise SaveWorkflowException(error)
    macro_names = request.form.getlist("macro-name")
    macro_values = request.form.getlist("macro-value")
    if len(macro_values) != len(macro_names):
        error = "macro name and macro value not match"
        raise SaveWorkflowException(error)
    macros_io = io.StringIO()
    for i in range(len(macro_names)):
        macro = "{name}:{value}".format(name=macro_names[i],
                                        value=macro_values[i])
        if not MACRO_PATTERN.match(macro):
            error = "macro name:{} error".format(macro_names[i])
            raise SaveWorkflowException(error)
        macros_io.write(macro + os.linesep)
    macros = macros_io.getvalue()
    macros_io.close()
    author = request.form.get("author")
    if author is None or author == "":
        error = "{} can't be empty".format("Author")
        raise SaveWorkflowException(error)
    email = request.form.get("email")
    if email is None or email == "":
        error = "{} can't be empty".format("Email")
        raise SaveWorkflowException(error)
    file = request.files.get('file')
    if file is None:
        error = "{} can't be empty".format("Workflow file")
        raise SaveWorkflowException(error)
    if not allowed_file(file.filename):
        error = "{} is not allowed".format(file.filename)
        raise SaveWorkflowException(error)
    dir_name = uuid.uuid4().hex
    workflow_dir = os.path.join(app.config["WORKFLOWS_DIR"], dir_name)
    if not os.path.exists(workflow_dir):
        os.mkdir(workflow_dir)
    filename = os.path.join(dir_name, "{}.zip".format(name))
    file.save(os.path.join(app.config["WORKFLOWS_DIR"], filename))

    workflow = Workflow(name=name,
                        description=description,
                        macros=macros,
                        author=author,
                        email=email,
                        path=filename
                        )
    db.session.add(workflow)
    db.session.commit()


def parse_macros(macros_string):
    macros_dict = dict()
    reader = io.StringIO(macros_string)
    while True:
        line = reader.readline().strip()
        if line == "":
            break
        splits = line.split(":")
        macros_dict[splits[0]] = "".join(splits[1:])
    return macros_dict


def transform(found):
    if not found:
        return None
    workflow = dict()
    workflow["name"] = found.name
    workflow["description"] = found.description
    workflow["macros"] = parse_macros(found.macros)
    workflow["author"] = found.author
    workflow["email"] = found.email
    workflow["path"] = found.path
    return workflow
