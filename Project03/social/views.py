from django.http import HttpResponse,HttpResponseNotFound,Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages

from . import models

def messages_view(request):
    """Private Page Only an Authorized User Can View, renders messages page
       Displays all posts and friends, also allows user to make new posts and like posts
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render private.djhtml
    """
    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)


        # TODO Objective 9: query for posts (HINT only return posts needed to be displayed)
        posts = []
        owners = list(models.Post.objects.order_by('-timestamp'))
        for one in owners:
            posts.append(one)
        try:
            posts = posts[:request.session['anotherCounter']]
        except:
            posts = posts[:request.session.get('anotherCounter',1)]
        #trim = request.session['anotherCounter'] or request.session.get('anotherCounter',1)
        #posts = posts[:trim]
        # TODO Objective 10: check if user has like post, attach as a new attribute to each post
        # boolValues = []
        #fetching = list(models.Post.objects.all())
        # for i in fetching:
        '''
        for j in posts:
            print(j.likes.all())
            print(user_info)
            if user_info in j.likes.all():
                j.boolValue=False
        '''
        # print(boolValues)
        context = { 'user_info' : user_info
                  , 'posts' : posts }
        '''context = { 'user_info' : user_info
                  , 'posts' : posts
                  , 'boolValues' : boolValues }'''
        return render(request,'messages.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def account_view(request):
    """Private Page Only an Authorized User Can View, allows user to update
       their account information (i.e UserInfo fields), including changing
       their password
    Parameters
    ---------
      request: (HttpRequest) should be either a GET or POST
    Returns
    --------
      out: (HttpResponse)
                 GET - if user is authenticated, will render account.djhtml
                 POST - handle form submissions for changing password, or User Info
                        (if handled in this view)
    """
    if request.user.is_authenticated:
        form = None
        # TODO Objective 3: Create Forms and Handle POST to Update UserInfo / Password
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            update = models.UpdateForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save()
                    update_session_auth_hash(request, user)
                    return redirect('social:messages_view')
                except:
                    raise Exception("Something went wrong.")
            if update.is_valid():
                try:
                    user_info = models.UserInfo.objects.get(user=request.user)
                    user_info.employment = request.POST['employment']
                    user_info.location = request.POST['location']
                    user_info.birthday = request.POST['birthday']
                    object, created = models.Interest.objects.get_or_create(label=request.POST['interest'])
                    # print(object)
                    if(created == True):
                        user_info.interests.add(object)
                    else:
                        if object not in user_info.interests.all():
                            user_info.interests.add(object)
                    user_info.save()
                    # print(user_info.interests.all())
                    return redirect('social:messages_view')
                except:
                    raise Exception("Something went wrong.")
        form = PasswordChangeForm(request.user)
        user_info = models.UserInfo.objects.get(user=request.user)
        update = models.UpdateForm(instance=user_info)
        context = { 'user_info' : user_info,
                    'form' : form,
                    'update' : update }
        return render(request,'account.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def people_view(request):
    """Private Page Only an Authorized User Can View, renders people page
       Displays all users who are not friends of the current user and friend requests
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render people.djhtml
    """
    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)
        # TODO Objective 4: create a list of all users who aren't friends to the current user (and limit size)
        all_people = []
        users = models.UserInfo.objects.all()
        friReq = list(models.FriendRequest.objects.all())
        f = list(user_info.friends.all())
        for usert in users:
            if usert not in f:
                if usert.user == request.user:
                    pass
                else:
                    all_people.append(usert)
        bestI=0
        '''anotherFri = list(models.FriendRequest.objects.get(from_user=request.user.id))
        for i in anotherFri:
            all_people.remove(to_user.user)
        '''
        '''for oops in friReq:
            for j in all_people:
                if oops.from_user.user == request.user and oops.to_user.user == j.user:
                    all_people.remove(j)'''
        for isee in friReq:
            for i in all_people:
                if isee.from_user.user == i.user and isee.to_user.user==request.user:
                    all_people.remove(i)
        #m=request.session['counter']
        try:
            m = request.session['counter']
        except:
            m = request.session.get('counter',1)
        all_people = all_people[:m]
        '''except:
            #m = request.session['counter']
            all_people = all_people[:1]'''
        # TODO Objective 5: create a list of all friend requests to current user
        friend_requests = []
        for friend in friReq:
            if friend.to_user.user == request.user:
                friend_requests.append(friend)

        all_requests = []
        for oops in friReq:
            for j in all_people:
                if oops.from_user.user == request.user and oops.to_user.user == j.user:
                    all_requests.append(j)


        context = { 'user_info' : user_info,
                    'all_people' : all_people,
                    'friend_requests' : friend_requests,
                    'all_requests' : all_requests }

        return render(request,'people.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def like_view(request):
    '''Handles POST Request recieved from clicking Like button in messages.djhtml,
       sent by messages.js, by updating the corrresponding entry in the Post Model
       by adding user to its likes field
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute postID,
                                a string of format post-n where n is an id in the
                                Post model

	Returns
	-------
   	  out : (HttpResponse) - queries the Post model for the corresponding postID, and
                             adds the current user to the likes attribute, then returns
                             an empty HttpResponse, 404 if any error occurs
    '''
    postIDReq = request.POST.get('postID')
    # timeAll = request.POST.get('timestamp')
    if postIDReq is not None:
        # remove 'post-' from postID and convert to int
        # TODO Objective 10: parse post id from postIDReq
        postID = postIDReq[5:]
        '''
        users = list(models.UserInfo.objects.all())
        for damn in users:
            if str(damn.user) == str(postID):
                thisIsIt = damn.user'''

        if request.user.is_authenticated:
            try:
                # TODO Objective 10: update Post model entry to add user to likes field
                '''users = list(models.UserInfo.objects.all())
                for damn in users:
                    if str(damn.user) == str(postID):
                        thisIsIt = damn.user'''
                current = models.Post.objects.get(id=postID)
                if request.user.id not in current.likes.all():
                    current.likes.add(request.user.id)
                status='success'
                return HttpResponse()
            except:
                raise Http404
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('like_view called without postID in POST')

def post_submit_view(request):
    '''Handles POST Request recieved from submitting a post in messages.djhtml by adding an entry
       to the Post Model
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute postContent, a string of content

	Returns
	-------
   	  out : (HttpResponse) - after adding a new entry to the POST model, returns an empty HttpResponse,
                             or 404 if any error occurs
    '''
    postContent = request.POST.get('postContent')
    if postContent is not None:
        if request.user.is_authenticated:

            # TODO Objective 8: Add a new entry to the Post model
            #user_info = models.Post.objects.get(owner=request.user)
            try:
                object = models.Post(content = postContent)
                object.owner_id = request.user.id
                object.save()
                '''object.likes.add(0)'''
                # xmodels.Post.objects.create(owner_user=request.user,content=postContent)
                '''models.Post.objects.likes.add(0)
                models.Post.objects.owner_user.add(request.user)'''
                status='success'
                # raise Exception('Working')
                return HttpResponse()
            except:
                raise Http404
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('post_submit_view called without postContent in POST')

def more_post_view(request):
    '''Handles POST Request requesting to increase the amount of Post's displayed in messages.djhtml
    Parameters
	----------
	  request : (HttpRequest) - should be an empty POST

	Returns
	-------
   	  out : (HttpResponse) - should return an empty HttpResponse after updating hte num_posts sessions variable
    '''
    if request.user.is_authenticated:
        # update the # of posts dispalyed

        # TODO Objective 9: update how many posts are displayed/returned by messages_view
        j = request.session.get('anotherCounter',1)
        request.session['anotherCounter']=j+1
        status='success'
        return HttpResponse()

    return redirect('login:login_view')

def more_ppl_view(request):
    '''Handles POST Request requesting to increase the amount of People displayed in people.djhtml
    Parameters
	----------
	  request : (HttpRequest) - should be an empty POST

	Returns
	-------
   	  out : (HttpResponse) - should return an empty HttpResponse after updating the num ppl sessions variable
    '''
    if request.user.is_authenticated:
        # update the # of people dispalyed

        # TODO Objective 4:  increment session variable for keeping track of num ppl displayed
        i = request.session.get('counter',1)
        request.session['counter']=i+1
        status='success'
        #  people_view(request)
        return HttpResponse()

    return redirect('login:login_view')

def friend_request_view(request):
    '''Handles POST Request recieved from clicking Friend Request button in people.djhtml,
       sent by people.js, by adding an entry to the FriendRequest Model
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute frID,
                                a string of format fr-name where name is a valid username

	Returns
	-------
   	  out : (HttpResponse) - adds an etnry to the FriendRequest Model, then returns
                             an empty HttpResponse, 404 if POST data doesn't contain frID
    '''
    frID = request.POST.get('frID')
    if frID is not None:
        # remove 'fr-' from frID
        username = frID[3:]

        if request.user.is_authenticated:
            try:
                # TODO Objective 5: add new entry to FriendRequest
                '''object = models.FriendRequest()
                user_info = models.UserInfo.objects.get(user_id=username)
                object.to_user_id = user_info.id
                object.from_user_id = request.user.id
                object.save()'''
                fri = models.UserInfo.objects.all()
                for okay in fri:
                    # y.user)
                    if str(okay.user) == str(username):
                        please = okay.user
                user_info = models.UserInfo.objects.get(user=request.user)
                # models.FriendRequest.create(to_user=please,from_user=user_info)
                object = models.FriendRequest()
                object.to_user_id = please.id
                object.from_user_id = request.user.id
                object.save()
                status='success'
                return HttpResponse()
            except:
                raise Http404
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('friend_request_view called without frID in POST')

def accept_decline_view(request):
    '''Handles POST Request recieved from accepting or declining a friend request in people.djhtml,
       sent by people.js, deletes corresponding FriendRequest entry and adds to users friends relation
       if accepted
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute decision,
                                a string of format A-name or D-name where name is
                                a valid username (the user who sent the request)

	Returns
	-------
   	  out : (HttpResponse) - deletes entry to FriendRequest table, appends friends in UserInfo Models,
                             then returns an empty HttpResponse, 404 if POST data doesn't contain decision
    '''
    data = request.POST.get('decision')
    if data is not None:
        # TODO Objective 6: parse decision from data
        final = data[2:]
        # print(data[:2])
        if request.user.is_authenticated:
            try:
                # TODO Objective 6: delete FriendRequest entry and update friends in both Users
                if str(data[:2]) == str("A-"):
                    fromUser = list(models.UserInfo.objects.all())
                    for yess in fromUser:
                        if str(yess.user) == str(final):
                            assured = yess.user
                    first = models.UserInfo.objects.get(user_id=assured.id)
                    #print(first.friends.all)
                    first.friends.add(request.user.id)
                    #print(first.friends.all)
                    user_info = models.UserInfo.objects.get(user_id=request.user.id)
                    user_info.friends.add(assured.id)
                    models.FriendRequest.objects.filter(to_user=request.user.id,from_user=assured.id).delete()
                elif str(data[:2]) == str("D-"):
                    another = models.UserInfo.objects.all()
                    for ugh in another:
                        if str(ugh.user) == str(final):
                            please = ugh.user
                    models.FriendRequest.objects.filter(to_user=request.user.id,from_user=please.id).delete()
                else:
                    print("NotWorking")
                status='success'
                return HttpResponse()
            except:
                raise Http404
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('accept-decline-view called without decision in POST')
