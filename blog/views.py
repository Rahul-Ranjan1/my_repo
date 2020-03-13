from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import Person, Image, Chat, Box
from django.db.models import Q




from django.conf import settings
import random

# Create your views here.
global otp
global Admin_OTP
global receiver
receiver = ''
global __username__
__username__ = ''

def home(request):
    return render(request, 'html_files/home.html')
def sign_up(request):
    try:
        return render(request, 'html_files/sign_up.html')
    except Exception:
        return HttpResponse('<h1>Email should be unique</h1>')
def forgot(request):
    return render(request, 'html_files/forgot.html')

def button(request):
    return render(request, 'html_files/home.html')
def save_data(request):
    try:
        image = request.FILES['pic_h']
        name = request.POST["Name"]
        
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        business = request.POST["business"]
        bio = request.POST["bio"]
        gender = request.POST["gender"]
        password = request.POST["Password"]

        p = Person(pic = image, name = name, username = username, email = email, phone = phone, address = address, business = business, bio = bio, gender = gender, password = password, BAN = "Allowed")
        p.save()
        
        return render(request, 'html_files/home.html')
    except Exception:
        return HttpResponse('<h1>Username and email should be unique</h1>')
def login(request):
    try:
        global __username__
        username = request.POST["username"]
        password = request.POST["password"]
        obj = Person.objects.filter(username = username)
        
        for a in obj:
            b = a
            break
        if(username == b.username and password == b.password and b.BAN == 'Allowed'):
            __username__ = b.username
            img = Image.objects.all().order_by('-auto')
            return render(request, 'html_files/first_page.html', {'L':img, 's':__username__})
        elif(b.BAN == 'Banned'):
            return HttpResponse('<h1>Person is banned...</h1>')
        else:
            return HttpResponse('<h1>Password is wrong...</h1>')
    except Exception:
        return HttpResponse('<h1>Person not found...</h1>')
    
def send_otp(request):
    try:
        email = request.POST["email"]
        obj = Person.objects.all()
        for a in obj:
            if(a.email == email):
                SUBJECT = 'Hello! Message from Blog Site'
                MESSAGE = random.randint(100000, 999999)
                msg = "We received your login request. \nYour Username : " + a.username + "\nYour OTP : " + str(MESSAGE) + "\nChange your password after login."
                FROM = settings.EMAIL_HOST_USER
                TO = []
                TO.append(email)
                send_mail(SUBJECT, msg, FROM, TO, fail_silently = False)
                global otp
                otp = MESSAGE
                global __email__
                __email__ = email
                global __username__
                __username__ = a.username
                return render(request, 'html_files/otp_check.html', {'L':TO})
            else:
                return HttpResponse('<h1>Email not found...</h1>')
    except Exception:
        return HttpResponse('<h1>Email exception occurred...</h1>')
   
def check_otp(request):
    global otp
    global __username__
    try:
        n = int(request.POST["otp"])
        if(otp == n):
            otp = otp+1
            obj = Image.objects.all().order_by('-auto')
            return render(request, 'html_files/first_page.html', {'L':obj, 's':__username__})
        else:
            __email__ = ""
            otp = otp + 1
            return HttpResponse('<h1>Invalid OTP...OTP changed</h1>')
    except Exception:
        otp += 1
        return HttpResponse('<h1>OTP NOT FOUND error occurred...</h1>')

def first_page(request):
    global __username__
    obj = Image.objects.all().order_by('-auto')
    context = {'L':obj, 's':__username__}
    return render(request, 'html_files/first_page.html', context)

def profile(request):
    obj = Person.objects.all()
    global __username__
    for a in obj:
        if(a.username == __username__):
            p = a
            break
    context = {'p':p, 's':__username__}        
    return render(request, 'html_files/profile.html', context)
def update_data(request):
    try:
        global __username__
        pic = request.FILES["pic_h"]
        name = request.POST["name"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        business = request.POST["business"]
        bio = request.POST["bio"]
        password = request.POST["password"]
        Person.objects.filter(username = __username__).delete()
        p = Person(name = name, username = username, email = email, phone = phone, gender = gender, address = address, business = business, bio = bio, password = password, pic = pic, BAN = 'Allowed')
        p.save()
        __username__ = username
        obj = Image.objects.all().order_by('-auto')
        return render(request, 'html_files/first_page.html', {'L':obj,'s':__username__})
    except Exception:
        msg = '<h1>These problems arise because :<br>a)Email and Username should be unique<br>b)Choose a profile pic.</h1>'
        return HttpResponse(msg)

def make_a_post(request):
    global __username__
    try:
        s = __username__
        img = Image.objects.filter(username = __username__).last()
        context = {'image_file':img.image_file, 's':s}
        return render(request, 'html_files/make_a_post.html', context)
    except Exception:
        s = __username__
        context = {'s':s}
        return render(request, 'html_files/make_a_post.html', context)

def hello(request):
    global __username__
    image = request.FILES['image']
    person = Person.objects.filter(username = __username__)
    for a in person:
        p = a
        break
    
    p = Image(username = p.username, email = p.email, image_file = image, comments = '')
    p.save()
    obj = Image.objects.all().order_by('-auto')
    context = {'L':obj, 's':__username__}
    return render(request, 'html_files/first_page.html', context)

def hello_hello(request):
    global __username__
    obj = Image.objects.all().order_by('-auto')
    s = __username__
    context = {'L':obj, 's':s}
    return render(request, 'html_files/first_page.html', context)

def my_posts(request):
    global __username__
    obj = Image.objects.filter(username = __username__).order_by('-auto')
    context = {'L':obj, 's':__username__}
    return render(request, 'html_files/my_posts.html', context)

def remove_post(request):
    id_ = request.POST['id__']
    Image.objects.filter(auto = id_).delete()
    global __username__
    obj = Image.objects.filter(username = __username__).order_by('-auto')
    context = {'L':obj, 's':__username__}
    return render(request, 'html_files/my_posts.html', context)

def save_comment(request):
    global __username__
    try:
        getAuto = request.POST["id_auto"]
        text = request.POST["text"]
        if(text == '' or text == ' ' or text == '   ' or text == '    ' or text == '\t' or text == '\t\t'):
            raise Exception
        username = __username__
        obj = Image.objects.filter(auto = getAuto)
        for i in obj:
            c = i
            break
        hell = c.comments + "\n"
        hell +=  __username__ + " : " + text + "\n"
        Image.objects.filter(auto = getAuto).update(comments = hell)

        obj = Image.objects.all().order_by('-auto')

        context = {'L':obj, 's':__username__}
        return render(request, 'html_files/first_page.html', context)
    except Exception:
        return HttpResponse('<h1>Text is None Exception...</h1>')

def deactivate(request):
    global __username__
    return render(request, 'html_files/deactivate.html', {'s':__username__})

def delete_account(request):
    global __username__
    toggle = request.GET.get('toggle', None)
    toggle_by = request.GET.get('toggle_by', None)
    chat_toggle = request.GET.get('chat_toggle',None)
    if(toggle is not None):
        if(toggle_by is not None):
            Image.objects.filter(username = __username__).delete()
            Person.objects.filter(username = __username__).delete()
            if(chat_toggle is not None):
                Box.objects.filter(Q(sender = __username__)|Q(receiver = __username__)).delete()
        else:
            Person.objects.filter(username = __username__).delete()
            if(chat_toggle is not None):
                Box.objects.filter(Q(sender = __username__)|Q(receiver = __username__)).delete()
        return render(request, 'html_files/home.html')

def admin_login(request):
    return render(request, 'html_files/admin_login.html')

def admin_requests_otp(request):
    return render(request, 'html_files/admin_requests_otp.html')

def send_Admin_OTP(request):
    global Admin_OTP
    Admin_OTP = random.randint(1000000, 9999999)
    email = request.POST["email"]
    SUBJECT = "Blog Site Admin OTP Request"
    MESSAGE = "\nAdmin we received Forgot Password OTP Request from " + str(email) + " . Is it you?\n" + "Your OTP : " + str(Admin_OTP)
    FROM = settings.EMAIL_HOST_USER
    TO = []
    TO.append(email)
    if(FROM == email):
        send_mail(SUBJECT, MESSAGE, FROM, TO, fail_silently = False)
        return render(request, 'html_files/Admin_OTP_check.html')
    else:
        return HttpResponse('<h1>Your email address does not match.</h1>')

def Admin_OTP_check(request):
    global Admin_OTP
    received_OTP = request.POST["admin_otp"]
    if(Admin_OTP == int(received_OTP)):
        Admin_OTP = 100
        obj = Person.objects.all()
        return render(request, 'html_files/Admin_welcome.html', {'p':obj})
    else:
        Admin_OTP = 100
        return HttpResponse('<h1>Invalid Admin OTP</h1>')

def Admin_welcome(request):
    obj = Person.objects.all()
    return render(request, 'html_files/Admin_welcome.html', {'p': obj})

def admin_login_(request):
    try:
        global __admin__
        admin_name = request.POST["admin_name"]
        admin_pass = request.POST["admin_password"]
        if(admin_name == settings.EMAIL_HOST_USER and admin_pass == settings.EMAIL_HOST_PASSWORD):
            obj = Person.objects.all()
            return render(request, 'html_files/Admin_welcome.html', {'p':obj})
        else:
            return HttpResponse('<h1>Either your email address or password does not match.</h1>')
    except Exception:
        return HttpResponse('<h1>Either your email address or password does not match.</h1>')

def admin_post(request):
    img = Image.objects.all().order_by('-auto')
    return render(request, 'html_files/admin_post.html', {'p':img})

def admin_removes_post(request):
    auto = request.POST["auto"]
    Image.objects.filter(auto = auto).delete()
    img = Image.objects.all().order_by('-auto')
    return render(request, 'html_files/admin_post.html', {'p':img})

def ban_person(request):
    username = request.POST["username"]
    Person.objects.filter(username = username).update(BAN = 'Banned')
    
    p = Person.objects.all()
    return render(request, 'html_files/Admin_welcome.html', {'p':p})


def remove_person(request):
    username = request.POST["username"]
    Person.objects.filter(username = username).delete()
    p = Person.objects.all()
    return render(request, 'html_files/Admin_welcome.html', {'p':p})

def send_mail_page(request):
    username = request.POST['username']
    obj = Person.objects.filter(username = username)
    for a in obj:
        b = a
        break
    
    return render(request, 'html_files/send_mail_page.html', {'p':b})

def send_email_to_person(request):
    try:
        username = request.POST["username"]
        SUBJECT = request.POST["subject"]
        MESSAGE = request.POST["message"]
        person = Person.objects.filter(username = username)
        for a in person:
            b = a
            break
        TO = []
        TO.append(b.email)
        FROM = settings.EMAIL_HOST_USER
        send_mail(SUBJECT, MESSAGE, FROM, TO, fail_silently = False)
        p = Person.objects.all()
        return render(request, 'html_files/Admin_welcome.html', {'p':p})
    except Exception:
        return HtpResponse('<h1>Email exception occured...</h1>')

def allow_person(request):
    username = request.POST["username"]
    Person.objects.filter(username = username).update(BAN = 'Allowed')
    p = Person.objects.all()
    return render(request, 'html_files/Admin_welcome.html', {'p':p})


def friends(request):
    global __username__
    
    p = Person.objects.all()
    return render(request, 'html_files/friends.html', {'p':p, 's':__username__, 'L':[10, 20, 33, 43]})

def profile_of_person(request):
    global __username__
    global them
    username = request.POST["username"]
    
    obj = Person.objects.filter(username = username)
    for a in obj:
        b = a
        them = a.username
        break
    ob = Person.objects.filter(username = __username__)
    for i in ob:
        s = i
        break
    return render(request, 'html_files/profile_of_person.html', {'s':s, 'p':b})

def group_chat(request):
    global __username__
    obj = Person.objects.filter(username = __username__)
    for a in obj:
        s = a
        break
    cmg = Chat.objects.all()
    text = ''
    for i in cmg:
        text += i.username + " : " + i.chat + "\n"
    return render(request, 'html_files/group_chat.html', {'s':s, 'text':text})

def save_group_chat(request):
    global __username__
    message = request.POST["message"]
    c = Chat(username = __username__, chat = message)
    c.save()
    cmg = Chat.objects.all()
    text = ''
    for i in cmg:
        text += i.username + " : " + i.chat + "\n"
    obj = Person.objects.filter(username = __username__)
    for a in obj:
        s = a
        break
    return render(request, 'html_files/group_chat.html',{'s':s, 'text':text})


def box_chat(request):
    global __username__
    global receiver
    obj = Person.objects.filter(username = __username__)
    for a in obj:
        b = a
        break
    rec = request.POST["username"]
    
    obj2 = Person.objects.filter(username = rec)
    for a in obj2:
        c = a
        receiver = a.username
        break
    text = Box.objects.filter((Q(sender__exact = __username__)&Q(receiver__exact = receiver))|(Q(receiver__exact = __username__)&Q(sender__exact = receiver))).order_by('auto')
    msg = ''
    for a in text:
        msg += "\n" + a.sender + " : " + a.chat
    Box.objects.filter(Q(receiver = __username__)&Q(sender = rec)&Q(notification = 1)).update(notification = 0)
    return render(request, 'html_files/messenger.html', {'s':b, 'p':c, 'message':msg})


def box_chat_save(request):
    global __username__
    global receiver
    obj = Person.objects.filter(username = __username__)
    for a in obj:
        b = a
        break
    obj2 = Person.objects.filter(username = receiver)
    for a in obj2:
        c = a
        break
    msg = request.POST["message"]
    B = Box(sender = __username__, receiver = receiver, chat = msg, notification = 1)
    B.save()
    text = Box.objects.filter((Q(sender__exact = __username__)&Q(receiver__exact = receiver))|(Q(sender__exact = receiver)&Q(receiver__exact = __username__))).order_by('auto')
    message = ''
    for a in text:
        message += "\n" + a.sender + " : " + a.chat
    return render(request, 'html_files/messenger.html', {'s':b, 'p':c, 'message' : message})


def notify(request):
    global __username__
    obj = Person.objects.filter(username = __username__)
    for a in obj:
        b = a
        break
    box = Box.objects.filter(Q(receiver = __username__)&Q(notification = 1)).order_by('-auto')
    context = {'s':b, 'box':box}
    return render(request, 'html_files/notifications.html', context)

def remove_notification(request):
    global __username__
    obj = Person.objects.filter(username = __username__)
    for a in obj:
        b = a
        break
    msg = request.POST["msg"]
    auto = request.POST["auto"]
    Box.objects.filter(Q(receiver = __username__)&Q(sender = msg)&Q(auto = auto)&Q(notification = 1)).update(notification = 0)
    box = Box.objects.filter(Q(receiver = __username__)&Q(notification = 1)).order_by('-auto')
    context = {'s':b, 'box':box}
    return render(request, 'html_files/notifications.html', context)

def notify_box_chat(request):
    global __username__
    global receiver
    obj1 = Person.objects.filter(username = __username__)
    for a in obj1:
        b = a
        break
    rec = request.POST["msg"]
    
    obj2 = Person.objects.filter(username = rec)
    for a in obj2:
        c = a
        receiver = a.username
        break
    text = Box.objects.filter((Q(sender__exact = __username__)&Q(receiver__exact = receiver))|(Q(sender__exact = receiver)&Q(receiver__exact = __username__)))
    msg = ''
    for n in text:
        msg += '\n' + n.sender + " : " + n.chat
    context = {'s':b, 'p':c, "message" : msg}
    Box.objects.filter(Q(receiver = __username__)&Q(sender = rec)&Q(notification = 1)).update(notification = 0)
    return render(request, 'html_files/messenger.html', context)


def remove_all(request):
    global __username__
    obj = Person.objects.filter(username = __username__)
    for a in obj:
        b = a
        break
    Box.objects.filter(Q(receiver = __username__)&Q(notification = 1)).update(notification = 0)
    box = Box.objects.filter(Q(receiver = __username__)&Q(notification = 1)).order_by('-auto')
    context = {'s':b, 'box':box}
    return render(request, 'html_files/notifications.html', context)












