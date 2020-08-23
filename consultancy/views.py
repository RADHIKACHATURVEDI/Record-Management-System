from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
import json
# Create your views here.

def index(request):
    return (render(request,"index.html"))

def register(request):
    return (render(request,"register.html"))



def register_user(request):

    if(request.method=="POST"):
        name = request.POST.get('name')
        phone = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date')
        visit_date = request.POST.get('visit_date')
        investigation = request.POST.get('investigation')
        history = request.POST.get('history')
        advice=request.POST.get("advice")
        follow_up_date=request.POST["follow_up_date"]

        if(len(phone)!=10):
            return redirect("/consultancy/register/",messages.error(request,"phone number must be 10 digits"))
        with open("consultancy/data.json") as f:
            data=json.load(f)
        data["database"].append(
            {
                "name":name,
                "phone_number":phone,
                "date_of_birth":date_of_birth,
                "visit_date":visit_date,
                "history":history,
                "investigation":investigation,
                "follow_up_date":follow_up_date,
                "advice":advice,
                "follow_up":[

                ],
            })
        with open("consultancy/data.json","w") as f:
            json.dump(data,f,indent=2)
        return redirect('/consultancy/register/',messages.info(request,"sucessfully registered"))
    else:
        return HttpResponse("Error 404")



def searchBar(request):
    if(request.method=="POST"):
        var=0
        date_of_birth=request.POST["date_of_birth"]
        name=request.POST["name"]

        if(date_of_birth=="" or name==""):
            return (HttpResponse("Fields Cannot be Empty"))
        
        with open("consultancy/data.json") as f:
            data=json.load(f)

        list_var=[]
        list_follow=[]
        for object in data["database"]:

            if(object["name"]==name and object["date_of_birth"]==date_of_birth):
                if (len(object["follow_up"]) != 0):
                    # list_var.append([object["name"], object["phone_number"],object["follow_up"][len(object["follow_up"])-1]["history"+str(len(object["follow_up"]))],object["date_of_birth"],object["follow_up"][len(object["follow_up"])-1]["investigation"+str(len(object["follow_up"]))],object["follow_up"][len(object["follow_up"])-1]["visit_date"+str(len(object["follow_up"]))],object["follow_up"][len(object["follow_up"])-1]["advice"+str(len(object["follow_up"]))],object["follow_up_date"] ])
                    list_var.append([object["name"], object["phone_number"], object["history"], object["date_of_birth"],object["investigation"], object["visit_date"], object["advice"],object["follow_up_date"]])
                    for i in range(len(object["follow_up"])):
                        list_follow.append([object["follow_up"][i]["visit_date"+str(i+1)],object["follow_up"][i]["investigation"+str(i+1)],object["follow_up"][i]["history"+str(i+1)],object["follow_up"][i]["advice"+str(i+1)]])
                    
                else:
                    list_var.append([object["name"], object["phone_number"], object["history"], object["date_of_birth"],object["investigation"], object["visit_date"], object["advice"],object["follow_up_date"]])

        if(len(list_var)>0):
            var=1

        return(render(request,"search_page.html",{"final_list":list_var,"final_follow_up":list_follow,"var":var,"name":name,"dob":date_of_birth}))
    else:
        follow_up(request)
        var=0
        return render(request,"search_page.html",{"var":var,"name":"","dob":""})

def follow_up(request):
    if(request.method=="POST"):
        visit_date=request.POST.get('visit_date')
        investigation=request.POST.get('investigation')
        history=request.POST.get('history')
        advice=request.POST.get('advice')
        name=request.POST.get("name")
        date_of_birth=request.POST.get("dob")
        follow_up_date=request.POST["follow_up_date"]

        with open("consultancy/data.json") as f:
            data = json.load(f)

        for object in data["database"]:
            if (object["name"] == name and object["date_of_birth"] == date_of_birth):
                object["follow_up_date"]=follow_up_date
                data1=object["follow_up"]
                data1.append({"visit_date"+str(len(object["follow_up"])+1): visit_date,
                              "investigation"+str(len(object["follow_up"])+1):investigation,
                              "history"+str(len(object["follow_up"])+1):history,
                              "advice"+str(len(object["follow_up"])+1):advice})



        with open("consultancy/data.json", "w") as f:
            json.dump(data, f, indent=2)

    return(redirect("/consultancy/index/"))


