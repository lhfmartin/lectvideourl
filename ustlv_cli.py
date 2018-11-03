import getpass
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
    for i2 in l3:
        if counter % 2 == 0 and counter != 0 and counter % 4!= 0:
            starttime = time.time()
        if counter % 4 == 0 and counter != 0:
            endtime = time.time()
            timetaken = endtime - starttime

        browser = RoboBrowser(history=True)
        browser.open(lvlink + str(i2))
        form = browser.get_form(id="fm1")
        form["username"].value = login1
        form["password"].value = login2

        browser.submit_form(form)
        htmlsource = str(browser.parsed)
        relist = re.findall("System error encount", htmlsource)
        if(len(relist) != 0):
            print("False", "(" + str(l3[counter]) + ")")
            p = round(counter / len(l3) * 100, 2)
            print(str(p) + "%")
        else:
            print("Done!", "Link: " + lvlink + str(i2))
            return (lvlink + str(i2))
        if counter > 4:
            eta = (len(l3) - counter) / 2 * timetaken
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
