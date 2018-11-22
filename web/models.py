from web import whooshee, db


@whooshee.register_model('name', 'description')
class Workflow(db.Model):
    __tablename__ = 'workflow'
    # 表的结构:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.TEXT, nullable=False)
    description = db.Column(db.TEXT)
    macros = db.Column(db.TEXT)
    author = db.Column(db.TEXT, nullable=False)
    email = db.Column(db.TEXT, nullable=False)
    path = db.Column(db.TEXT, nullable=False)

    def __repr__(self):
        return '<id:{id}>,<name:{name}>,<path:{path}>'.format(id=self.id,
                                                              name=self.name,
                                                              path=self.path)
