from .views import ReviewViewSet, CommentViewSet
from rest_framework import router


router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet)



