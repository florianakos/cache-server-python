import simplejson as json
import time
from api.vt_api import VirusTotalApi
from db.dynamo_db import DynamoDB
from flask import Flask, jsonify, request

app = Flask(__name__)
db = DynamoDB()
vt = VirusTotalApi()

def vt_ip_report(ip):
    cached = db.load("VTCacheIPAddresses", ip)
    if cached and "Item" in cached.keys():
        return cached["Item"]
    else:
        report = vt.get_ip_address_report(ip)
        if report and report['response_code'] == 1:
            cached_vt_data = {
                "query_value": ip,
                "timestamp": round(time.time()),
                "ttl": round(time.time()) + 120,
                "vtData": report
            }
            db.save(table_name="VTCacheIPAddresses", data=cached_vt_data)
            return cached_vt_data
        else:
            return {"query_value": ip, "timestamp": round(time.time()), "vtData": "Not found"}


def vt_domain_report(domain):
    cached = db.load("VTCacheDomains", domain)
    if cached and "Item" in cached.keys():
        return cached["Item"]
    else:
        report = vt.get_domain_report(domain)
        if report and report['response_code'] == 1:
            cached_vt_data = {
                "query_value": domain,
                "timestamp": round(time.time()),
                "ttl": round(time.time()) + 120,
                "vtData": report
            }
            db.save(table_name="VTCacheDomains", data=cached_vt_data)
            return cached_vt_data
        else:
            return {"query_value": domain, "timestamp": round(time.time()), "vtData": "Not found"}

def vt_url_report(url):
    cached = db.load("VTCacheURLs", url)
    if cached and "Item" in cached.keys():
        return cached["Item"]
    else:
        report = vt.get_url_report(url)
        if report and report['response_code'] == 1:
            cached_vt_data = {
                "query_value": url,
                "timestamp": round(time.time()),
                "ttl": round(time.time()) + 120,
                "vtData": report
            }
            db.save(table_name="VTCacheURLs", data=cached_vt_data)
            return cached_vt_data
        else:
            return {"query_value": url, "timestamp": round(time.time()), "vtData": "Not found"}

def vt_file_report(file_hash):
    cached = db.load("VTCacheFiles", file_hash)
    if cached and "Item" in cached.keys():
        return cached["Item"]
    else:
        report = vt.get_file_report(file_hash)
        if report and report['response_code'] == 1:
            cached_vt_data = {
                "query_value": file_hash,
                "timestamp": round(time.time()),
                "ttl": round(time.time()) + 120,
                "vtData": report
            }
            db.save(table_name="VTCacheFiles", data=cached_vt_data)
            return cached_vt_data
        else:
            return {"query_value": file_hash, "timestamp": round(time.time()), "vtData": "Not found"}

@app.route('/ip-address/report', methods=['POST'])
def ip_report():
    request_body = request.data.decode('utf-8').split('\n')
    return jsonify([vt_ip_report(ip) for ip in request_body])

@app.route('/url/report', methods=['POST'])
def url_report():
    request_body = request.data.decode('utf-8').split('\n')
    return jsonify([vt_url_report(ip) for ip in request_body])

@app.route('/domain/report', methods=['POST'])
def domain_report():
    request_body = request.data.decode('utf-8').split('\n')
    return jsonify([vt_domain_report(domain) for domain in request_body])

@app.route('/file/report', methods=['POST'])
def file_report():
    request_body = request.data.decode('utf-8').split('\n')
    return jsonify([vt_file_report(file_hash) for file_hash in request_body])


if __name__ == '__main__':

    app.config['JSON_SORT_KEYS'] = True
    app.run(host="0.0.0.0", port=8888, debug=True)
