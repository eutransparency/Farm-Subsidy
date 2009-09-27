from web.comments.models import CommentWithOwner
from web.comments.forms import CommentFormWithOwners

def get_model():
    return CommentWithOwner

def get_form():
    return CommentFormWithOwners
