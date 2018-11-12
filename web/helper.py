import os
import uuid
from werkzeug import secure_filename
from web.models import Workflow
from web import app, db
import io
import re

ALLOWED_EXTENSIONS = set(['zip'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def save_workflow(request):
    name = request.form.get("name")
    if name is None or name == "":
        error = "{} can't be empty".format("Workflow name")
        raise Exception(error)
    description = request.form.get("description")
    if description is None or description == "":
        error = "{} can't be empty".format("Workflow description")
        raise Exception(error)
    macros = request.form.get("macros")
    print(macros)
    if macros is None or macros == "":
        error = "{} can't be empty".format("")
        raise Exception(error)
    check_macros(macros)
    author = request.form.get("author")
    if author is None or author == "":
        error = "{} can't be empty".format("Author")
        raise Exception(error)
    email = request.form.get("email")
    if email is None or email == "":
        error = "{} can't be empty".format("Email")
        raise Exception(error)
    file = request.files.get('file')
    if file is None:
        error = "{} can't be empty".format("Workflow file")
        raise Exception(error)
    if not allowed_file(file.filename):
        error = "{} is not allowed".format(file.filename)
        raise Exception(error)
    filename = secure_filename(file.filename) + "." + uuid.uuid4().hex
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


def check_macros(macros_string):
    reader = io.StringIO(macros_string)
    pattern = re.compile("[A-Z0-9_]+:.+")
    while True:
        line = reader.readline().strip()
        if not pattern.match(line):
            if line == "":
                break
            raise Exception(" '{}' format error".format(line))


def parse_macros(macros_string):
    macros_dict = dict()
    reader = io.StringIO(macros_string)
    while True:
        line = reader.readline().strip()
        if line == "":
            break
        splits = line.split(":")
        macros_dict[splits[0]] = splits[1]
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


if __name__ == "__main__":
    pass
    print(check_macros("R>: end 1 fastq file input"))
