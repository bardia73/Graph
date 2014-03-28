from django.db import models
import datetime
from django.utils import timezone
import json

class Vertex(models.Model,object):
    password = models.CharField(max_length=50)
    user_id = models.CharField(max_length=100)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=75)
    tel = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    sex = models.BooleanField() # 1 for male  // 0 for female
    birthdate = models.DateField()
    reg_date = models.DateTimeField('date published')
    #statues = models.CharField(max_length=30)
    #varificationCode = models.models.CharField(max_length=50)
    
    def get_followers(self): # a person => you
    	followers_list = []
    	for edge in Edge.objects.filter(vertex_head_id =self.user_id):
	    	followers_list += Vertex.objects.filter(user_id = edge.vertex_tail_id)
    	return followers_list
    	
    def get_following(self): # you => a person
    	followings_list = []
    	for edge in Edge.objects.filter(vertex_tail_id =self.user_id):
    		followings_list += Vertex.objects.filter(user_id = edge.vertex_head_id)
    	return followings_list
    
	def is_connected_to(self,vertex_id): # you => vertex_id ???
		if len(Edge.objects.filter(vertex_tail_id = self.user_id , vertex_head_id = vertex_id)) == 0:
			return False
		else:
			return True
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.firstname+' '+self.lastname
        
class Edge(models.Model,object): 
	""" tail ==> head """
	vertex_head_id = models.CharField(max_length=100)
	vertex_tail_id = models.CharField(max_length=100)
	def __unicode__(self):  # Python 3: def __str__(self):
		return self.vertex_tail_id+' ==> '+self.vertex_head_id
    
class Flow(models.Model): 
    vertexes = models.ManyToManyField(Vertex)
    text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')
    history = models.TextField(null=True)
    def set_history(self,to_vertex):
        jsonDec = json.decoder.JSONDecoder()
        try:
            history_list = jsonDec.decode(self.history)
            history_list.append(to_vertex)
        except TypeError:
            history_list=list(to_vertex)
            
        self.history = json.dumps(history_list)
        self.save()
    def get_history(self):
        jsonDec = json.decoder.JSONDecoder()
        history_list = jsonDec.decode(self.history)
        return history_list
    
    def __unicode__(self):
        return self.text

	
# Create your models here. 

