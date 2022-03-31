# The Strong Social

## Usage:

In order to run this project, one must download **CONDA**. It is recommended to install the *Anaconda Distribution* (which will include **conda**) to **manage installing one's python packages (including *Django*)**.

For further details visit [Anaconda Documentation](https://docs.anaconda.com/anaconda/install/).

One can run the project locally with the following command:
```
   python manage.py runserver localhost:8000
```

One can also run the project on **mac1xa3.ca** with the following command:
```
   python manage.py runserver localhost:10047
```
For immediate uses, one can log into the system with the following credentials:

**username**: TestUser
**password**: 1234

## Objective 1 : Complete Login and SignUp Pages

**Page URL:** 
 - [Login Webpage](https://mac1xa3.ca/e/jainy3/)
 - [Signup Webpage](https://mac1xa3.ca/e/jainy3/signup/)

**Desciption:** The main pupose of this objective is to make a new entry in the **UserInfo** model manually from the shell and to create a **Signup** form for the users willing to create a new account.

The following points will give an elaborate explanation of what is going on the back-end:
 - When the user clicks the **Create An Account** button, the webpage redirects to the **Signup Page** which is displayed in **signup.djhtml** which is rendered by **signup_view** fucnction in views.py (which is in login directory).
  - The function accpets **GET** and **POST** requests. If the request is **GET**, the in-built form for **Signup Page** known as **UserCreationForm** is called and then the function displays the signup form on the webpage.
 - If the request is **POST**, then the function first checks if the form is valid or not, if valid fetches the data entered by the user and creates a **UserInfo** object. After that, if the entries are authenticated and successfully registered, the function automatically log the user in and redirects the user to the [Messages Webpage](https://mac1xa3.ca/e/jainy3/social/messages/).
 - Creation of an **UserInfo** object:
```python
   models.UserInfo.objects.create_user_info(username=username, password=raw_password)
```

**Exceptions:** 
 - If the user enters anything wrong/invalid or makes a mistake while entering the data in both of the forms then the page will just reload, that means it will redirect the user to the page the user was currently on. 
 - If the user enters anything wrong/invalid in the **Login Page**, then the person won't be successfully logged-in and if the user enters anything wrong/invalid in the  **Signup Page**, then the person won't be redirected to the [Messages Webpage](https://mac1xa3.ca/e/jainy3/social/messages/). 

## Objective 2 : Adding User Profile and Interests

**Desciption:** The main purpose of this objective is to display the **username** of the currently logged-in user and also display the information related to the user such as **employment, location, birthday, and interests**.

The following points will give an elaborate explanation of what is going on the back-end:
 - The template which displays all this information is called as **social_base.djhtml** which also renders the **left_column** used by **messages.djhtml, people.djhtml, and account.djhtml**.
 - The **social_base.djhtml** file uses the **user_info** object to display the specific information with the help of **Django Template Variables**, where **user_info** is an object from the **UserInfo** model corresponding to the currently logged-in user.
 - To display the interests, we use **for** loop and iterate it over **user_info.interests.all**.
 ```html
    <!-- Interests -->
    <div class="w3-card w3-round w3-white w3-hide-small">
        <div class="w3-container">
            <p>Interests</p>
            <p>
                <!-- TODO Objective 2: Add Currently Logged In User Interests -->
                {% for i in user_info.interests.all %}
                    <span class="w3-tag w3-small w3-theme-d5">{{ i.label }} </span>
                {% endfor %}
            </p>
        </div>
    </div>
    <br>
 ```
**Exceptions:**
 - If the currently logged-in user is unauthenticated, then the user is redirected to the **Login page**.


## Objective 3 : Account Settings Page

**Page URL:** 
[Account Webpage](https://mac1xa3.ca/e/jainy3/social/account/)

**Desciption:** The main purpose of this objective is to be able to change the currently logged-in user's *password* and to be able to update currently logged-in user's information such as *employment, location, birthday, interests (each interest submission adds to the list of current interests).*

The following points will give an elaborate explanation of what is going on the back-end:
 - In order to display the information update form, a new class known as **UpdateForm** is created in models.py (which is in the social directory).
```python
    class UpdateForm(forms.ModelForm):
        interest = forms.CharField(max_length=30,required=False)
        class Meta:
            model = UserInfo
            fields = ['employment','location','birthday']
```
 - The following **GET** or **POST** requests are handeled by the **account_view** function in views.py (which is in the social directory).
 - If it is a **GET** request, then the fucntion bascially displays both of the forms on the webpage. If the user is authenticated, the function will render **account.djhtml** file. There is no need of creating a **PasswordChnageForm** as it is already available by doing specific imports.
 - If it is a **POST** request, then the function first checks whether the **PasswordChangeForm** is valid or not. If valid then fetches the record and changes the *password*. 
 - Then the function checks whether the **UpdateForm** is valid or not. If valid, then the function fetches the data entered by the currently logged-in user and stores it in the respective fields for that specifc user (which is the currently logged-in user) in the **UserInfo** model. By this the user can either update the information or add new information.
 - Interests are handeled differently, there is a seperate model for interests know as **Interest** model which stores all the previously or newly entered interests (no interest is repeated in this model). If the interest entered doesn't exist in the **Interest** model, it then creates one and also adds in the *interests* dataset of the **UserInfo** model of that specific user. If the interest entered is already in the **Interest** model then it checks whether that specific interest is in the *interests* dataset of the **UserInfo** model of that specific user. If it doesn't exist then it adds that specific interest to the *interests* dataset of the **UserInfo** model of that specific user.
 ```python
    object, created = models.Interest.objects.get_or_create(label=request.POST['interest'])
    if(created == True):
        user_info.interests.add(object)
    else:
        if object not in user_info.interests.all():
            user_info.interests.add(object)
 ```

 **Exceptions:**
  - If the user is unauthenticated, then the user is redirected to the **Login Page**.
 - If the user types any data wrong/invalid in the **Password Change Form**, then the function just reloads implying that the password has **not** changed. If the user enters everything correctly, then the user is redirected to the *Messages Webpage*.
 - If the user types any data wrong/invalid in the **User Information Update Form**, then the function just reloads implying that the information has **not** added/updated. If the user enters everything correctly, then the user is redirected to the *Messages Webpage*.

## Objective 4 : Displaying People List

**Page URL:** 
[People Webpage](https://mac1xa3.ca/e/jainy3/social/people/)

**Desciption:** The main purpose of this objective is to display different users who are **not** friends of the currently logged in user.

The following points will give an elaborate explanation of what is going on the back-end:
 - Currently there is only a single entry in the suggested friend's list, in order to load more entries, the user has to click the **More** button which will load a single entry per single click. The amount of people displayed is reset when the user logs out.
  - The **More** button sends an *AJAX POST* from **people.js** file to **/e/jainy3/social/moreppl/** where the the fucntion **more_ppl_view** keeps tracks of the session variable.
```python
   i = request.session.get('counter',1)
   request.session['counter']=i+1
```
  - The feature is displayed in **people.djhtml** (which is in templates directoy which is in the social directory) which is rendered by **people_view** function in views.py (which is in the social directory).
  - After successfull executon of the function, the page reloads and the desired output is attained. 

  **Exceptions:** 
   - If the currently logged-in user is unauthenticated, then the user is redirected to the **Login page**.
   - If the *AJAX POST* response is a faliure, then the fucntion in javascript (**morePplResponse**) ouputs an error message.


## Objective 5 : Sending Friend Requests

**Page URL:** 
[People Webpage](https://mac1xa3.ca/e/jainy3/social/people/)

**Desciption:** The main purpose of this objective is to send friend requests from the account of the currently logged-in user to the account of the desrired user.

The following points will give an elaborate explanation of what is going on the back-end:
 - The Friend Request button sends an *AJAX POST* from **people.js** file to **/e/jainy3/social/friendrequest/**  where the *AJAX POST* sends the **id** of the button which is customized in respect to the username of the user to whom the friend request is sent in the following format: **fr-username**. The **id** sent is handled by the function **friend_request_view**
 in the views.py ( which is in the social directory).
 - The **friend_request_view** function fetches the data sent in the form of *JSON*, and trims it in order to restore the username of the user to whom the friend request is sent. The fucntion then creates an entry in the **FriendRequest** Model where *to_user_id* is the *id* of the user to whom the request is sent and *from_user_id* is the *id* of the currently logged-in user. On success, the function finally returns an empty **HttpResposnse**.
 ```python
    object = models.FriendRequest()
    object.to_user_id = please.id
    object.from_user_id = request.user.id
    object.save()
 ```
 **NOTE:** The word **please** in the above code is an object of *UserInfo* class which corresponds to the user to whom the request is sent.
 
 - In order to avoid the confusion in the database, the fucntion **people_view** in the views.py (which is in the social directory)
 removes those users from the suggested friend list by checking if the *from_user* is the user who is being displayed in the suggested friend list and *to_user* is the currently logged-in user.
 ```python
    for isee in friReq:
        for i in all_people:
            if isee.from_user.user == i.user and isee.to_user.user==request.user:
                all_people.remove(i)
 ```
**NOTE:** *friReq* is a list of all the entries in the **FriendRequest** Model and *all_people* is the list of those users who are to displayed in the suggested friend list.
 - The button is disabled after successfully sending the friend request.
 - In order to Accept/Decline the friend request, the fucntion **people_view** creates a list of those people who sent the request to the currently logged-in user and displayes it on the **people.djhtml** (which is in templates directoy which is in the social directory) file which is rendered by the **people_view** function.
 ```python
    for friend in friReq:
        if friend.to_user.user == request.user:
            friend_requests.append(friend)
 ```
 **NOTE:** The *friend_requests* is the list which contains the user which is to be dispalyed and *firReq* is a list of all the entries in the **FriendRequest** Model.

 **Exceptions:**
 - If the currently logged-in user is unauthenticated, then the user is redirected to the **Login page**.
 - If the *AJAX POST* response is a faliure, then the fucntion in javascript (**frResponse**) ouputs an error message.
 - Returns a **Http404** error, if the **POST** data doesn't contain frID.

 ## Objective 6 : Accepting/Declining Friend Requests

 **Page URL:** 
[People Webpage](https://mac1xa3.ca/e/jainy3/social/people/)

**Desciption:** The main purpose of this objective is to accpet or decline the friend request sent to the currently logged-in user.

The following points will give an elaborate explanation of what is going on the back-end:
 - The Friend Requests displayed in **Objective 5** contain *Accept* and *Decline* buttons. Each button's **id** is customized to the following format: **A-username** if the user accepts the request and **D-username** if the user declines the request., where *username* is the username of the user who sent the friend request.
 - Each button is linked to the function **acceptDeclineRequest** in **people.js** which fetches the button's *id* and stores it in a *JSON* data and makes an AJAX POST call to **/e/jainy3/social/acceptdecline/** where the function **accept_decline_view** deals with the following *JSON* data.
 ```javascipt
    function acceptDeclineRequest(event) {
    let whicheverID = event.target.id;
    let data = {'decision' : whicheverID};
    let url = accept_decline_url;
    $.post(url,
           data,
           function(data)
           {
           location.reload();
           });
    } 
 ```
 - The function **accept_decline_view** in views.py (which is in social directory) fetches the *JSON* data and trims it in order to restore the username of the user who sent the friend request. 
 - If the currently logged-in user has accepted the friend request, then the function adds the corresponding user to the friends data to both of the respective users. After successfully accepting the request, the corresponding entry which included both of the users(*to_user* and *from_user*) in the **FriendRequest** model is deleted.
 - If the currently logged-in user has declined the friend request, then the fucntion deletes the corresponding entry of both of the users (*to_user* and *from_user*) in the **FriendRequest** model.

**Exceptions:**
 - If the currently logged-in user is unauthenticated, then the user is redirected to the **Login page**.
 - Returns a **Http404** error, if the **POST** data doesn't contain decision.

 ## Objective 7 : Displaying friends

 **Page URL:** 
[Social/Messages Webpage](https://mac1xa3.ca/e/jainy3/social/messages/)

**Desciption:** The main purpose of this objective is to display the users who are friends of the currently logged-in used.

The following points will give an elaborate explanation of what is going on the back-end:
 -  The fucntion is displayed in **messages.djhtml** (which is in templates directory which is in social directory) which is rendered by **messages_view** fucntion in views.py.
 - In the template (*messages.djhtml*), the friends of the currently logged in user are outputted by running a **for** loop inside the template which iterates over the **user_info.friends.all**. 
```html
      {% for obj in user_info.friends.all %}
      <div class="w3-card w3-round w3-white w3-center">
        <div class="w3-container">
          <p>Friend</p>
          {% load static %}
          <img src="{% static 'avatar.png'  %}" alt="Avatar" style="width:50%"><br>
          <br>
          <span>{{ obj.user }}</span>
        </div>
      <br>
      </div>
      <br>
      {% endfor %}
```

**Exceptions:**
 - If the currently logged-in user is unauthenticated, then the user is redirected to the **Login page**.

## Objective 8 : Submitting Posts

**Page URL:** 
[Social/Messages Webpage](https://mac1xa3.ca/e/jainy3/social/messages/)

**Desciption:** The main purpose of this objective is to be able to submit a post by the currently logged-in user and handle the output of the respective submitted post.

The following points will give an elaborate explanation of what is going on the back-end:
 - The top of the middle column of the *Messages Webpage* contains a *text field* in which the user will wrtie the contents of the post.
 - The **Post** button is linked to the function **submitPost** in **messages.js** (which is in static directory which is in social directory) file. The function **submitPost** sends an *AJAX POST* which contains the *content of the post in JSON format* to **/e/jainy3/social/postsubmit/** where the function **post_submit_view** in views.py handels the data sent.
 ```javascript
    function submitPost(event) {
    let url = post_submit_url;
    let form = $(this);
    let postData = document.getElementById("post-text").outerText;
    data = {"postContent":postData};
    $.post(url,
           data,
           function(data)
           {
               location.reload();
           });
}
 ```
 - The function **post_submit_view** in views.py fetches the data received in *JSON* format. The fetched data is the *content of the post*.
 - The function then creates a new entry for the currently logged-in user in the **Post** model.
 ```python
    object = models.Post(content = postContent)
    object.owner_id = request.user.id
    object.save()
 ```
  - The page reloads after successfully submitting the post into the database.

**Exceptions:**
 - If the currently logged-in user is unauthenticated, then the user is redirected to the **Login page**.
 - Returns a **Http404** error, if any error occurs.


## Objective 9 : Displaying Post List

**Page URL:** 
[Social/Messages Webpage](https://mac1xa3.ca/e/jainy3/social/messages/)

**Desciption:** The main purpose of this objective is to display the submitted posts of all the users (doesn't matter if they are friends or not) in the *Social/Messages Webpage* of the currently logged-in user.

The following points will give an elaborate explanation of what is going on the back-end:
 - Currently there is only a single post on the *Messages Webpage*, in order to load more posts, the user has to click the **More** button which will load a another post per single click. The amount of posts displayed is reset when the user logs out, leaving only a single post to display.
  - The **More** button sends an *AJAX POST* from **messages.js** file to **/e/jainy3/social/morepost/** where the the fucntion **more_post_view** keeps tracks of the session variable.
  ```python
    j = request.session.get('anotherCounter',1)
    request.session['anotherCounter']=j+1
  ```
  - The feature is displayed in **messages.djhtml** (which is in templates directoy which is in the social directory) which is rendered by **messages_view** function in views.py (which is in the social directory).
  - The **messages_view** function in views.py sorts the entries in the post model according to the **timestamp** in decreasing order, so that the posts are displayed from newest to oldest.
 ```python
   owners = list(models.Post.objects.order_by('-timestamp'))
 ```
 - In **messages.djhtml** file, the posts are displayed by **looping** over the *list of posts* rendered by the **messages_view** function.
  - After successfull executon of the function, the page reloads and the desired output is attained.

**Exceptions:**
 - If the currently logged-in user is unauthenticated, then the user is redirected to the **Login page**.
 - If the *AJAX POST* response is a faliure, then the fucntion in javascript (**moreResponse**) ouputs an error message.


## Objective 10 : Liking Posts

**Page URL:** 
[Social/Messages Webpage](https://mac1xa3.ca/e/jainy3/social/messages/)

**Desciption:** The main purpose of this objective is to be able to **like** the post of different users (including the posts submitted by the currently logged-in user) displayed on the **Messages Webpage** by the currently logged-in user. *No user can like a post more than one time.*

The following points will give an elaborate explanation of what is going on the back-end:
 - Each **like** button's *id* is customized in the following format: **post-ID**, where *ID* is the unique ID given by the system to every entry stored in the **Post** model.
 - Each **like** button is also linked to the function **submitLike** in **messages.js** which fetches the *id* of the corresponding button and stores it in the format of *JSON* data. On clicking the button, the function  sends an **AJAX POST** to **/e/jainy3/social/like/** where the function **like_view** in views.py fetches the data received in the form of *JSON* data.
```javascript
   function submitLike(event) {
    let url = like_post_url;
    let likes = event.target.id;
    let data = {'postID':likes};
    $.post(url,
           data,
           function(data)
           {
           location.reload();
           });
}
```
 - After fetching the data in the function **like_view** in views.py, the data is trimmed in order to restore the *unique ID*. By the help of this *unique ID*, we will be able to identify which *post* is liked in the **Post** model.
 - The function then fetches the record from the **Post** model which corresponds to that specific *unique ID* and adds the *id* of the currently logged-in user to the *likes* dataset, if and only if the currently logged-in *user's id* is **not** present in the likes dataset of that specific *post* entry.
 ```python
    current = models.Post.objects.get(id=postID)
    if request.user.id not in current.likes.all():
        current.likes.add(request.user.id)
 ```
 - In order to disbale the **like** button we do *if* statements in the **messages.djhtml** file, so that no user can like the post more than one time.
 ```html
    {% if user_info in post.likes.all %}
        <button type="button" class="w3-button w3-theme-d1 w3-margin-bottom like-button" id="post-{{ post.id }}" disabled>
            <i class="fa fa-thumbs-up"></i> Like</button>
        <span class="w3-button w3-theme-d1 w3-margin-bottom">{{ post.likes.count }} Likes</span>
    {% else %}
        <button type="button" class="w3-button w3-theme-d1 w3-margin-bottom like-button" id="post-{{ post.id }}">
             <i class="fa fa-thumbs-up"></i> Like</button>
        <span class="w3-button w3-theme-d1 w3-margin-bottom">{{ post.likes.count }} Likes</span>
    {% endif %}
 ```

 **Exceptions:**
  - If the currently logged-in user is unauthenticated, then the user is redirected to the **Login page**.
  - Returns a **Http404** error, if any error occurs.

## Objective 11 : Create a Test Database

**Desciption:** The main purpose of this objective is to create a variety of test users, create many posts and likes and different friend requests to showcase all the functionality implemented in this project.

The following table has credentials of some users registered in the database:

Username | Password
-------- | ---------
kween    |  interesting2002
newUser    |  okur2002#
Veronica    |  iamthequeen101
David101    |  ieatnothing@
VictoriaIsTheB  |  ieatchanel
GossipGirl    |  youknowyouloveme
SerenaVanDerWoodsen |  youknowyouloveme
BlairWaldorf  |  imakemoney999
NickiMinaj  |  money999
prettySweet  |  123qwe##
madisson  |  queerEnergy
charmi  |  stormiMerchIsOut2020
