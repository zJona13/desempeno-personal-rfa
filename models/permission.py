from .db import db

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    module = db.Column(db.String(50), nullable=False)  # Which module this permission belongs to
    
    def __repr__(self):
        return f'<Permission {self.name}>'