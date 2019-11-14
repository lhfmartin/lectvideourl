import getpass
from robobrowser import RoboBrowser
import re
import sys
import time



def generatelists(start, fin):
    l1 = []
    l2 = []
    for i in range(start, fin):
        t1 = str(i)
        for a in range(0, len(t1) - 1):
            appended = False
            for b in range(a + 1, len(t1)):
                if t1[a] == t1[b]:
                    appended = True
                    l1.append(i)
                    break
            if appended == True:
                break
            if a == len(t1) - 1 - 1 and appended == False:
                l2.append(i)
    return l1, l2

def trywith(l3, ccode, lectsession, date, login1, login2):
    lvlink = "https://rvc.ust.hk/mgmt/media.aspx?path=18FA_" + ccode + "-" + lectsession + "_" + date + "_"
    counter = 0
    starttime = time.time()
    browser = RoboBrowser(history=True)
    browser.open(lvlink + str(l3[0]))
    form = browser.get_form(id="fm1")
    form["username"].value = login1
    form["password"].value = login2
    browser.submit_form(form)
    htmlsource = str(browser.parsed)
    print(htmlsource)

    for i2 in l3:
        if counter > 4:
            endtime = time.time()
            timetaken = endtime - starttime


        if counter % 7000 == 0 and counter > 6000:
            print("Sleeping, will resume in 30 seconds.")
            time.sleep(30)
        browser.open(lvlink + str(i2))
        htmlsource = str(browser.parsed)
        print(htmlsource)
        recas = re.findall("To access the protected service", htmlsource)
        while len(recas) > 0:
            #browser = RoboBrowser(history=True)
            browser.open(lvlink + str(i2))
            form = browser.get_form(id="fm1")
            form["username"].value = login1
            form["password"].value = login2
            browser.submit_form(form)
            htmlsource = str(browser.parsed)
            print(htmlsource)
            recas = re.findall("To access the protected service", htmlsource)
            
        relist = re.findall("System error encount", htmlsource)
        if(len(relist) != 0):
            print("False", "(" + str(l3[counter]) + ")")
            p = round(counter / len(l3) * 100, 2)
            print(str(p) + "%")
        else:
            print("Done!", "Link: " + lvlink + str(i2))
            with open("cs2611urls.txt", "a") as f:
                f.write("\n\n" + date[4:6] + "/" + date[2:4] + ":\n" + lvlink + str(i2) + "\n")
                if not bool(re.search("jwplayer", htmlsource)):
                    f.write("\tError\n")
            return (lvlink + str(i2))
        if counter > 4:
            eta = (len(l3) - counter) / counter * timetaken
            print("ETA:", str(int(eta / 60)) + "m" + str(int(eta % 60)) + "s")
        counter += 1
    return False


ccode = input("Course Code: ")
lectsess = input("Session: ")
date = input("Date: ")
starti = int(input("i0 = "))
endi = int(input("in = "))
username = input("ITSC: ")
password = getpass.getpass("Password: ")

l1 = list(range(starti, endi))

trywith(l1, ccode, lectsess, date, username, password)
