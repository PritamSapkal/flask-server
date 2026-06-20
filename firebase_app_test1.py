from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Firebase JSON Key
firebase_config = {
  "type": "service_account",
  "project_id": "potholes-tracker-6de66",
  "private_key_id": "b64c3a4c0aa82517b6e1cfd0113ccf4edee6a85f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDI7o12k7vRXKWf\nHJO6xzMT56V+97dCMmTr9pGNdCKI15bVDEcRu5YFD5Fx8Gqx8hweIpZh2qEcGdlL\nOwIvEkz48Oea6EMrWhun6Fv67GhgJENuvgur3wP8WBM7eH3Ur7ta54Z9PxuBc2ys\nhNKnkJMAqnaWIYpm1cgOK8HX9omXpcykk/7MciWYL04pmbZ4qaTVjEAAf2LrmwqX\nZ9d55Suki9UGUIB8B7U1ARoY8iRvSiYXJ96ZWQckyP202UDsWpkkwB6cIRod5jPI\nc6bOlINYjNTKKDZzq1SjUYnbkaxiyU+U4itK+/REGAbeBeQTyMFIyBDj7HRSf1d6\nyUKlAsKfAgMBAAECggEAAKi/sA7mA9bQ+EeouGkk4sDUyyjW4hG2QQvrCFLENjy2\n0vYaWZWK9XNKn9wRDYpkyziD08ha1PPEwbls1Wiy9fIcYGa4qbC+/HsHqjgSU5Zq\n3jcjZKnzomVLkttfVk5JSBAQYeLOHUuapKo+4qvXv53Pi8iKYrH62QkNtr6pTuUL\n3LNrn9SUG0lu/kiQn87n2qA6LlZUH5ttIcDD7NjcKUBdG6BKY0dECCGBXxVWs6ij\nweVypE5rZySP2htNFIPV1NfoIqEg+yQPzQmbETlEpDtbJbw1RsIMIyhpaF8eDizl\nRU2e5sqLG2UYK2s7j2el60loCMXnOEcJSe7WYX8JyQKBgQDpm39K0A8BZY2L7Pbq\nfwqwcgxoGdVZ6WHz4kZP/UFOkPiNGtr32LJ5cZg9+PVP4pq9i19fEijc9+AjThp5\nxEFxkxwxFePV66gsnR6bhpNE5u+gKUkvdCJA++d2ZKoJmNfty7TBdq4WW7KGt/vM\nn00zxdl/7KisUK+xCEPs0vGZOwKBgQDcMTprDgGUSJypkbOTkWY0DawhDVm1vIII\nNKh2Fn7xL4byM54AOJUpbjsD6F65KqQyU5N3fGYXpTZBMiwZiKU+kySMcH4HJkjQ\nR2y7tSZQ5k4q/oNUbxNShDr3JU/osP8jogN+xXxs3XC8Q1Pwl/SeQj8mx7YYwmYx\ny6xBLnFF7QKBgA2mBSDk2QuW2FdFiAOZWpGGiE0IvVtcdFmgbcU8obUqaSstV3/F\njF/mECQGyKZbMflDDFZspDCM1u6ZIJjeq4gsNSh1A/O6qf+5SlGB4lbTO0rbPqhk\nG6A6V4KmTPz0jiEZlrz65x7tSpfuZerFn+gXdiawOAahTDKGrhlHFdCDAoGAMCH6\nuSgopDdzN4YIETv5cWuDsv3uHFIGwrBwGtA0E5jmEM/DvByiTpowAFytSCDQH8gx\nNi9VSdntkDbdeP9rz8/ub1yvz/RIem8Cj827gHe3oqJcJvrY6HLLSPc5Do6SV0G1\nLeMRneKSIDU/hhpReL7Wey2w2py0JjJ1hxIV5MkCgYAybx4HqT4OHKwXjQo0sVz4\no7SmPRTBgFq13SdB9NDAAA9HyH62oz/8RwIkpZSUmCJjr80cPznp/n4CpzKg4MgG\nvW5UYzAn6SlpHkpUTeIfIDdcjW3aN2ZmWHmfZM9JDKyXF8DaIbA1tI+Uv3FYLdsY\nWu8ciabaY0D4ncVvZZH6Jw==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@potholes-tracker-6de66.iam.gserviceaccount.com",
  "client_id": "114758203481956963523",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40potholes-tracker-6de66.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_pothole_data():
    try:
        potholes_ref = db.collection("potholes_database").stream()
        data = [{
            "latitude": float(doc.to_dict().get("latitude", 0)),
            "longitude": float(doc.to_dict().get("longitude", 0)),
            "size": str(doc.to_dict().get("size", "")).strip().lower()
        } for doc in potholes_ref if doc.to_dict().get("latitude") and doc.to_dict().get("longitude")]
        return data
    except Exception as e:
        print(f"Firebase Error: {str(e)}")
        return []

@app.route('/api/potholes', methods=['GET'])
def potholes():
    try:
        data = get_pothole_data()
        return jsonify({
            "success": True,
            "count": len(data),
            "data": data if data else []
        })
    except Exception as e:
        return jsonify({"success": False, "error": "Server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
