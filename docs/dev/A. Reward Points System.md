## Reward Points System

The reward point system is very simple, and does not have much complexity. The points app has two models: `PointValue` and `AwardedPoint`. 

- **Point Value** stores a string key and an integer that represents points.
- **Awarded Point** stores data about the awarded points. It stores the targeted user instance, a point_value instance, a reason, a integer that represents points, and a timestamp. 

### Helper Functions

`award_points(target, key, reason="")`

**Parameters**: 

- target - must be an instance of the user model. This is who will be awarded the points.
- key - Can either be an integer or string. If it is an integer, then it will represent that amount of points the user is awarded. If it is a string, then the function will lookup keys in the Point Value table, and get the value that corresponds to the string as the points that will be awarded. 
- reason - reasons for awarding points.

Call this function where you want to award points to a target user. For instance, if you want to award points to users who have favorited an activity, you would call this function after (or before) the user favorites the activity. 

```python
def favorite_item(self, user, item):
    fav = Favorite(user=user, item=item)
    fav_reason = "{0} favorited {1}".format(user.name, item.title)
    award_points(user, 'favorite', reason=fav_reason)
    return fav
```

*Please do not use this example, as it is just an example*

Notice that in the key parameter we used a string. That means there has to be a Point Value record with the 'favorite' key. If there isn't a point value that does not have the key parameter, then no points will be awarded, and the reason will explain why.

`unaward_points(target, key)`

**Parameters**:

- target - must be an instance of the user model. This is who will be unawarded points.
- key - Can either be an integer or string. If it is an integer, then it will represent the amount of points the user is unawarded. If it is a string, then the function will lookup keys in the Point Value table, and get the value that corresponds to the string as the points that will be unawarded.

Call this function where you want to take away points from the target user. This should generally be used if an object that awarded the creator points was deleted by the user. Using the same example above, you would call this function when the user unfavorites an activity.

```python
def unfavorite_item(self, user, item):
    fav = Favorite.objects.get(user=user, item=item)
    fav.delete()
    unaward_points(user, 'favorite')
    return somewhere
```

Notice that we use 'favorite' as the key parameter. It is recommended to keep the key parameter consistent. If you award points for favoriting an item, and it uses the key 'favorite', then unawarding points should also use 'favorite'.

The admin/staff could create Point Value objects in the Django Admin. 

### Example from the project

In the project, when a review is created or deleted, it will either add or remove points respectively from the target user. We done this using signals.

In /reviews/signals.py

```python
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from points.models import award_points, unaward_points
from .models import Review

@receiver(post_save, sender=Review)
def award_points_for_review(sender, instance, created, **kwargs):
    """ Award points when a review is created """
    if created:
        award_points(instance.user, 'review_create')
        # if the review has a photo when created, award points
        if instance.photo:
            award_points(instance.user, 'review_photo')


@receiver(pre_delete, sender=Review)
def unaward_points_for_review(sender, instance, using, **kwargs):
    """ Unaward points when a review is deleted """
    unaward_points(instance.user, 'review_create')

```

When a review is saved, it will send a signal to the `award_points_for_review` method to call. If the review was created, it will reward points to the user. When the review is created, it will also check if a photo was uploaded. 

Same with deleting a review; however, we a signaling the function before it is deleted, so we can access the instance.

Read more about Django Signals:

<https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html>

<https://docs.djangoproject.com/en/2.2/topics/signals/>
