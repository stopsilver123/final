from flask import Flask, render_template, request, redirect, flash, url_for, session
from database import DBhandler
import hashlib
import sys
import math
application = Flask(__name__)
DB = DBhandler()
application.secret_key = 'super secret key'
application.config['SESSION_TYPE'] = 'filesystem'


@application.route("/") 
def hello():
    return render_template("EDhome.html")
    
@application.route("/EDhome") 
def home_restaurant():
    return render_template("EDhome.html")

@application.route("/EDlist") 
def list_restaurants():
    page=request.args.get("page",0,type=int)
    category = request.args.get("category", "all")
    limit=6
    
    start_idx=limit*page
    end_idx=limit*(page+1)
    
    if category=="all":
        data=DB.get_restaurants()
    else:
        data=DB.get_restaurants_bycategory(category)
    if data is None:
        tot_count=0
    else:
        tot_count=len(data)
    print("category",category,tot_count)
    if tot_count<=limit:
        data = dict(list(data.items())[:tot_count])
    else:
        data = dict(list(data.items())[start_idx:end_idx])
    data=dict(sorted(data.items(), key=lambda x:x[1]['name'], reverse=False))
    page_count = len(data)
    print(tot_count,page_count)
    #print("리스트데이터확인")
    #print(data)
              
    avgRate_list=[]
    for res in data.values():
        avg_rate=DB.get_avgrate_byname(str(res['name']))
        print(avg_rate)
        avgRate_list.append(avg_rate)
        
    top_restaurants=DB.get_restaurants_byHeartCount() #top4 식당이름 리스트
    
    return render_template("EDlist.html", top4=top_restaurants, avg_rate=avgRate_list, datas=data.items(), total=tot_count, limit=limit, page=page, page_count=math.ceil(tot_count/6), category=category)

@application.route("/EDonepick") #로그인 안 한 경우
def onepick_restaurant_nologin():
    total=0
    return render_template("EDonepick.html", total=total)

@application.route("/EDonepick/<user>/") #로그인 되어있는 경우
def onepick_restaurant(user):
    data=DB.get_restaurant_bypicked(str(user))
    total=len(data)
    data = dict(list(data.items())[:total])
    data=dict(sorted(data.items(), key=lambda x:x[1]['name'], reverse=False))
    return render_template("EDonepick.html", datas=data.items(), total=total)

@application.route("/EDonepick/<user>/", methods=['POST', 'GET']) #찜화면목록삭제
def EDonepick_change(user):
    data_heart=request.form['heart']
    data_restaurant=request.form['restaurant']
    data_user=user

    print(data_heart)
    print(data_restaurant) #앞단어만가져옴;
    
    DB.turn_picked(data_restaurant, data_user, data_heart)
    return redirect(url_for('onepick_restaurant', user=data_user))


@application.route("/EDRegister") 
def reg_restaurant():
    return render_template("EDRegister.html")


@application.route("/EDmoreinformation/<name>/") 
def list_(name):
    data = DB.get_restaurant_byname(str(name))
    print("####data:",data)
    return render_template("EDmoreinformation.html", data = data)

@application.route("/EDdetail_notLogin/<name>/") #리스트에서 넘어옴 로그인xx
def list_detail_notLogin(name):
    data = DB.get_restaurant_byname(str(name))
    avg_rate = DB.get_avgrate_byname(str(name))
    Data = DB.get_menu_byresname(str(name))
    data_main = DB.get_mainmenu_byrestname(str(name))
    data_side=DB.get_sidemenu_byrestname(str(name))
    data_review = DB.get_review_byresname(str(name))
    review_total = len(data_review)

    return render_template("EDdetail_notLogin.html", data=data, avg_rate=avg_rate, Data=Data, data_main=data_main, data_side=data_side, data_review=data_review, review_total=review_total)

@application.route("/EDdetail/<restaurant_name>/<user_name>/") #리스트에서 넘어옴   
def list_detail_withHeart(restaurant_name, user_name):
    data = DB.get_restaurant_byname(str(restaurant_name))
    avg_rate = DB.get_avgrate_byname(str(restaurant_name))
    Data = DB.get_menu_byresname(str(restaurant_name))
    data_main = DB.get_mainmenu_byrestname(str(restaurant_name))
    data_side=DB.get_sidemenu_byrestname(str(restaurant_name))
    data_review = DB.get_review_byresname(str(restaurant_name))
    review_total = len(data_review)

    data_pick = DB.restaurant_and_heart(str(user_name))
    heart = "OFF"

    for res in data_pick:
        if res == restaurant_name:
            heart = "ON"
            break
        else:
            heart = "OFF"
    print("하트출력")
    print(heart)
    return render_template("EDdetail.html", data=data, avg_rate=avg_rate, Data=Data, data_main=data_main, data_side=data_side, data_review=data_review, review_total=review_total, data_heart = heart)



@application.route("/EDdetail", methods=['POST']) #맛집등록직후
def ED_register_post():
    global idx
    image_file=request.files["upload"]
    image_file.save("static/images/{}".format(image_file.filename))
    data=request.form
    restaurant_name=request.form['restaurant_name']
    print(restaurant_name)
    print(data)

    if DB.insert_restaurant(data['restaurant_name'], data, image_file.filename):
        return redirect(url_for('list_detail_notLogin', name=restaurant_name))
    else:
        return "Restaurant name already exist!"
    

    #상세화면에서 찜하는 용  
@application.route("/EDdetail/<restaurant_name>/", methods=['POST', 'GET'])
def ED_heart_change(restaurant_name):
    data_heart=request.form['heart']
    data_user=request.form['user_name']
    print(data_heart)
    """
    if data_heart=="ON":
        DB.turn_picked(restaurant_name, data_user)
    elif data_heart=="OFF":
        DB.turn_unpicked(restaurant_name, data_user)
    """
    DB.turn_picked(restaurant_name, data_user, data_heart)
    DB.turn_pick_restaurant_count(restaurant_name, data_heart)
    return redirect(url_for('list_detail_withHeart', restaurant_name=restaurant_name, user_name=data_user))
    
@application.route("/EDmenuRegister", methods=['POST']) #식당이름만 전달
def reg_menu():
    data=request.form
    print(data)
    return render_template("EDmenuRegister.html", data=data)

@application.route("/EDreviewRegister", methods=['POST']) #리뷰더보기->리뷰등록하기
def reg_review():
    data=request.form
    print(data)
    return render_template("EDreviewRegister.html", data=data)

# detail 화면 메뉴
@application.route("/EDdetail/<res_name>/")
def view_menu(res_name):
    data_restaurantName=request.form
    data_name1=restname
    
    data_main = DB.get_mainmenu_byrestname(str(restname))
    data_side=DB.get_sidemenu_byrestname(str(restname))
    print("####main:",data_main)
    print("####side:", data_side)
    
    tot_count=len(data_main)+len(data_side)
        
    
    return render_template("EDMoreMenu.html", data_restname=data_name1, dataM=data_main, dataS=data_side, total=tot_count)
    
# detail 화면 리뷰
@application.route("/EDdetail/<res_name>/")
def view_review(res_name):
    data_review = DB.get_review_byresname(str(res_name))
    tot_count=len(data)
    
    page_count = len(data)
    
    return render_template("EDdetail.html", data_review=data_reivew, total=tot_count)
    
    
    
@application.route("/EDMoreMenu/<restname>/",methods=['POST','GET'])
def view_menus(restname):
    
    data_restaurantName=request.form
    data_name1=restname
    data_main = DB.get_mainmenu_byrestname(str(restname))
    data_side=DB.get_sidemenu_byrestname(str(restname))
    data_rate= DB.get_avgrate_byname(str(restname))
    print("####main:",data_main)
    print("####side:", data_side)
    
    tot_count=len(data_main)+len(data_side)
        
    
    return render_template("EDMoreMenu.html", data_restname=data_name1, dataM=data_main, dataS=data_side, total=tot_count)


@application.route("/EDMoreMenu", methods=['POST'])
def menu_register():
    image_file=request.files["photo1"]
    image_file.save(("static/images/{}".format(image_file.filename)))
    data=request.form
    
    restname=data['restaurant_name']
    
    if DB.insert_menu(restname, data,image_file.filename):
        return redirect (url_for('view_menus', restname=restname))

    
@application.route("/EDMOREreview", methods=['POST'])
def ED_review_register_content():
    image_file=request.files["photo2"]
    image_file.save("static/images/{}".format(image_file.filename))
    data=request.form

    print(data)
    resname=data['restaurant_name']
    if DB.insert_review(data, image_file.filename):
        return redirect(url_for('view_reviews', res_name=resname)) #식당이름으로찾아야됨
    
    
@application.route("/EDMOREreview/<res_name>/", methods=['POST', 'GET'])
def view_reviews(res_name):
    data_restaurantName=request.form #html에서 식당이름만 받아옴
    data_Rname2=res_name
    data=DB.get_review_byresname(str(res_name))
    rate=DB.get_rate_byname(str(res_name))
    print("####data: ", data)
    if not data:
        tot_count=0
    else:        
        tot_count=len(data)
        
    return render_template("EDMOREreview.html", data2_restaurant_name=data_Rname2, datas=data, rate=rate,total=tot_count)


#회원가입
@application.route("/EDSignup")
def signup():
    return render_template("EDSignup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data,pw_hash):
        return render_template("EDLogin.html")   
    else:
        flash("이미 존재하는 아이디입니다!")
        return render_template("EDSignup.html")
    
# 로그인
@application.route("/EDLogin")
def login():
    return render_template("EDLogin.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('hello'))
    else:
        flash("아이디와 비밀번호를 다시 확인해주세요!")
        return render_template("EDLogin.html")
    
#로그아웃
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('hello'))
    
    #계산기 화면
@application.route("/EDrecommend") 
def before_recommend():
    data=DB.get_restaurants()
    total=0
    return render_template("EDrecommend.html", total=total)

#가격대 sorting 
@application.route("/EDrecommendResult", methods=['GET','POST'])
def recommend_restaurants():
    page=request.args.get("page",0,type=int)
    #result = request.args.get("recommend_cost",type=int)
    result=int(request.form['recommend_cost'])
    print(result)
    limit=6
    
    start_idx=limit*page
    end_idx=limit*(page+1)
    
    if (result>=5000) and (result<7000):
        data=DB.get_restaurants_byprice(5000)
        print("오천원")
        print(data)
        print("출력끝")
    elif (result>=7000) and (result<10000):
        data=DB.get_restaurants_byprice(7000)
    elif (result>=10000) and (result<15000):
        data=DB.get_restaurants_byprice(10000)
    elif (result>=15000) and (result<20000):
        data=DB.get_restaurants_byprice(15000)
    elif (result>=20000):
        data=DB.get_restaurants_byprice(20000)
    else:
        data=DB.get_restaurants_byprice(0)
    if data is None:
        tot_count=0
    else:
        tot_count=len(data)

    if tot_count<=limit:
        data = dict(list(data.items())[:tot_count])
    else:
        data = dict(list(data.items())[start_idx:end_idx])
    data=dict(sorted(data.items(), key=lambda x:x[1]['name'], reverse=False))
    page_count = len(data)
    print(tot_count,page_count)
    
    avgRate_list=[]
    for res in data.values():
        print("루프")
        print(res)
        print(res['name'])
        avg_rate=DB.get_avgrate_byname(str(res['name']))
        print(avg_rate)
        avgRate_list.append(avg_rate)
    return render_template("EDrecommendResult.html", datas=data.items(), data_cost=result,
                           total=tot_count, avg_rate=avgRate_list, limit=limit, page=page, page_count=math.ceil(tot_count/6))

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)



