#!/usr/bin/python3

import easysnmp
from easysnmp import *
import sys, time, math

agent_info = sys.argv[1]
my_info = agent_info.split(':')
ipaddress = my_info[0]
portnumber = my_info[1]
agentcommunity = my_info[2]
SampleFreq = float(sys.argv[2])
Counts_sample = int(sys.argv[3])
sample_time = 1/SampleFreq
ObjIDs = []
obj1=[]
obj2=[]
timer=""
#print(SampleFreq)
for i in range(4,len(sys.argv)):
	ObjIDs.append(sys.argv[i])
ObjIDs.insert(0,'1.3.6.1.2.1.1.3.0')
#OIDs=[int(float(l)) for l in ObjIDs] 
#print(ObjIDs)

#def SNMPagentTime():
#	#AgentTime=[]
#	session=Session(hostname=ipaddress,remote_port=portnumber,community=agentcommunity,version=2,timeout=1)
#	SnmpTime=session.get(ObjIDs)
#	return int(SnmpTime[0].value)
session=Session(hostname=ipaddress,remote_port=portnumber,community=agentcommunity,version=2,timeout=1,retries=3)

def sid():
	global obj1, t1, t2
	outcome = session.get(ObjIDs)
	TimerSys= int(outcome[0].value)/100
	obj2 = []
	#print("t2 {}".format(TimerSys))
#	for t in range(0,len(outcome)):
#		print("outcome value{}".format(outcome[t].value))

	# if int(TimerSys) > 2**32 or int(TimerSys) <= 0:
	# 	print(" The system just restarted. ")

	for th in range(1,len(outcome)):
		if outcome[th].value!='NOSUCHOBJECT' and outcome[th].value!='NOSUCHINSTANCE':

			#print(outcome[th].snmp_type)
			if outcome[th].snmp_type=='COUNTER64' or outcome[th].snmp_type=='GAUGE' or outcome[th].snmp_type=='COUNTER32' or outcome[th].snmp_type=='COUNTER':
				obj2.append(int(outcome[th].value))
				#print("loid2 {}".format(obj2))
			else:
				obj2.append(outcome[th].value)
			#print("loid1 {}".format(obj1))
	
			if count!=0 and len(obj1)>0:
				if TimerSys > t1:	
					if outcome[th].snmp_type=='COUNTER' or outcome[th].snmp_type=='COUNTER32'or outcome[th].snmp_type=='COUNTER64': 
						#print("if la oid2 {}".format(obj2[th-1]))
						#print("if la oid1 {}".format(obj1[th-1]))
						oiddiff = int(obj2[th-1]) - int(obj1[th-1])
						#print("oiddiff {}".format(oiddiff))
						#print(outcome[th].snmp_type)
						time_diff=(TimerSys - t1)
						#print("time diff {}".format(time_diff))
						rate = int(oiddiff / time_diff)
						#print("rate {}".format(rate))
						if rate < 0:
							if TimerSys > t1:
								if outcome[th].snmp_type == 'COUNTER32':
									#print(outcome[th].snmp_type)
									oiddiff = oiddiff + (2**32)
									try:
										if timer==str(t2):
											print(round(oiddiff/(time_diff)),end="|")
										else:
											print(t2,"|",round(oiddiff/(time_diff)), end="|");timer=str(t2)

									except:
										print(t2,"|", round(oiddiff/(time_diff)), end= "|");timer=str(t2)

								elif outcome[th].snmp_type == 'COUNTER64':
									#print(outcome[th].snmp_type)
									#time_diff = round(time_diff)
									#print("time_diff {}".format(time_diff))
									oiddiff=oiddiff+2**64
									#print(oiddiff)
									try:
										if timer==str(t2):
											#print(oiddiff/(time_diff))
											print(round(oiddiff/(time_diff)), end ="|")
										else:
											print(t2, "|", round(oiddiff/(time_diff)), end="|");timer=str(t2)
										
									except:
										#print(oiddiff/time_diff)
										print(t2,"|",round(oiddiff/(time_diff)),end= "|");timer=str(t2)

							else:
								print(" This seems like the system was restarted ")
								break

						else:
							try:
								if timer==str(t2):
									print( round(rate) ,end= "|")
									#print("1")
								else:
									print(t2,"|", round(rate), end="|") 
									timer=str(t2)
									#print("2")
							except:
								print(t2 ,"|", round(rate), end="|")  
								timer=str(t2)
								#print("3")

					elif outcome[th].snmp_type=='GAUGE':
						oiddiff = int(obj2[th-1]) - int(obj1[th-1])
						#if oiddiff>0: oiddiff="+"+str(oiddiff)
						try:
							if timer==str(t2):
								print(obj2[len(obj2)-1],"(",+oiddiff,")", end="|")
								#print("4")
							else:
								print(t2,"|",obj2[len(obj2)-1],"(",+oiddiff,")", end="|")
								timer=str(t2)
								#print("5")
						except:
							print(t2,"|",obj2[len(obj2)-1],"(",+oiddiff,")", end="|")
							timer=str(t2)
							#print("6")

				else: 
					print(" This seems like the system was restarted ")
					break
	obj1 = obj2
	t1 = TimerSys
	#print("new time {}".format(t1))
if Counts_sample==-1:
	count = 0
	obj1 = []
	while True:
		t2 = time.time()
		sid()
		if count!=0:
			print(end="\n")
		ResponseTime = time.time()
		count = count+1
		if sample_time >= ResponseTime - t2:
			time.sleep((sample_time- ResponseTime + t2))
		else:
			n=math.ceil((ResponseTime-t2)/sample_time)
			print(n,"n",((n*sample_time)- ResponseTime + t2))
			time.sleep(((n*sample_time)- ResponseTime + t2))
else:
	obj1 = []
	a=Counts_sample
	for count in range(0,Counts_sample+1):
		t2 = time.time()
		#print("intitial time ",t2)
		sid()
		if count!=0:
			print(end="\n")
		ResponseTime = time.time()
		#print(" resp time",ResponseTime)
		#print(-ResponseTime+t2, "respdiff")
		#print("sleep",(sample_time - ResponseTime + t2))
		if sample_time >= ResponseTime - t2:
			time.sleep((sample_time- ResponseTime + t2))
		else:
			n=math.ceil((ResponseTime-t2)/sample_time)
			#print(n,"n",((n*sample_time)- ResponseTime + t2))
			time.sleep(((n*sample_time)- ResponseTime + t2))