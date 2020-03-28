## Django Notes
1- We can Replace a function that checks if ```request.method == 'POST'``` with a class based view and we define a function called ```def post(self,request,any_key_if_exist)```
and instead of putting the code related to the get method in the else we can define get method in the class so we have both get and post methods in the class

2- we can inherit from ```TemplateResponseMixin``` to get the function ```render_to_response``` and we can use it inside any function of the class
by writing ```self.render_to_response(context)``` it take a dictionary that contains the data to render inside the page

3- The ```as_view()``` that is called in the url file all what it do is it call the ```def dispatch(self,request,*args,**kwargs)``` which checks
the type of the request done (post,get,put) and invoke the corresponding function in the class,
 if the function is not found an ```http_mehtod_not allowed``` exception will be thrown, The function implementation is as follow:
 ```python
class View:
    http_method_names = [u'get  ',u'post',u'put',u'patch',u'delete',u'head',u'option',u'trace']
    # when we call View.as_view() it calls the following function
    def dispatch(self,request,*args,**kwargs):
        if request.method.lower() in self.http_method_names:
        #getattr() method invoke the corresponding method to the method type used, if the method type is not found an exception is thrown
            handler = getattr(self,request.method.lower(),self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request,*args,**kwargs)

```
 
4- we can switch between views based on the http method request used for example
```python
class SwitchboardView(generic.View):
    def get(self,request,pk):
        view = ResultView.as_view()
        return view(request,pk)
    def post(self,request,pk):
        view = VoteView.as_view()
        return view(request,pk)
```
by doing this previous part we will avoid putting 2 paths in the url file one for each view and they will be replaced by just 1 path.


5- Instead of using login_required witht class based views (CBV's) function in the url file we can do the following:
```python

class RequireLoginMixin:
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated():
            return  redirect_to_login(request.get_full_path())
        return super(RequireLoginMixin,self).dispatch(request,*args,**kwargs)
``` 
then we can inherit the RequireLoginMixin class by doing so the child class will have the login required functionality.
 
6- Authentication in Django Rest Framework (DRF) 
```python
from django.contrib.auth import authenticate
from rest_framework import authentication
from rest_framework import exceptions

class AdminOnlyAuth(authentication.BaseAuthentication):
    def authenticate(self,request):
        try:
            username = request.query_params.get('username')
            password = request.query_params.get('password')
            user = authenticate(username=username,password=password)
            if user is None or user.is_superuser():
                raise exceptions.AuthenticationFailed('No such user')
            # we return user and None, this none replace permessions class
            return (user,None)
        except:
            raise exceptions.AuthenticationFailed('No such user')
```
7- In order to add authentication to your rest api you should create a class as in point 6 then add the following code into ```setting.py```
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':(
    'path to the AdminOnlyAuth class',   
)
}
```
