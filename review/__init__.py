import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('verify_reviews/review-fdf05-firebase-adminsdk-szrvl-d4063f98f4.json')
firebase_admin.initialize_app(cred)
