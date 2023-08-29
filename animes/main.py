from flask import Blueprint, request, render_template, make_response, abort
from . import db
from .models import Anime, User
import os
from flasgger import swag_from
from .auth import login_required

main = Blueprint("main", __name__)
secret = os.environ["FLASK_SECRET_KEY"]


@main.route("/profile")
@swag_from("apidocs/profile.yaml")
@login_required
def profile():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        print(auth_header.split(" ")[0])
        auth_token = auth_header.split(" ")[0]
    else:
        auth_token = ""
    if auth_token:
        resp = User.decode_auth_token(auth_token, secret)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            return {
                "status": "success",
                "data": {"user_id": user.id, "email": user.email},
            }, 200
        return {"status": "fail", "message": resp}, 401
    else:
        return {
            "status": "fail",
            "message": "Invalid token, please provide a valid one",
        }, 401


@main.route("/")
@swag_from("apidocs/base.yaml")
def index():
    return render_template("base.html")


@main.route("/all")
@swag_from("apidocs/all.yaml")
@login_required
def all():
    listing = []
    for i in Anime.query.order_by(Anime.Anime_ID).limit(100):
        result = {
            "Anime_ID": i.Anime_ID,
            "Name": i.Name,
            "Genre": i.Genre,
            "Type": i.Type,
            "Episodes": i.Episodes,
            "Rating": i.Rating,
            "Members": i.Members,
        }
        listing.append(result)
    return listing, 200


@main.route("/anime/<string:name>")
@swag_from("apidocs/get_anime.yaml")
@login_required
def list(name):
    listing = []
    look_for = "%{0}%".format(name)
    anime = Anime.query.filter(Anime.Name.contains(look_for))
    if anime.first():
        for i in anime:
            output = {
                "Anime_ID": i.Anime_ID,
                "Name": i.Name,
                "Genre": i.Genre,
                "Type": i.Type,
                "Episodes": i.Episodes,
                "Rating": i.Rating,
                "Members": i.Members,
            }
            listing.append(output)
    else:
        output = "error: Anime with Name = " + str(name) + " not found."
        abort(404, description=output)

    return listing, 200


@main.route("/anime/add/<int:anime_id>", methods=["POST"])
@swag_from("apidocs/add_anime.yaml")
@login_required
def add(anime_id):
    listing = []

    if anime_id is None:
        listing.append("Please enter an Anime ID")
        return listing, 201

    name = request.args.get("name")
    genre = request.args.get("genre")
    type = request.args.get("type")
    episodes = request.args.get("episodes")
    rating = request.args.get("rating")
    members = request.args.get("members")

    result = Anime.query.filter_by(Anime_ID=anime_id).first()

    if result:
        print("already exists")
        message = "Anime with Anime_ID: " + str(anime_id) + " already exists."
        listing.append(message)
        return listing, 201
    else:
        new_anime = Anime(
            Anime_ID=anime_id,
            Name=name,
            Genre=genre,
            Type=type,
            Episodes=episodes,
            Rating=rating,
            Members=members,
        )
        db.session.add(new_anime)
        db.session.commit()
        new_result = Anime.query.filter_by(Anime_ID=anime_id).first()
        output = {
            "Anime_ID": new_result.Anime_ID,
            "Name": new_result.Name,
            "Genre": new_result.Genre,
            "Type": new_result.Type,
            "Episodes": new_result.Episodes,
            "Rating": new_result.Rating,
            "Members": new_result.Members,
        }
        listing.append(output)

    return listing, 200


@main.route("/anime/update/<int:anime_id>", methods=["PATCH"])
@swag_from("apidocs/update_anime.yaml")
@login_required
def update(anime_id):
    listing = []

    if anime_id is None:
        listing.append("Please enter an Anime ID")
        return listing, 201

    name = request.args.get("name")
    genre = request.args.get("genre")
    type = request.args.get("type")
    episodes = request.args.get("episodes")
    rating = request.args.get("rating")
    members = request.args.get("members")

    result = Anime.query.filter_by(Anime_ID=anime_id).first()

    if result:
        result.Name = name if name is not None else result.Name
        result.Genre = genre if genre is not None else result.Genre
        result.Type = type if type is not None else result.Type
        result.Episodes = episodes if episodes is not None else result.Episodes
        result.Rating = rating if rating is not None else result.Rating
        result.Members = members if members is not None else result.Members

        db.session.commit()

        new_result = Anime.query.filter_by(Anime_ID=anime_id).first()
        output = {
            "Anime_ID": new_result.Anime_ID,
            "Name": new_result.Name,
            "Genre": new_result.Genre,
            "Type": new_result.Type,
            "Episodes": new_result.Episodes,
            "Rating": new_result.Rating,
            "Members": new_result.Members,
        }
        listing.append(output)
    else:
        message = (
            "Anime with Anime ID: "
            + str(anime_id)
            + " does not exist. Please include an existing Anime ID."
        )
        listing.append(message)
        return listing, 201

    return make_response(listing), 200


@main.route("/anime/delete/<int:anime_id>", methods=["DELETE"])
@swag_from("apidocs/delete_anime.yaml")
@login_required
def delete(anime_id):
    listing = []

    if anime_id is None:
        listing.append("Please enter an Anime ID")
        return listing, 201

    result = Anime.query.filter_by(Anime_ID=anime_id).first()

    if result:
        db.session.delete(result)
        db.session.commit()
        message = (
            "Anime with Anime ID: " + str(anime_id) + " has been deleted from the DB."
        )
        listing.append(message)
    else:
        message = (
            "Anime with Anime ID: "
            + str(anime_id)
            + " does not exist. Please include an existing Anime ID."
        )
        listing.append(message)
        return listing, 201

    return listing, 200
