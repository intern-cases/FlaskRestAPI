from flask import request, jsonify, abort
from authentication import login_required, user_verifying
from testalch import UserSchema, UserModel, PostSchema, PostModel, CommentSchema, CommentModel, UserPointModel, \
    UserPointSchema, PostPointModel, PostPointSchema, CommentPointModel, CommentPointSchema, Manager, MigrateCommand, \
    db, app, RoleModel, UserRolesModel, NestedCommentSchema
from flask import Blueprint

index_blueprint = Blueprint('index', __name__)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

nested_comments_schema = NestedCommentSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

posts_schema = PostSchema(many=True)
comments_schema = CommentSchema(many=True)

userpoints_schema = UserPointSchema(many=True)
postpoints_schema = PostPointSchema(many=True)
commentpoints_schema = CommentPointSchema(many=True)

"""""""""""""""""""""""""""""""""""USER TABLE ROUTES"""""""""""""""""""""""""""""""""""""""""""""
# user ve admin rollerinin database'e eklenmesi için yazılmış route şu anda user 1 ve admin 2 olarak belirlendi.
@index_blueprint.route("/addroles", methods=["POST"])
def add_roles():
    role_name = request.json["role_name"]
    new_role = RoleModel(role_name)
    db.session.add(new_role)
    db.session.commit()


@index_blueprint.route("/setroles", methods=["PUT"])
@login_required
def set_admin():
    # giriş yapmış kullanıcının admin olup olmadığını ifte kontrol ediyoruz
    # burda admin başka kullanıcıya admin yetkisi verebiliyor.
    user = UserRolesModel.query.filter(user_verifying() == UserRolesModel.user_id).get(UserRolesModel.role_id)
    if user.role_id == 2:
        user_id = request.json["user_id"]
        role_id = request.json["role_id"]
        user = UserRolesModel.query.filter(user_id == UserRolesModel.user_id).first()
        user.role_id = role_id
        db.session.commit()
    else:
        return jsonify("You're not allowed to do this")
    return


# kullanıcı kayit
@index_blueprint.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    role_id = 1
    new_user = UserModel(username, email, password)

    if username is None or password is None or email is None:
        abort(404)  # alanlar boş olamaz
    if UserModel.query.filter(username == UserModel.username or email == UserModel.email).first() is not None:
        abort(404)  # user exist

    db.session.add(new_user)
    db.session.commit()
    new_user_role = UserRolesModel(new_user.user_id, role_id)
    db.session.add(new_user_role)
    db.session.commit()

    return jsonify(new_user)


@index_blueprint.route("/set_points/<string:username>", methods=["POST"])
@login_required
def point_to_user(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    if user_verifying() == user.user_id:
        return jsonify("You can't set points to yourself.")
    else:
        point = request.json["point"]
        if 0 <= int(point) <= 10:
            user_id = user.user_id
            point_user = UserPointModel(user_id, int(point))
            db.session.add(point_user)
            db.session.commit()
            return jsonify(point_user)
        else:
            return jsonify("Giriceğiniz puan 0 ile 10 arasında olmalıdır.")


# user bilgilerini görebildiği panel.
@index_blueprint.route("/user_panel", methods=["GET"])
@login_required
def get_logged_user():
    spesific_user = UserModel.query.filter(user_verifying() == UserModel.user_id).first()
    result = user_schema.dump(spesific_user)
    return jsonify(result)


# tüm userları getir
@index_blueprint.route("/users", methods=["GET"])
@login_required
def get_users():
    all_users = UserModel.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


# idye göre kullanıcı görme
@index_blueprint.route("/user/<int:user_id>", methods=["GET"])
def user_detail(user_id):
    user = UserModel.query.filter(user_id == UserModel.user_id).first()
    result = user_schema.dump(user)
    return jsonify(result)


# kullanıcı adına  göre kullanıcıları görme
@index_blueprint.route("/user/<string:username>", methods=["GET"])
def user_detail_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    result = user_schema.dump(user)
    return jsonify(result)


# kullanıcı adına göre kullanıcıyı güncelleme
@index_blueprint.route("/user/<string:username>", methods=["PUT"])
@login_required
def user_update(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    # login olan kullanıcı sadece kendini update edebilsin diye if state koyulmuştur.
    if user.user_id == user_verifying():
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        user.email = email
        user.username = username
        user.password_hash = password

        db.session.commit()
        return jsonify(user)
    else:
        return jsonify("You're not allowed to do this action.")


# kullanıcı kullanıcı numarasina göre kullanıcı silme
@index_blueprint.route("/user/<int:user_id>", methods=["DELETE"])
@login_required
def user_delete(user_id):
    if user_id == user_verifying():
        user = UserModel.query.filter(user_verifying() == UserModel.user_id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify(user)
    else:
        return jsonify("You're not allowed to do this action.")


# kullanıcı adına göre kullanıcı silme
@index_blueprint.route("/user/<string:username>", methods=["DELETE"])
@login_required
def user_delete_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    if user_verifying() == user.user_id:
        db.session.delete(user)
        db.session.commit()
        return jsonify(user)
    else:
        return jsonify("You're not allowed to do this action.")


"""""""""""""""""""""""""""""""""""POST TABLE ROUTES"""""""""""""""""""""""""""""""""""""""""""""


# kullanıcıya post ekleme
@index_blueprint.route("/post", methods=["POST"])
@login_required
def add_post():
    user_id = user_verifying()
    post_text = request.json["post_text"]
    new_post = PostModel(post_text, user_id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post)


@index_blueprint.route("/set_points_post/<int:post_id>", methods=["POST"])
@login_required
def points_to_post(post_id):
    post = PostModel.query.filter(post_id == PostModel.post_id).first()
    if user_verifying() == post.user_id:
        return jsonify("You can't set points to your post.")
    else:
        point = request.json["point"]
        if 0 <= int(point) <= 10:
            user_id = user_verifying()
            point_post = PostPointModel(user_id, post_id, int(point))
            db.session.add(point_post)
            db.session.commit()
            return jsonify(point_post)
        else:
            return jsonify("Giriceğiniz puan 0 ile 10 arasında olmalıdır.")


@index_blueprint.route("/my_posts", methods=["GET"])
@login_required
def logged_users_post():
    my_post = PostModel.query.filter(PostModel.user_id == user_verifying())
    result = posts_schema.dump(my_post)
    return jsonify(result)


# tüm postları alma
@index_blueprint.route("/main_page", methods=["GET"])
def get_posts():
    all_posts = PostModel.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result)


# kullanıcı idsine göre postları görme
@index_blueprint.route("/post/<int:user_id>", methods=["GET"])
def post_detail(user_id):
    posts = PostModel.query.filter(user_id == PostModel.user_id).all()
    result = posts_schema.dump(posts)
    return jsonify(result)


# kullanıcıya göre postları görme
@index_blueprint.route("/post/<string:username>", methods=["GET"])
def post_detail_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    post = PostModel.query.filter(user.user_id == PostModel.user_id).all()
    result = posts_schema.dump(post)
    return jsonify(result)


# usera bağlı bi postu güncellemek için daha sonra kullanıcı
# o posta sahip olup olmadığıyla ilgili authentication gelicek
@index_blueprint.route("/post/<int:user_id>/<int:post_id>", methods=["PUT"])
@login_required
def post_update(user_id, post_id):
    post = PostModel.query.filter(user_id == PostModel.user_id and post_id == PostModel.post_id).first()
    post_text = request.json["post_text"]

    post.post_text = post_text

    db.session.commit()
    return jsonify(post)


# post silme kullanıcıya bağlı, postu silmek için sonradan authentication eklenicek
@index_blueprint.route("/post/<int:post_id>", methods=["DELETE"])
@login_required
def post_delete(post_id):
    post = PostModel.query.filter(user_verifying() == PostModel.user_id and post_id == PostModel.post_id).first()
    if user_verifying() == post.user_id:
        db.session.delete(post)
        db.session.commit()
        return jsonify(post)
    else:
        return jsonify("You're not allowed to do this action.")


"""""""""""""""""""""""""""""""""""Comment table routes"""""""""""""""""""""""""""""""""""""""""""""


# comment ekleme
@index_blueprint.route("/comment/post<int:post_id>", methods=["POST"])
@login_required
def add_comment_to_post(post_id):
    user_id = user_verifying()
    post = PostModel.query.filter(post_id == PostModel.post_id).first()
    comment_text = request.json["comment_text"]
    parent_id = None
    new_comment = CommentModel(user_id, post.post_id, comment_text, parent_id)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(new_comment)


@index_blueprint.route("/set_points_comment/<int:comment_id>", methods=["POST"])
@login_required
def points_to_comment(comment_id):
    comment = CommentModel.query.filter(comment_id == CommentModel.comment_id).first()
    if user_verifying() == comment.user_id:
        return jsonify("You can't set points to your comment.")
    else:
        points = request.json["points"]
        if 0 <= int(points) <= 10:
            user_id = user_verifying()
            comment_id = comment.comment_id
            point_comment = CommentPointModel(user_id, comment_id, int(points))
            db.session.add(point_comment)
            db.session.commit()
            return jsonify(point_comment)
        else:
            return jsonify("You have to set points between 0 and 10.")


# postun commentlerini update etmek için comment giriş yapmış usera bağlı mı diye kontrol ediliyor.
@index_blueprint.route("/comment/<int:post_id>/<int:comment_id>", methods=["PUT"])
@login_required
def posts_comment_update(post_id, comment_id):
    post = CommentModel.query.filter(post_id == CommentModel.post_id).first()
    comment = CommentModel.query.filter(
        user_verifying() == CommentModel.user_id and CommentModel.post_id == post.post_id).first()
    if user_verifying() == comment.user_id:
        comment_text = request.json["comment_text"]
        comment.comment_text = comment_text
        db.session.commit()
        return jsonify(comment)
    else:
        return jsonify("You're not allowed to do this action.")


# comment silmek için, comment usera bağlı mı kontrol ediliyor.
@aindex_blueprint.route("/comment/delete<int:comment_id>", methods=["DELETE"])
@login_required
def post_comment_delete(comment_id):
    comment = CommentModel.query.filter(comment_id == CommentModel.comment_id).first()
    user_id = comment.user_id
    if user_verifying() == user_id:
        db.session.delete(comment)
        db.session.commit()
        return jsonify(comment)
    else:
        return jsonify("You're not allowed to do this action.")


@index_blueprint.route("/comment/<int:comment_id>", methods=["POST"])
@login_required
def add_comment_to_comment(comment_id):
    user_id = user_verifying()
    post = PostModel.query.filter(user_id == PostModel.user_id).first()
    parent_id = comment_id
    comment_text = request.json["comment_text"]
    comment = CommentModel(user_id, post.post_id, comment_text, parent_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify("Request done.")


@index_blueprint.route("/post<int:post_id>/comments", methods=["GET"])
def get_comments_from_post(post_id):
    all_comments = CommentModel.query.filter(post_id == PostModel.post_id).all()
    if all_comments:
        results = nested_comments_schema.dump(all_comments)
        return jsonify(results)
    else:
        all_comments = CommentModel.query.filter(post_id == CommentModel.post_id).all()
        results = comments_schema.dump(all_comments)
        return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
