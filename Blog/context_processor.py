from Blog.models import Profile

def friend_count(request):
    if request.user.is_authenticated:
        pr = Profile.objects.get(user=request.user)
        pr_image = pr.image
        name = []
        for fr in pr.user_friend.all():
            name.append(fr.username)
        
        friend_num = pr.friend_req.all().exclude(username__in=name).count()
        return {'pic':pr_image,'friend_num':friend_num}
    return {}

