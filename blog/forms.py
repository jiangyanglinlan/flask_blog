from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SubmitField,
    BooleanField,
    SelectField,
    ValidationError,
    HiddenField,
)
from wtforms.validators import DataRequired, Length, Email

from .models import Category


class LoginForm(FlaskForm):
    '''
    登录表单
    '''
    username = StringField('账号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


class CategoryForm(FlaskForm):
    '''
    分类表单
    '''
    name = StringField('分类名', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField('提交')

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('分类名已经存在')


class PostForm(FlaskForm):
    '''
    文章表单
    '''
    title = StringField('标题', validators=[DataRequired(), Length(1, 100)])
    category = SelectField('分类', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CommentForm(FlaskForm):
    '''
    评论表单
    '''
    author = StringField('昵称', validators=[DataRequired(), Length(1, 30)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 254)])
    body = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('评论')


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()


class SettingForm(FlaskForm):
    name = StringField('名字', validators=[DataRequired(), Length(1, 20, message='长度在 1 到 20 之间')])
    blog_title = StringField('博客标题', validators=[DataRequired(), Length(1, 50, message='长度在 1 到 50 之间')])
    blog_sub_title = StringField('博客副标题', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('关于', validators=[DataRequired()])
    submit = SubmitField('提交')