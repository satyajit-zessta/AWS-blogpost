from import_export import resources, fields
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget,DateWidget
from .models import User, Post, Tagging, Comment
from datetime import datetime

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class ParseDateField(fields.Field):
    def get_value(self, value, **kwargs):
        if value:
            # Parse the string to DateTimeField
            try:
                # Assuming the date format is "%Y-%m-%d"
                parsed_date = datetime.strptime(value, "%Y-%m-%d")
                return parsed_date
            except ValueError:
                # Handle parsing errors based on your needs
                return None
        else:
            return None
        
class PostResource(resources.ModelResource):

    def after_import_row(self, row, row_result, row_number=None, **kwargs):
        if row_result.original.date is None:
            row_result.original.date = datetime.now().date()

    class Meta:
        model = Post
        export_order = ('id', 'title', 'author', 'content', 'date', 'comments', 'tags')


class TagResource(resources.ModelResource):
    class Meta:
        model = Tagging


# Custom Field for word count
class WordCountField(fields.Field):
    def get_value(self, obj):
        content = obj.content
        if content:
            return len(content.split())
        else:
            return 0


class CommentResource(resources.ModelResource):
    word_count = WordCountField(column_name='word_count', attribute='content', readonly=True)
    date = fields.Field(column_name='date', 
                        attribute='date', 
                        widget=DateWidget(format="%Y-%m-%d"))

    class Meta:
        model = Comment
        export_order = ('id', 'name', 'email', 'post', 'content', 'date', 'word_count')
