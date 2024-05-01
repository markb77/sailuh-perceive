
#views.py
from loginapp.forms import *
from loginapp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from random import sample
import logging 
log = logging.getLogger(__name__)

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    
 
    return render(request,'registration/register.html', {'form':form})
 
def register_success(request):
    return render_to_response('registration/success.html')
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
@csrf_protect
def home(request):
	if request.user.is_authenticated():
		#retrieve a start session or create new
		if request.method == 'POST':
			log.debug(request.POST)
		error_msg = ''
	        session_count = Session_log.objects.filter(user=request.user,session_action='_start').count()
		
		user_content_count = UserConsent.objects.filter(user=request.user).count()
		if user_content_count > 0:
			user_content = UserConsent.objects.filter(user=request.user)[user_content_count - 1]
		click_count = []
		#all_threads = EmailThread.objects.raw('SELECT DISTINCT title FROM loginapp_emailthread' )
		all_threads = EmailThread.objects.order_by('title').values_list('title', flat=True).distinct()
		all_threads_count = sum(1 for result in all_threads)
		random_int = sample(range(0,all_threads_count),1)
        	rtitle = [obs for (i,obs) in enumerate(all_threads) if i in random_int]
		
	
		thread_emails = EmailThread.objects.filter(title = rtitle)
		all_emails = EmailThread.objects.all()
		rthread = str(rtitle)
		#remail = sample([e1,e2],1)[0]
		source_doc = "This is the first knowledge source created for this session"
		ks = KnowledgeSource.objects.create(source_doc=source_doc)
		
		
		if session_count == 0:
			session = Session_log.objects.create(user = request.user, session_action = '_start')  				
			user_content = UserConsent.objects.create(user=request.user,email_thread=rthread,knowledge_source=ks,session=session)			
			for t in thread_emails:
				var_click = Click_log.objects.filter(user=request.user,session=session, for_email = t.parent_email).count()
				click_count.append(var_click)			 
		else:
			log_session = Session_log.objects.filter(user=request.user).latest('time_action')
			if log_session.session_action == '_end':	
				if request.method == 'POST' and 'end-survey' in request.POST:
					error_msg = 'This session has already ended. Logout and login to start a new session'
					session = log_session
					user_content_count = UserConsent.objects.filter(user=request.user,session=session)
					user_content = UserConsent.objects.get(user=request.user,session=session)
					current_thread = user_content.email_thread
					#thread_emails = EmailThread.objects.filter(title = current_thread)
					rtitle = user_content.email_thread
					#rtitle[0].replace("u'","")
					#rtitle[0].replace("'","")
					
					thread_emails = EmailThread.objects.filter(title = rtitle)
					for t in thread_emails:
						click_count.append(Click_log.objects.filter(user=request.user,session=session, for_email = t.parent_email).count())
				else:
					session = Session_log.objects.create(user = request.user, session_action = '_start')					
					user_content = UserConsent.objects.create(user=request.user,email_thread=rthread,knowledge_source=ks,session=session)
					for t in thread_emails:
						click_count.append(Click_log.objects.filter(user=request.user,session=session,for_email = t.parent_email).count())					
				
			else:
				session = log_session
				user_content_count = UserConsent.objects.filter(user=request.user,session=session).count()			
				
				if user_content_count > 0:
					user_content = UserConsent.objects.filter(user=request.user,session=session)
				else:
					user_content = UserConsent.objects.create(user=request.user,email_thread=rthread,knowledge_source=ks,session=session)
				current_thread = user_content.email_thread
				rtitle = user_content.email_thread
				#rtitle[0].replace("u'","")
				#rtitle[0].replace("'","")
				
				thread_emails = EmailThread.objects.filter(title = rtitle)
				#thread_emails = EmailThread.objects.filter(title = current_thread)
				for t in thread_emails:
					click_count.append(Click_log.objects.filter(user=request.user,session=session, for_email = t.parent_email).count())	

				#elif request.method == 'POST' and 'end-session' in request.POST:
		if request.method == 'POST' and 'end-survey' in request.POST:
			check_session = Session_log.objects.filter(user=request.user).latest('time_action')
			if check_session.session_action == '_start':
				Session_log.objects.create(user = request.user, session_action = '_end') 
				#start = check_session.time_action
				q1 = ''
				if 'knowledge_source_relation' in request.POST:
					q1 = request.POST['knowledge_source_relation']
				q2 = ''
				if 'subject_relation' in request.POST:
					q2 = request.POST['subject_relation']
				q2_extended = ''
				if 'subject_list' in request.POST:
					q2_extended = request.POST['subject_list']
				q3 = ''
				if 'association_reason' in request.POST:
					q3 = request.POST['association_reason']
				q4 = ''
				if 'uncertain' in request.POST:
					q4 = request.POST['uncertain']
				q4_extended = ''
				if 'uncertain_yes' in request.POST:
					q4_extended = request.POST['uncertain_yes']
				
				
				s_response = Survey_response.objects.create(q1 = q1, q2 = q2,q2_extended = q2_extended,q3= q3, q4= q4,q4_extended = q4_extended)
				Survey.objects.create(session = check_session, survey_response = s_response,  timestamp_survey_start =request.POST['start_survey'])

			else:
				error_msg = 'This session has already ended. Logout and login to start a new session'

		elif request.method == 'POST' and 'hide_show' in request.POST:
			
			i = 1
			for t in thread_emails:
				#t.parent_email
				log.debug(request.POST['idisp_email'])
				if 'disp_email' in request.POST and int(request.POST['idisp_email']) == int(i) :
					show_count = int(request.POST['disp_email'])
					log.debug(show_count)
					show_count = Click_log.objects.filter(user = request.user,session = session,for_email = t.parent_email).count()
					show_count += 1
					if(show_count%2 == 0):
						show_action = "_show"
					else:
						show_action = "_hide"
					cl = Click_log.objects.create(user = request.user,session = session, click_action = show_action, for_email = t.parent_email)
					break				
				i = i + 1

		elif request.method == "POST" and 'height_change' in request.POST:        
			i = 1
			box_height = []
			box_width = []
			for t in thread_emails:
				if 'bheight' in request.POST  :
					var_htname = request.POST.get('bheight')
					var_wname = request.POST.get('bwidth')
				
					bl = Box_log.objects.create(user = request.user,session = session, width = var_wname,height = var_htname, for_email = t.parent_email)
					box_height.append(var_htname)
					box_width.append(var_wname)
				else:
					bl_count = Box_log.objects.filter(user = request.user,session = session, for_email = t.parent_email).count()
					#bl = Box_log.objects.filter(user = request.user,session = session, for_email = t.parent_email).order_by(id).reverse()[bl_count -1]
					bl = Box_log.objects.filter(user = request.user,session = session, for_email = t.parent_email)[bl_count -1]
					box_height.append(bl.height)
					box_width.append(bl.width)
					
				i = i + 1
			
        		#thread_title = thread_emails[0].title
			thread_count = thread_emails.count()
			return render(request,'home.html',{'user': request.user,'all_emails':all_emails, 'session':session, 'thread_title': rtitle, 'thread_emails':thread_emails,'thread_count':thread_count,'click_count':click_count, 'error_msg':error_msg,'box_height': box_height,'box_width':box_width, 'ks':ks})
		

		elif request.method == "POST" and 'scroll_change' in request.POST:
			i = 1
			scroll_positions = []
			for t in thread_emails:				
				if 'scroll_pos' in request.POST and int(request.POST['idisp_email']) == int(i) :
					scroll_pos = int(request.POST.get('scroll_pos'))
					sl = Box_scroll_log.objects.create(user = request.user,session = session, scrollbar_pos = scroll_pos, for_email = t.parent_email)	
					scroll_positions.append(scroll_pos)
					if 'bheight' in request.POST:
						var_htname = request.POST.get('bheight')
						var_wname = request.POST.get('bwidth')
					
						bl = Box_log.objects.create(user = request.user,session = session, width = var_wname,height = var_htname, for_email = t.parent_email)
				else:
					sl_count = Box_scroll_log.objects.filter(user = request.user,session = session, for_email = t.parent_email).count()
					if sl_count == 0:
						scroll_positions.append(0)
					else:
						sl = Box_scroll_log.objects.filter(user = request.user,session = session, for_email = t.parent_email)[sl_count -1]
						scroll_positions.append(sl.scrollbar_pos)

				i = i + 1
			#thread_title = thread_emails[0].title	
			thread_count = thread_emails.count()		
        		return render(request,'home.html',{'user': request.user, 'all_emails':all_emails,'session':session, 'thread_title': rtitle, 'thread_emails':thread_emails,'thread_count':thread_count, 'click_count':click_count, 'error_msg':error_msg,'scroll_positions': scroll_positions, 'ks':ks})
			
			
	#thread_title = thread_emails[0].title	
	thread_count = thread_emails.count()
    	return render(request,'home.html',{'user': request.user, 'all_emails':all_emails,'session':session, 'thread_title': rtitle, 'thread_emails':thread_emails,'thread_count':thread_count, 'click_count':click_count, 'error_msg':error_msg,'ks':ks})

		
