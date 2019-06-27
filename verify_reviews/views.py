from django.shortcuts import render, redirect
from firebase_admin import firestore
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

approve = 9001
reject = 500
unReviewed = 401


@login_required
def index(request):
    if request.method == 'POST':
        submit_type = request.POST.get('action')
        check = request.POST.getlist('check')
        if submit_type == 'Approve':
            change_review_status(check, approve)
        elif submit_type == 'Reject':
            change_review_status(check, reject)
    docs = get_data_from_firebase(unReviewed)
    context = {'reviews': []}
    for doc in docs:
        document = doc.to_dict()
        document['id'] = doc.id
        dic = context['reviews']
        dic.append(document)

    return render(request, 'index.html', context)


@login_required
def approved(request):
    if request.method == 'POST':
        check = request.POST.getlist('check')
        change_review_status(check, reject)
        return redirect('/')

    docs = get_data_from_firebase(approve)
    context = {'reviews': []}
    for doc in docs:
        document = doc.to_dict()
        document['id'] = doc.id
        dic = context['reviews']
        dic.append(document)
    return render(request, 'approved.html', context)


@login_required
def rejected(request):
    if request.method == 'POST':
        check = request.POST.getlist('check')
        change_review_status(check, approve)
        return redirect('/')

    docs = get_data_from_firebase(reject)
    context = {'reviews': []}
    for doc in docs:
        document = doc.to_dict()
        document['id'] = doc.id
        dic = context['reviews']
        dic.append(document)
    return render(request, 'rejected.html', context)


@login_required
def sign_out(request):
    logout(request)
    return redirect('/')


def get_data_from_firebase(status_code):
    db = firestore.client()
    docs = db.collection(u'user_review').where(u'status', u'==', status_code).stream()
    return docs


def change_review_status(check, status_code):
    db = firestore.client()
    for doc_id in check:
        doc = db.collection(u'user_review').document(doc_id).get()
        doc = doc.to_dict()
        doc['status'] = status_code
        db.collection(u'user_review').document(doc_id).set(doc)



