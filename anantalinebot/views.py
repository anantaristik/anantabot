import random
import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


def index(request):
    return HttpResponse("test!!")

@csrf_exempt
def callback(request):
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        global domain
        domain = request.META['HTTP_HOST']

        # get request body as text
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@handler.add(MessageEvent, message=TextMessage)
def message_handle(event):
    users_msg = event.message.text

    list_random_msg = ["kenapa?", "gatau", "nanti coba lagi ya!", "ohh, ok", "sabar"]
    random_ya_tdk = ["ya", "mungkin", "tidak"]
    random_pap = ["https://ibb.co/GHgR7Vp","https://ibb.co/BtY4xm3","https://ibb.co/M1HVHjZ","https://ibb.co/jyk8Frp","https://ibb.co/VLNgNRt"]

    not_found = str(random.choice(list_random_msg))
    tanya_anan = str(random.choice(random_ya_tdk))
    pap_rand = random.choice(random_pap)

    JADWAL_SENIN = ("[JADWAL KULIAH HARI SENIN] \n\nSemangat ya Ananta\n\n" 
				+ "1.) Anum C\n"
				+ "> Waktu: 08.00-08.50 WIB \n"
                + "> Lokasi: A2.07 (Ged baru) \n\n"

                + "2.) RPL B\n"
				+ "> Waktu: 13.00-14.40 WIB \n"
                + "> Lokasi: A6.09 (Ged Baru) \n\n"

                + "3.) JarKom B\n"
				+ "> Waktu: 15.00-16.40 WIB \n"
                + "> Lokasi: daring"
    )
    JADWAL_SELASA = ("[JADWAL KULIAH HARI SELASA] \n\nSemangat ya Ananta\n\n" 
				+ "1.) StatProb A\n"
				+ "> Waktu: 10.00-11.40 WIB \n"
                + "> Lokasi: 2.2302 (Ged lama) \n\n"

                + "2.) Technop A\n"
				+ "> Waktu: 13.00-14.40 WIB \n"
                + "> Lokasi: A1.10 (Ged Baru) \n\n"

                + "3.) DAA C\n"
				+ "> Waktu: 15.00-16.40 WIB \n"
                + "> Lokasi: 3.3111-3.3112 (Ged C - Digabung)"
    )
    JADWAL_RABU = ("[JADWAL KULIAH HARI RABU] \n\nSemangat ya Ananta\n\n" 
				+ "1.) Anum C\n"
				+ "> Waktu: 08.00-09.40 WIB \n"
                + "> Lokasi: A2.07 (Ged baru) \n\n"

                + "2.) RPL B\n"
				+ "> Waktu: 11.00-11.50 WIB \n"
                + "> Lokasi: A6.09 (Ged Baru) \n\n"

                + "3.) JarKom B\n"
				+ "> Waktu: 13.00-14.40 WIB \n"
                + "> Lokasi: 3.3111-3.3112 (Ged C - Digabung)"
    )
    JADWAL_KAMIS= ("[JADWAL KULIAH HARI KAMIS] \n\nSemangat ya Ananta\n\n" 
				+ "1.) StatProb A\n"
				+ "> Waktu: 10.00-10.50WIB \n"
                + "> Lokasi: 2.2302 (Ged lama) \n\n"

                + "2.) Technop A\n"
				+ "> Waktu: 14.00-14.50 WIB \n"
                + "> Lokasi: A1.10 (Ged Baru) \n\n"

                + "3.) DAA C\n"
				+ "> Waktu: 15.00-16.40 WIB \n"
                + "> Lokasi: 3.3111-3.3112 (Ged C - Digabung)"
    )

    HELP = ("[ANANTA BOT MESSAGE] \n\nIni bantuan untuk anantabot\n\n" 
				+ "1.) Ketik 'ananta'\n" 
				+ "> Biar penasaran aja.\n\n"
				+ "2.) Ketik '!tanya pertanyaan'\n" 
				+ "> (ex: '!tanya apakah ananta ganteng?')\n\n"
				+ "3.) Ketik '!ananta jadwal-hari'\n"
				+ "> Untuk melihat jadwal kuliah ananta\n\n"
				)

    if users_msg == "ananta":
        response = "itu aku!"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))

    elif users_msg[:7].lower() == "!ananta":
        
        users_msg = users_msg[8:].strip()

        if users_msg == "jadwal-senin":
            response = JADWAL_SENIN
        elif users_msg == "jadwal-selasa":
            response = JADWAL_SELASA
        elif users_msg == "jadwal-rabu":
            response = JADWAL_RABU
        elif users_msg == "jadwal-kamis":
            response = JADWAL_KAMIS
        elif users_msg == "help":
            response = HELP

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))

    elif users_msg[:6].lower() == "!tanya":

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=tanya_anan))

    elif users_msg == "pap":
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url=pap_rand,
            preview_image_url=pap_rand))

    else:
        response = not_found

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))
