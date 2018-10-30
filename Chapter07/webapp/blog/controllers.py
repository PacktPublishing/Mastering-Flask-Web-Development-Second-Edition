import datetime
from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort
from flask_login import login_required, current_user
from .models import mongo, Post, Comment

from .forms import CommentForm, PostForm
from ..auth.models import User
from ..auth import has_role

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder='../templates/blog',
    url_prefix="/blog"
)


def sidebar_data():
    recent = Post.objects.limit(5).all()
    top_tags = []
    #top_tags = db.session.query(
    #    Tag, func.count(tags.c.post_id).label('total')
    #).join(tags).group_by(Tag).order_by('total DESC').limit(5).all()

    return recent, top_tags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.objects.paginate(page, current_app.config.get('POSTS_PER_PAGE', 10))
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
        post = Post()
        post.title = form.title.data
        post.user = current_user.id
        post.text = form.text.data
        post.save()
        flash('Post added', 'info')
        return redirect(url_for('.post', post_id=post.id))
    return render_template('new.html', form=form)


@blog_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.objects.get(id=id)
    # We want that the current user can edit is own posts
    if current_user.id == post.user.id:
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.datetime.now()
            post.update()
            return redirect(url_for('.post', post_id=post.id))
        form.title.data = post.title
        form.text.data = post.text
        return render_template('edit.html', form=form, post=post)
    abort(403)


@blog_blueprint.route('/post/<post_id>', methods=('GET', 'POST'))
def post(post_id):
    form = CommentForm()

    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        current_post = Post.objects.get(id=post_id)
        current_post.comments.append(new_comment)
        try:
            current_post.save()
        except Exception as e:
            flash('Error adding your comment: %s' % str(e), 'error')
        else:
            flash('Comment added', 'info')
        return redirect(url_for('blog.post', post_id=post_id))

    post = Post.objects.get(id=post_id)
    tags = post.tags
    comments = post.comments
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
def posts_by_tag(tag_name):
    posts = Post.objects(tags=tag_name)
    #tag = Tag.query.filter_by(title=tag_name).first_or_404()
    #posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'tag.html',
        tag=tag_name,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_blueprint.route('/user/<string:username>')
def posts_by_user(username):
    user = User.objects(username=username).first()
    posts = Post.objects(user=user).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )
