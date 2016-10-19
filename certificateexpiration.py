#!/usr/bin/python3
# -*- coding: utf-8 -*-


import datetime
import ssl
import OpenSSL
import socket

"""Checks server SSL certificate for expiry."""


def check():
    hostname = "your_server.com"
    port = 443

    num_days = 7
    cert = ssl.get_server_certificate(
        (hostname, port), ssl_version=ssl.PROTOCOL_TLSv1)
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    expiry_date = x509.get_notAfter()
    print(str(expiry_date))
    assert expiry_date, "Cert doesn't have an expiry date."

    ssl_date_fmt = r'%Y%m%d%H%M%SZ'
    expires = datetime.datetime.strptime(str(expiry_date)[2:-1], ssl_date_fmt)
    remaining = (expires - datetime.datetime.utcnow()).days

    if remaining <= num_days:
        print("ALERTING!")
    else:
        print("Not alerting. You have " + str(remaining) + " days")


check()
