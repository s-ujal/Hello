from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest



# Create your views here.

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')


def getToken(request):
    appId = "02f11f6818554a19a162e482329511b4"
    appCertificate = "2359e6ad792f413f820f5812190d799f"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


# def getMember(request):
#     uid = request.GET.get('UID')
#     room_name = request.GET.get('room_name')

#     member = RoomMember.objects.get(
#         uid=uid,
#         room_name=room_name,
#     )
#     name = member.name
#     return JsonResponse({'name':member.name}, safe=False)
def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    try:
        member = RoomMember.objects.get(uid=uid, room_name=room_name)
        name = member.name
        return JsonResponse({'name': member.name}, safe=False)
    except RoomMember.DoesNotExist:
        print("member not found")
        return HttpResponseBadRequest('Member not found')

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    try:
        member = RoomMember.objects.get(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )
        member.delete()
        return JsonResponse('Member deleted', safe=False)
    except RoomMember.DoesNotExist:
        print("member not found")
        return HttpResponseBadRequest('Member not  found')