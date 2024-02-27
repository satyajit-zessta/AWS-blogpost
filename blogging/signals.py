from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import pre_init, pre_save, pre_delete, post_init, post_save, post_delete,m2m_changed
from django.contrib.auth.models import User as Admin
from blogging.models import Comment,Post
from .email import sendEmail
from django.dispatch import receiver

    
@receiver(post_save ,sender=Comment)
def at_ending_save(sender, instance,created ,**kwargs):
    print("Triggered for email",'****'*3)
    name = instance.name.capitalize()
    posts = instance.post.all()
    date = instance.date
    content = instance.content

    for post in posts:
        post_title = post.title.title()
        author = (post.author.first_name).title()
        author_email = post.author.email

        sendEmail(email=author_email, author_name=author, commentor=name, title=post_title, date=date, content=content)
        
    
@receiver(m2m_changed, sender=Post.tags.through)
def tags_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    print("m2m_triggered")
    instance.tags_count = instance.tags.count()
    instance.save()