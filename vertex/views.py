from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from vertex.models import Vertex,Edge,Flow
from django.utils import timezone
from login.views import authDetail

   
def profile(request, user_id):

	try:
		vertex = Vertex.objects.get(user_id=user_id)       
	except :
		return render_to_response('404error.html',{},context_instance=RequestContext(request))	
	
	auth = authDetail(request)
	me = False
	if auth[0]:
		client = auth[1]
		if client.user_id == vertex.user_id:
			me = True
	else:
		client = None
			
	flows = vertex.flow_set.order_by('-last_forward_date')[:5]
	heOrShe = "He" if vertex.sex else "She"
	if client:
		following = vertex in client.get_following()
	else:
		following = False
	#
	if me:
		return render_to_response('vertex.html',
{"VERTEX_DETAIL":"Yourself"                         ,"VERTEX_ID":user_id, "FOLLOWING_VERTEX":vertex.get_following(), "FOLLOWER_VERTEX":vertex.get_followers(),"flows":flows,"COUNTRY":vertex.country , "CITY":vertex.city,"phone":vertex.tel,"email":vertex.email,"Gender":heOrShe,"BIRTHDAY":vertex.birthdate,"AGE": vertex.age(),"login":client!=None },
context_instance=RequestContext(request))
	else:
		return render_to_response('vertex.html',
{"VERTEX_DETAIL":vertex.firstname.capitalize()+' '+vertex.lastname.capitalize(),"VERTEX_ID":user_id,"FOLLOWING_VERTEX":vertex.get_following() , "FOLLOWER_VERTEX":vertex.get_followers(),"flows":flows,"COUNTRY":vertex.country , "CITY":vertex.city,"phone":vertex.tel,"email":vertex.email ,"Gender":heOrShe,"BIRTHDAY":vertex.birthdate,"AGE": vertex.age(),"login":client!=None,"following":following },
context_instance=RequestContext(request))	
	return HttpResponse("You're looking at vertex %s." % vertex)

def postflow(request):
	useremail = request.POST['id']
	vertex = Vertex.objects.get(email =useremail)
	user_id = vertex.user_id

	#useremail = request.POST['USER_EMAIL']
	flow_text = request.POST['flow_text']
	pub_date = timezone.now()
	newflow = Flow.objects.create(text = flow_text,pub_date = timezone.now(),last_forward_date = timezone.now(),owner = user_id)
	#vertex = Vertex.objects.get(user_id = user_id)
	newflow.set_history(vertex.user_id)
	newflow.save()
	vertex.flow_set.add(newflow)
	vertex.save()
	followers_list = vertex.get_followers()
	for followers in followers_list:
		followers.flow_set.add(newflow)
		followers.save()

	response = HttpResponseRedirect('/home/')
	return response 	
    #gotta add others too
    
    
def forward(request,user_id,flow_id):
    #flow_text = request.POST['flow_text']
    #forward_to = request.POST['forward_to']
	flow = Flow.objects.get(id = flow_id)
	flow.last_forward_date = timezone.now()
	flow.save()
	vertex = Vertex.objects.get(user_id = user_id)
	forward_to = "all"
	if forward_to == "all":
		followers_list = vertex.get_followers()
		for followers in followers_list:
			followers.flow_set.add(flow)
			followers.save()
	else:
		forward_list = [] #I'll change it later with the html
		for index,followers in enumerate(forward_list):
			follower = Vertex.objects.get(user_id = followers)
			follower.flow_set.add(flow)
			follower.save()
            
        
    
def like_flow(request,liker_id):
	flow_text = request.POST['flow_text']
	flow = Flow.objects.get(text = flow_text)
	flow.like(liker_id)
	flow.save()



# Create your views here.
