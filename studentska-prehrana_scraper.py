# -*- coding: utf-8 -*-
import os
import sys
from bs4 import BeautifulSoup
import urllib
import sys
import MySQLdb
import time

start_time = time.time()
reload(sys)
sys.setdefaultencoding('utf-8')
db = MySQLdb.connect(host="",
                     user="",
                     passwd="",
                     db="", use_unicode=True, charset='utf8')
cur = db.cursor()

#Url
r = urllib.urlopen('https://studentska-prehrana.si/Pages/Directory.aspx').read()
soup = BeautifulSoup(r, "html.parser")

basic_info = ""
info = ""
meniji = ""
feat = ""
baza_address1 = ""
baza_city1 = ""
baza_features = ""
baza_features_ids = ""
baza_href = ""
baza_rest_name = ""
baza_opening_note = ""
baza_meniji = ""
pripravi_za_bazo_meniji = ""


def vrni_id_featuresa(x):
    return {
        'Stalen arhitektonsko prilagojen dostop za invalide in dostop do mize v notranjosti lokala': 8,
        'Stalen arhitektonsko prilagojen dostop za invalide in dostop do mize v notranjosti lokala ter do toalete prilagojene za invalide': 8,
        'Vegetarijanska prehrana': 2,
        'Kosila': 5,
        'Lokal odprt ob vikendih': 7,
        'Pizze': 1,
        'Solatni bar': 4,
        'Dostava': 6,
        'Študentske ugodnosti': 3,
    }.get(x, 9)


for el in soup.find_all('li', {'class': 'restaurantItem'}):
    info += "["
    for rest in el.find_all('div'):
        aa = str(rest.get('class'))
        if (aa == "[u'name']"):
            for hr in rest('h1'):
                for hr1 in rest('a'):
                    info += str(hr1.get("href"))
                    info += "|"
                    baza_href = hr1.get('href')
                    baza_hash = str(baza_href.strip()[-36:])
                    baza_hash = str(baza_hash.strip()[:26])
                    rr = urllib.urlopen(hr1.get("href")).read()
                    soup_linki = BeautifulSoup(rr, "html.parser")
                    for small_info in soup_linki.find_all('span', {
                        'id': 'ContentHolderMain_ContentHolderMainContent_ContentHolderMainContent_lblRestaurantAddress'}):
                        # print info_.text
                        info += str(small_info.text.strip())
                        info += "|"
                        baza_phone = str(small_info.text.strip())
                        if baza_phone.find("tel:") != -1:
                            baza_phone = baza_phone.rsplit('tel: ', 1)[1]
                            baza_phone = baza_phone.replace(')', '')
                        else:
                            baza_phone = ""
                        # kraj in mesto
                        if small_info.text.strip().find("(") != -1:
                            baza_address1 = small_info.text.strip().rsplit(',', 1)[0]
                            tmp22 = baza_address1
                            baza_address1 = baza_address1.strip().rsplit(',', 1)[0]
                            baza_address1 = baza_address1.replace('(', '')
                            # ce vsbeuje se fonsko se more 1x splitat
                            if baza_address1.find(",") != -1:
                                tmp22 = baza_address1
                                baza_address1 = baza_address1.strip().rsplit(',', 1)[0]
                            baza_city1 = tmp22.rsplit(',', 1)[1]
                            baza_city1 = baza_city1[1:]
                            baza_city1 = baza_city1[5:]
                    for elmen in soup_linki.find_all('div', {'class': 'holderRestaurantInfo'}):
                        for meni_ol in elmen.find_all('ol'):
                            for meni_li in meni_ol.find_all('li'):
                                for meni_h1 in meni_li.find_all('h1'):
                                    if meni_h1.text.isdigit() == True:
                                        # print meniji
                                        info += str(meni_h1.text)
                                        info += "|"
                                        for el1 in meni_li.find_all('li'):
                                            # print el1.text
                                            meniji += "("
                                            meniji += str(el1.text)
                                            meniji += ")"
                                            info += meniji + "|"
                                            baza_meniji += str(el1.text) + "(|)"
                                            meniji = ""
                                        pripravi_za_bazo_meniji += baza_meniji
                                        baza_meniji = ""
                                        pripravi_za_bazo_meniji += "($)"



                    features_link = hr1.get("href")[:-1] + "1"
                    rrr = urllib.urlopen(features_link).read()
                    soup_info = BeautifulSoup(rrr, "html.parser")
                    for info_ in soup_info.find_all('li', {
                        'id': 'ContentHolderMain_ContentHolderMainContent_ContentHolderMainContent_riInfo_liWeek'}):
                        # print info_.text
                        info += str(info_.text.strip())
                        info += "|"
                        baza_opening_week = str(info_.text.strip())

                        baza_opening_week = baza_opening_week[38:]
                        baza_opening_week = baza_opening_week.replace(" do ", ",").strip()

                    for info_1 in soup_info.find_all('li', {
                        'id': 'ContentHolderMain_ContentHolderMainContent_ContentHolderMainContent_riInfo_liClosedWeekends'}):
                        # print info_.text
                        info += str(info_1.text.strip())
                        info += "|"
                        baza_opening_ends = str(info_1.text.strip())
                    for info_2 in soup_info.find_all('li', {
                        'id': 'ContentHolderMain_ContentHolderMainContent_ContentHolderMainContent_riInfo_liNotes'}):
                        # print info_.text
                        info += str(info_2.text.strip())
                        info += "|"
                        baza_opening_note = str(info_2.text.strip())
                    info += "|"
        if (aa == "[u'name']"):
            # print rest.text
            info += str(rest.text.strip())
            info += "|"
            baza_rest_name1 = str(rest.text.strip())
            baza_rest_name2 = str(rest.text.strip())
            baza_rest_name = baza_rest_name1.rsplit('(', 1)[0].strip()

            if baza_rest_name.find("(") != -1:
                baza_rest_name = baza_rest_name.rsplit('(', 1)[0]
                baza_v_obnovi = "1"
            baza_rest_name = baza_rest_name.replace('"', '')
        if (aa == "[u'prices']"):
            baza_price_tmp = str(rest.text.strip()[:24])
            baza_price = baza_price_tmp.strip()[-4:]
            baza_price = baza_price.replace(",", ".")
        if (aa == "[u'features']"):
            # print rest
            for features_img in rest.find_all('img'):
                feat += "{"
                feat += str(features_img.get("title"))
                baza_features += str(features_img.get("title")) + "|"
                feat += "}"
                info += str(feat)
                feat = ""

    insert_stmt = (
        "INSERT INTO 2estaurants(original_id,name,address,city,value_of_charge,phone,opening_week,opening_sat,opening_note,slug,created_at,updated_at) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now())"
    )
    data = (
    baza_hash, baza_rest_name, baza_address1, baza_city1, baza_price, baza_phone, baza_opening_week, baza_opening_ends,
    baza_opening_note, baza_hash)
    cur.execute(insert_stmt, data)
    db.commit()

    # print baza_href
    # print "1["+baza_rest_name+"]"
    # print "2["+baza_address1+"]"
    # print "3["+baza_city1+"]"
    # print "4["+baza_price+"]"
    # print "5["+baza_phone+"]"
    # print "6["+baza_opening_week+"]"
    # print "7["+baza_opening_ends+"]"
    # print "8["+baza_opening_note+"]"
    # print "9["+baza_meniji+"]"
    # print "10["+baza_features+"]"
    # pripravi_za_bazo_meniji+="(h)"+baza_hash+"(h)


    baza_meniji_V = ""
    meniji_spl = pripravi_za_bazo_meniji.split("($)")
    for men in meniji_spl:
        # print men
        meniji_spl2 = men.split("(|)")
        # print "{"
        for men2 in meniji_spl2:
            #   print "("+men2+")"
            baza_meniji_V += men2 + ";"

        # print "}"
        if baza_meniji_V:
            if baza_meniji_V != ";":
                insert_stmt2 = (
                    "INSERT INTO 2enus(content,restaurant_id,created_at,updated_at)"
                    "VALUES (%s,%s,now(),now())"
                )
                baza_meniji_V = baza_meniji_V[:-1]
                data2 = (baza_meniji_V, baza_hash)
                cur.execute(insert_stmt2, data2)
                db.commit()
                baza_meniji_V = ""

    featursi_spl = baza_features.split("|")
    for fe in featursi_spl:
        # print vrni_id_featuresa(fe)
        insert_stmt2 = (
            "INSERT INTO 2eature_restaurant(feature_id,restaurant_id,created_at,updated_at)"
            "VALUES (%s,%s,now(),now())"
        )
        data2 = (vrni_id_featuresa(fe), baza_hash)
        cur.execute(insert_stmt2, data2)
        db.commit()


    pripravi_za_bazo_meniji = ""

    baza_href = ""
    baza_rest_name = ""
    baza_meniji = ""
    baza_features = ""
    info = ""
    baza_hash = ""
# print basic_info

print("--- %s seconds ---" % (time.time() - start_time))

