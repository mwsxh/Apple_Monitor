# -*- coding:utf-8 -*-
import urllib2,json,notify,time,urllib

model_map = {}
# read model list
in_f = open("models.txt","r")
for line in in_f:
    arr = line.strip().split("\t")
    model_map[arr[0]] = arr[1]
in_f.close()

req=urllib2.Request(url=r"https://reserve.cdn-apple.com/HK/zh_HK/reserve/iPhone/stores.json")
store_data = json.loads(urllib2.urlopen(req).read())
store_list = store_data["stores"]
store_map = {}
for item in store_list:
    store_map[item["storeNumber"]] = item["storeName"]


def check(monitor_models):
    req=urllib2.Request(url=r"https://reserve.cdn-apple.com/HK/zh_HK/reserve/iPhone/availability.json")
    try:
        status_data = json.loads(urllib2.urlopen(req).read())
    except urllib2.URLError,e:
        print e.message
        return []

    # print store_map

    avaliable_list = []

    for store, status_map in status_data.items():
        if store.startswith("R"):
            for model, status in status_map.items():
                if model.startswith("M"):
                    if model in monitor_models and status == "ALL":
                        avaliable_list.append((model,store))

    return avaliable_list


# run_time:h
def execute(monitor_models,email_addrs,run_time):
    start_time = time.time()
    seconds = run_time*3600
    while(True):
        result = check(monitor_models)
        if len(result)>0:
            content = construct_email_content(result)
            # notify.send_email("HK IPHONE有货通知!BY CYT",content,email_addrs)
            for item in result: print (model_map[item[0]],store_map[item[1]]+" | ")
            print "有货！"
            notify.send_wx(content)
            time.sleep(5)
        else:
            print "没货"
        time.sleep(1)
        if time.time() - start_time > seconds:
            break


def construct_email_content(result):
    content = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
    for item in result:
        model_name = model_map[item[0]]
        store_name = store_map[item[1]].encode("utf-8")
        content += model_name+" "+store_name+"\t|||||||\t"
    content += "赶紧上去抢啊!"
    return content

if __name__ == "__main__":
    monitor_models=[u"MN4D2ZP/A",u"MN482ZP/A",u"MN492ZP/A"]
    email_addrs = ["422780332@qq.com"]
    execute(monitor_models,email_addrs,2)

