#!/usr/bin/env python
#coding:utf-8
import time
import os
from apns import APNs, Payload, Frame
from gcm import GCM
from pyramid.view import view_config


here = os.path.abspath(os.path.dirname(__file__))


@view_config(route_name='push_cmccdali', renderer='json')
def push_cmccdali(request):

    def send_apn(title, ios_tokens):
        cert = os.path.join(here, 'certs/cmccdali.pem')
        apns = APNs(use_sandbox=False, cert_file=cert, key_file=cert)
        frame = Frame()
        identifier = 1
        expiry = time.time() + 3600
        priority = 10
        payload = Payload(alert=title, sound="default", badge=1)
        map(lambda token_hex: frame.add_item(token_hex, payload, identifier, expiry, priority), ios_tokens)
        apns.gateway_server.send_notification_multiple(frame)

    def send_gcm(title, android_tokens):

        API_KEY = "AIzaSyD8fBIglR0mjQRYp2MNhMf4EOB0Yns1BQU"
        gcm = GCM(API_KEY)
        data = {
            "title": "渠信通",
            "message": title,
            "msgcnt": "1",
            "soundname": "beep.wav"
        }

        # Plaintext request
        # reg_id = 'APA91bECCGb10glOktSyt8AxvDqJPVUQbGBDEl5z5YdVZhUnNSytL3qPyfUbSs1Dm3bfHil-jm3E1vhsE4Fqq4fWsx2cyiI2cv-izAaITnnvccODPcAjw4SasnqSz94qpwKQudQpXaANdYyWQbeqBYTXFTCGz-68MA'
        # reg_id2 = 'APA91bFde0j2m9rTmOQ-TjZJyM_m_O0U3_RRZ_3sHnSESmkP66erMbdpHxP0G0jeYsnHn0TATEUmQqbVc3e935_SjvXFkKtma-jzOxO2KGsWTGRSQPXvnCMYJ73CjTBrJRRTFivhy06TopsS0uBx_NEyMn6VVGTiiA'

        #gcm.plaintext_request(registration_id=[reg_id2, data=data)

        # # JSON request
        # reg_ids = [reg_id, reg_id2]
        # response = gcm.json_request(registration_ids=reg_ids, data=data)

        # Extra arguments
        gcm.json_request(
            registration_ids=android_tokens, data=data,
            collapse_key='uptoyou', delay_while_idle=True, time_to_live=3600
        )

    print request.body
    try:
        data = request.json_body
    except ValueError:
        return {"status_code": 1, "status_msg": "json_body error"}

    print data
    send_apn(data["title"], data["iphone_takens"])
    send_gcm(data["title"], data["andriod_takens"])
