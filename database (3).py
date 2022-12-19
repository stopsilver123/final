import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
            
            firebase = pyrebase.initialize_app(config)
            self.db = firebase.database()

    """ 맛집 """
    def insert_restaurant(self, name, data, img_path): 
        restaurant_info ={
            "name": name,
            "category": data['category'], 
            "hashtag_category": data['hashtag_category'],
            "postcode": data['postcode'],
            "Addr": data['address'],
            "detailAddr": data['detailAddress'],
            "extraAddr": data['extraAddress'],
            "tel": data['telephone_number'],
            "img_path": "static/images/"+img_path,
            "stime" : data['start_time'], 
            "ftime": data['finish_time'], 
            "site": data['urlsite'], 
            "park": data['parking'],
            "avgprice": data['avgprice'],
            "heart_count": 0
        }

        if self.restaurant_duplicate_check(name): #등록가능
            self.db.child("restaurant").push(restaurant_info) #restaurant라는 이름의 테이블에서 name 키를 에대해
            #print(data,img_path)
            return True
        else:
            return False

    def restaurant_duplicate_check(self ,name):
        restaurants = self.db.child("restaurant").get() #restaurant라는 테이블 안의 정보 모두 get
        print("중복확인시작")
        print(restaurants)
        print("key는 ")
        print(restaurants.key())
        print("val은 ")
        print(restaurants.val())
        
        if restaurants.val() is None: #데이터베이스가 아예 비어있는 경우
            print("DB에 아무것도 없다")
            return True # ->바로 등록 가능
        else:                
            for res in restaurants.each():
                value = res.val()
                print("루프ㄱ")
                print(res.key())
                if value['name'] == name: #res.key()는 식당이름(키)
                    return  False #동일한 이름이 없다 -> 등록 불가
            print("루프끝, 같은 이름 없음")    
            return True                       #-> 등록 가능
                                     
    def get_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        print("get_restaurants함수값")
        #print(restaurants)
        return restaurants
        
    def get_restaurant_byname(self, name):
        restaurants = self.db.child("restaurant").get()
        target_value=""
        for res in restaurants.each():
            value = res.val()
                
            if value['name'] == name:
                target_value=value
        return target_value

    def get_avgrate_byname(self,name):
        reviews = self.db.child("review").get()
        rates=[]
        if reviews.val() is None: #데이터베이스가 아예 비어있는 경우
            print("DB리뷰에 아무것도 없다")
            return 0.0 
        else: 
            for res in reviews.each():
                value = res.val()
                if value['restaurant_name'] == name:
                    rates.append(float(value['rating']))
            if len(rates) == 0:
                divisor=1
            else:
                divisor=len(rates)
            rated=sum(rates)/divisor
            return round(rated,2)
        
        
    def get_restaurants_byHeartCount(self):
        #restaurants = self.db.child("restaurant").order_by_child("heart_count").limit_to_first(3).get()
        restaurants = self.db.child("restaurant").get()
        print(restaurants)
        before = []
        after = []
        result = []
        for res in restaurants.each():
            R_info = res.val()
            if R_info['heart_count'] > 0:
                before.append((R_info['name'], R_info['heart_count']))
                
        after = sorted(before, key = lambda x : x[1], reverse=True)
        print(after)
        print(after[0][0])
        for x in range(4):
            result.append(after[x][0])
        print(result)
        return result
            
    """    메뉴    """
    def insert_menu(self, name, data, img_path): 
        menu_info ={
            "restaurant_name": data['restaurant_name'],
            "name": data['foodname'],
            "img_path": "static/images/"+img_path, 
            "price": data['price'], 
            "description": data['desc'], 
            "category": data['category'],
            "allergy":data['allergy'],
            "foodhash":data['foodhash'],
            "extra":data['extra']
        }
        
        restname = data['restaurant_name']
        
        if self.menu_duplicate_check(name, restname): #name: 메뉴명
            self.db.child("menu").push(menu_info)
            print(data,img_path)
            return True
        else:
            return False
    
    
    def menu_duplicate_check(self, name, restaurantname):
        menus = self.db.child("menu").get()
        print("메뉴중복확인시작")
        
        if menus.val() is None: #데이터베이스가 아예 비어있는 경우
            print("메뉴db에 아무것도 없다")
            return True # ->바로 등록 가능
        else:                
            for res in menus.each():
                print("루프ㄱ")
                print(res.key())
                
                if res.val()['restaurant_name'] == restaurantname:
                    if res.key() == name: #res.key()는 음식이름(키)
                        return False #동일한 이름이 있다 -> 등록 불가
                    else:
                        continue
                else:
                    continue
                    
            print("루프끝, 같은 이름 없음")    
            return True                       #-> 등록 가능
        
    def get_menu_byresname(self,name):
        menus=self.db.child("menu").get()
        target_value=[]
        
        if menus.val() is None:
            return target_value
        else:
            for res in menus.each():
                value=res.val()
                
                if value['restaurant_name']==name:
                    target_value.append(value)
            return target_value
                     
    def get_mainmenu_byrestname(self,name):
        menus=self.db.child("menu").get()
        target_value=[]
        
        if menus.val() is None:
            return target_value
        else:
            for res in menus.each():
                value=res.val()
                
                if value['restaurant_name']==name:
                    if value['category']=="main":
                        target_value.append(value)
            return target_value
    
    def get_sidemenu_byrestname(self,name):
        menus=self.db.child("menu").get()
        target_value=[]
        
        if menus.val() is None:
            return target_value
        else:
            for res in menus.each():
                value=res.val()
                
                if value['restaurant_name']==name:
                    if value['category']=="side":
                        target_value.append(value)
        return target_value
    
    
    """    리뷰    """    
    def insert_review(self, data, img_path): #name은 음식이름
        review_info ={
            "restaurant_name": data['restaurant_name'], 
            "foodname": data['foodname'],
            "rating": data['rating'],
            "description": data['review'],
            "writer": data['writer'],
            "img_path": "static/images/"+img_path,
            "heart_count": 0
            
        }
        #"img_path": img_path
        self.db.child("review").push(review_info)
        print(data, img_path)
        return True

    
    def get_review_byresname(self, resname):
        reviews=self.db.child("review").get()
        target_value=[]
        if reviews.val() is None: #데이터베이스가 아예 비어있는 경우
            print("DB리뷰에 아무것도 없다")
            return target_value
        else:
            for res in reviews.each():
                value=res.val()
            
                if value['restaurant_name']==resname:
                    print(value)
                    target_value.append(value)
                
            return target_value
        
        """ 카테고리 sorting"""
    def get_restaurants_bycategory(self, cate):
        restaurants = self.db.child("restaurant").get()
        target_value=[]
        #if restaurants.val() is None:
            #return target_value
        #else:
        for res in restaurants.each():
            value = res.val()    
            if value['category'] == cate:
                target_value.append(value)
        print("######target_value",target_value)
        new_dict={}
        for k,v in enumerate(target_value):
            new_dict[k]=v

        return new_dict
            
    
    """회원가입"""
    
    def insert_user(self, data, pw):
        user_info ={
        "id": data['id'],
        "pw": pw,
        "nickname": data['nickname'],
        "pick_restaurant": ""
        }
    
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False
          
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        
        print("users###", users.val())
        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()
        
                if value['id'] == id_string:
                    return False
            return True
        
    """로그인"""
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
                
            if value['id'] == id_ and value['pw'] == pw_:
                return True
            
        return False
    
    
    """찜 관련"""
    #찜한 식당 리스트
    def get_restaurant_bypicked(self, user_id):
        all_users = self.db.child("user").get()
        target_value=[] 
        keyCheck = "pick_restaurant"

        for res in all_users.each():
            user_unikey = res.key()
            user_info = res.val()

            if user_info['id'] == user_id:
                if keyCheck not in list(user_info.keys()):
                    self.db.child("user").child(user_unikey).update({"pick_restaurant": ""})
                    user_pick = [0]
                else:
                    user_pick = user_info['pick_restaurant'] #user 안의 picked 키 안의 식당명 리스트
                    
                break
        
        restaurants = self.db.child("restaurant").get() 
        if restaurants.val() is None: #데이터베이스가 아예 비어있는 경우
            print("restaurantDB에 아무것도 없다")
        else:                
            for res in restaurants.each():
                #print("루프ㄱ")
                #print(res.key())
                #print(res.val())
                
                for pick in user_pick:
                    if pick == res.val()['name']:
                        print(pick)
                        target_value.append(res.val())
                        print("붙임")
                    else:
                        continue
        
        new_dict={}
        for k,v in enumerate(target_value):
            new_dict[k]=v

        return new_dict
    
    
    #찜하기/찜취소 - 유저데이터변경
    def turn_picked(self, restaurant_name, user_name, heart):
        users = self.db.child("user").get()

        keyCheck = "pick_restaurant"
        user_pick=[]
        
        for res in users.each():
            user_unikey = res.key()
            user_info = res.val()
            print(user_info)
            #print("user_info") #print(user_info) #print(user_info['id'])
            #print(user_info.keys()) #결과: dict_keys(['id', 'nickname', 'pick_restaurant', 'pw'])
            
            if user_info['id'] == user_name:
                if keyCheck not in list(user_info.keys()):
                    
                    self.db.child("user").child(user_unikey).update({"pick_restaurant": restaurant_name})
                    break
                    
                if user_info['pick_restaurant'] == "":
                    if heart == "ON":
                        user_pick.append(restaurant_name)
                        print("빈리스트에붙임")
                        self.db.child("user").child(user_unikey).update({"pick_restaurant": user_pick})
                    elif heart == "OFF":
                        break
                    break
                    
                else:
                    for pick in user_info['pick_restaurant']:
                        print("for루프")
                        print(pick)
                        if pick == restaurant_name:
                            continue
                        else:
                            user_pick.append(pick)
                            print("다른식당붙임")
                    if heart == "ON":
                        user_pick.append(restaurant_name)
                        print("하트붙임")
                    self.db.child("user").child(user_unikey).update({"pick_restaurant": user_pick})
                    break
                break
                
        return True
    
    #찜하기/찜취소 - 식당하트수 변경
    def turn_pick_restaurant_count(self, restaurant_name, heart):
        restaurants = self.db.child("restaurant").get()

        keyCheck = "pick_restaurant"
        user_pick=[]
        
        for res in restaurants.each():
            restaurant_unikey = res.key()
            restaurant_info = res.val()
            print(restaurant_info)
            #print("user_info") #print(user_info) #print(user_info['id'])
            #print(user_info.keys()) #결과: dict_keys(['id', 'nickname', 'pick_restaurant', 'pw'])
            heartCount = restaurant_info['heart_count']
            if restaurant_info['name'] == restaurant_name:
                print(restaurant_info['name'])
                print(restaurant_info['heart_count'])
                if restaurant_info['heart_count'] >= 1:
                    if heart == "ON":
                        heartCount += 1
                    elif heart == "OFF":
                        heartCount -= 1
                    self.db.child("restaurant").child(restaurant_unikey).update({"heart_count": heartCount})
                    
                else: #heartCount == 0
                    if heart == "ON":
                        self.db.child("restaurant").child(restaurant_unikey).update({"heart_count": 1})
                    elif heart == "OFF":
                        continue                    
                        
                break
                
        return True       
        
    def restaurant_and_heart(self, user_id):
        all_users = self.db.child("user").get()
        target_value=[]
        
        for res in all_users.each():
            user_info = res.val()
            if user_info['id'] == user_id:
                target_value = user_info['pick_restaurant']
                break
                
        print(target_value)
        return target_value
    
    """ 별점 받아오기 """
    
    def get_rate_byname(self,name):
        reviews = self.db.child("review").get()
        rates=[]
        if reviews.val() is None: #데이터베이스가 아예 비어있는 경우
            print("DB리뷰에 아무것도 없다")
            return 0.0 
        else: 
            for res in reviews.each():
                value = res.val()
                if value['restaurant_name'] == name:
                    rates.append(value['rating'])
            return rates 
        
    """ 가격대 sorting """
    def get_restaurants_byprice(self, result):
        restaurants = self.db.child("restaurant").get()
        target_value=[]
        price = 0
        if result == 5000:
            price="5000원"
        elif result == 7000:
            price="7000원"
        elif result == 10000:
            price="10000원"
        elif result == 15000:
            price="15000원"
        elif result == 20000:
            price="20000원"
        else:
            price="0원"
        
        for res in restaurants.each():
            value=res.val()
            if value['avgprice']==price:
                target_value.append(value)
        #print("####target_value", target_value)
        new_dict={}
        for k,v in enumerate(target_value):
            new_dict[k]=v
            
        print(new_dict)
        return new_dict
            
            