from django.shortcuts import render, redirect
from firebase_admin import firestore
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import AddFacultyForm
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
def feedback(request):
    db = firestore.client()
    docs = db.collection(u'feedback').order_by(u'timestamp').stream()
    context = {'feedback': []}
    for doc in docs:
        context['feedback'].insert(0, doc.to_dict())
    return render(request, 'feedback.html', context)


@login_required
def add_faculty(request):
    if request.method == 'POST':
        form = AddFacultyForm(request.POST)
        if form.is_valid():
            db = firestore.client()
            counter = db.collection(u'counters').document(u'search')
            count = counter.get().to_dict()['num_of_fac']
            name = form.cleaned_data['name'].title()
            school = form.cleaned_data['school'].upper()
            designation = form.cleaned_data['designation'].title()
            data = {'name': name,
                    'school': school,
                    'designation': designation,
                    'university': 'VITCC'}
            count += 1
            db.collection(u'fac_details').add(data)
            counter.set({'num_of_fac': count})

            return redirect('/')

    else:
        form = AddFacultyForm()
    return render(request, 'add_faculty.html', {'form': form})


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



