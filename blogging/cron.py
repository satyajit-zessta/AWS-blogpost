from .models import Comment

from datetime import timedelta,date


def handle():
    two_months_ago = date.today() - timedelta(days=60)
    old_comments = Comment.objects.filter(date__lte=two_months_ago)
    print(old_comments)
    if old_comments:
        old_comments.delete()
        print('Successfully deleted old comments.')
    else:
        print("No old comments found.")

def test():
    print("It's working bro")