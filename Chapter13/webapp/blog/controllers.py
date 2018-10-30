import datetime
from sqlalchemy import func
from flask import (
    render_template,
    Blueprint,
    flash,
    redirect,
    url_for,
    session,
    current_app,
    abort,
    request,
    get_flashed_messages
)
from flask_login import login_required, current_user
from .models import db, Post, Tag, Comment, tags
from .forms import CommentForm, PostForm
from .. import cache
from ..auth.models import User
from ..auth import has_role

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder='../templates/blog',
    url_prefix="/blog"
)


def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    messages = str(hash(frozenset(get_flashed_messages())))
    if current_user.is_authenticated:
        roles = str(current_user.roles)
    else:
        roles = ""
    return (path + args + roles + session.get('locale', '') + messages).encode('utf-8')


@cache.cached(timeout=7200, key_prefix='sidebar_data')
def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(tags).group_by(Tag).order_by('total DESC').limit(5).all()

    return recent, top_tags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
@cache.cached(timeout=60, key_prefix=make_cache_key)
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page,
                                                                   current_app.config.get('POSTS_PER_PAGE', 10),
                                                                   False)
    recent, top_tags = sidebar_data()

    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
@has_role('poster')
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post()
        new_post.title = form.title.data
        new_post.user_id = current_user.id
        new_post.text = form.text.data
        new_post.youtube_id = form.youtube_id.data
        db.session.add(new_post)
        db.session.commit()
        flash('Post added', 'info')
        return redirect(url_for('.post', post_id=new_post.id))
    return render_template('new.html', form=form)


@blog_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    # We want admins to be able to edit any post
    if current_user.id == post.user.id:
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.youtube_id = form.youtube_id.data
            post.text = form.text.data
            post.publish_date = datetime.datetime.now()
            db.session.merge(post)
            db.session.commit()
            flash('Post edited', 'info')
            return redirect(url_for('.post', post_id=post.id))
        form.title.data = post.title
        form.youtube_id.data = post.youtube_id
        form.text.data = post.text
        return render_template('edit.html', form=form, post=post)
    abort(403)


@blog_blueprint.route('/post/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
    form = CommentForm()

    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        try:
            db.session.add(new_comment)
            db.session.commit()
        except Exception as e:
            flash('Error adding your comment: %s' % str(e), 'error')
            db.session.rollback()
        else:
            flash('Comment added', 'info')
        return redirect(url_for('blog.post', post_id=post_id))

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'post.html',
        post=post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags,
        form=form
    )


@blog_blueprint.route('/tag/<string:tag_name>')
@cache.cached(timeout=60, key_prefix=make_cache_key)
def posts_by_tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'tag.html',
        tag=tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_blueprint.route('/user/<string:username>')
@cache.cached(timeout=60, key_prefix=make_cache_key)
def posts_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )
