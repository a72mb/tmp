from flask_restful import Resource, reqparse
from login_sqlalchemy.models.users import User
from login_sqlalchemy.models import shared

db = shared.db


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return {"id": user.id, "username": user.username, "email": user.email}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, help="Username cannot be blank!")
        parser.add_argument("email", required=True, help="Email cannot be blank!")
        args = parser.parse_args()
        new_user = User(username=args["username"], email=args["email"])  # type: ignore
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created", "id": new_user.id}, 201
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200