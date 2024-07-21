from posixpath import join
from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import random
import time
import os

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['ADMIN_PW'] = os.urandom(8)
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    coins = db.Column(db.Float, default=100000000000)
    bits = db.Column(db.Float, default=0)
    rank = db.Column(db.String(20), default='non')
    combat_exp = db.Column(db.Float, default=0)
    combat_level = db.Column(db.Float, default=0)
    mining_exp = db.Column(db.Float, default=0)
    mining_level=db.Column(db.Float, default=0)
    foraging_exp=db.Column(db.Float, default=0)
    foraging_level=db.Column(db.Float, default=0)
    fishing_exp=db.Column(db.Float, default=0)
    fishing_level=db.Column(db.Float, default=0)
    enchanting_exp=db.Column(db.Float, default=0)
    enchanting_level=db.Column(db.Float, default=0)
    alchemy_exp=db.Column(db.Float, default=0)
    alchemy_level=db.Column(db.Float, default=0)
    farming_exp=db.Column(db.Float, default=0)
    farming_level=db.Column(db.Float, default=0)
    runecrafting_exp=db.Column(db.Float, default=0)
    runecrafting_level=db.Column(db.Float, default=0)
    taming_exp=db.Column(db.Float, default=0)
    taming_level=db.Column(db.Float, default=0)
    carpentry_exp=db.Column(db.Float, default=0)
    carpentry_level=db.Column(db.Float, default=0)
    social_exp=db.Column(db.Float, default=0)
    social_level=db.Column(db.Float, default=0)
    catacombs_exp=db.Column(db.Float, default=0)
    catacombs_level=db.Column(db.Float, default=0)
    grind_level=db.Column(db.Float, default=1)
    base_health=db.Column(db.Float, default=100)
    health=db.Column(db.Float, default=100)
    base_defense=db.Column(db.Float, default=0)
    defense=db.Column(db.Float, default=0)
    truedefese=db.Column(db.Float, default=0)
    base_strength=db.Column(db.Float, default=0)
    strength=db.Column(db.Float, default=0)
    critchance=db.Column(db.Float, default=0.3)
    critdamage=db.Column(db.Float, default=1.5)
    intellegence=db.Column(db.Float, default=0)
    miningspeed=db.Column(db.Float, default=0)
    seacreaturechance=db.Column(db.Float, default=0.2)
    magicfind=db.Column(db.Float, default=0)
    petluck=db.Column(db.Float, default=0)
    abilitydamage=db.Column(db.Float, default=0)
    ferocity=db.Column(db.Float, default=0)
    miningfortune=db.Column(db.Float, default=0)
    farmingfortune=db.Column(db.Float, default=0)
    foragingfortune=db.Column(db.Float, default=0)
    sword_used=db.Column(db.String(255), nullable=True, default=None)
    bow_used=db.Column(db.String(255), nullable=True, default=None)
    arrow_used=db.Column(db.String(255), nullable=True, default=None)
    arrow_bonus=db.Column(db.Float, default=0)
    bpc=db.Column(db.Float, default=2000)
    waiting=db.Column(db.Boolean, nullable=True, default=None)
    reforge = db.Column(db.String(255), nullable=True, default='None')
    rarity = db.Column(db.Float, default=0)
    pickaxe=db.Column(db.String(255), nullable=True, default='None')
    pickaxe_speed=db.Column(db.Float, default=0)


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        username = request.form['username']
        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()
        if not user:
            # Create a new user if not exists
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        # Render the template with user's data
        session["username"] = username
        return render_template('hub.html', user=user)
    return render_template('start.html')

# Rank system
@app.route('/rank', methods=['POST', 'GET'])
def ranks():
    rank = User.query.get(session["username"]).rank
    return render_template('ranks.html', rank=rank)

@app.route('/vip', methods=['POST', 'GET'])
def vip():
    rank = User.query.get(session["username"]).rank
    if rank != 'non':
        return '''You already have Vip or higher.<br>
    <a href="/rank">Back</a>'''
    else:
        coins = User.query.get(session["username"]).coins
        bits = User.query.get(session["username"]).bits
        bpc = User.query.get(session["username"]).bpc
        if coins >= 1000000:
            coins -= 1000000
            rank = 'vip'
            bits += 500
            bpc += 100
            db.session.commit()
            return '''You purchased Vip!<br>
    <a href="/rank">Back</a>'''
        else:
            return '''You cannot afford Vip.<br>
    <a href="/rank">Back</a>'''
    db.session.commit()
@app.route('/vip+', methods=['POST', 'GET'])
def vip2():
    rank = User.query.get(session["username"]).rank
    if rank != 'non' and rank != 'vip':
        return '''You already have Vip+ or higher.<br>
    <a href="/rank">Back</a>'''
    elif rank == 'non':
        return '''You must buy Vip before you buy Vip+.<br>
    <a href="/rank">Back</a>'''
    else:
        coins = User.query.get(session["username"]).coins
        bits = User.query.get(session["username"]).bits
        bpc = User.query.get(session["username"]).bp
        if coins >= 200000:
            coins -= 200000
            rank = 'vip+'
            bits += 1500
            bpc += 300
            db.session.commit()
            return '''You purchased Vip+!<br>
    <a href="/rank">Back</a>'''
        else:
            return '''You cannot afford Vip+.<br>
    <a href="/rank">Back</a>'''

@app.route('/mvp', methods=['POST', 'GET'])
def mvp():
    rank = User.query.get(session["username"]).rank
    if rank != 'non' and rank != 'vip' and rank != 'vip+':
        return '''You already have Mvp or higher.<br>
    <a href="/rank">Back</a>'''
    elif rank != 'vip+':
        return '''You must buy Vip+ before you buy Mvp.<br>
    <a href="/rank">Back</a>'''
    else:
        coins = User.query.get(session["username"]).coins
        bits = User.query.get(session["username"]).bits
        bpc = User.query.get(session["username"]).bpc
        if coins >= 500000:
            coins -= 500000
            rank = 'mvp'
            bits += 2500
            bpc += 500
            db.session.commit()
            return '''You purchased Mvp!<br>
    <a href="/rank">Back</a>'''
        else:
            return '''You cannot afford Mvp.<br>
    <a href="/rank">Back</a>'''

@app.route('/mvp+', methods=['POST', 'GET'])
def mvp2():
    rank = User.query.get(session["username"]).rank
    if rank == 'mvp+' or rank == 'mvp++' or rank == 'youtuber':
        return '''You already have Mvp+ or higher.<br>
    <a href="/rank">Back</a>'''
    elif rank != 'mvp':
        return '''You must buy Mvp before you buy Mvp+.<br>
    <a href="/rank">Back</a>'''
    else:
        coins = User.query.get(session["username"]).coins
        bits = User.query.get(session["username"]).bits
        bpc = User.query.get(session["username"]).bpc
        if coins >= 1000000:
            coins -= 1000000
            rank = 'mvp+'
            bits += 5000
            bpc += 1000
            db.session.commit()
            return '''You purchased Mvp+!<br>
    <a href="/rank">Back</a>'''
        else:
            return '''You cannot afford Mvp+.<br>
    <a href="/rank">Back</a>'''

@app.route('/mvp++', methods=['POST', 'GET'])
def mvp3():
    rank = User.query.get(session["username"]).rank
    if rank == 'mvp++' or rank == 'youtuber':
        return '''You already have Mvp++ or higher.<br>
    <a href="/rank">Back</a>'''
    elif rank != 'mvp+':
        return '''You must buy Mvp+ before you buy Mvp++.<br>
    <a href="/rank">Back</a>'''
    else:
        coins = User.query.get(session["username"]).coins
        bits = User.query.get(session["username"]).bits
        bpc = User.query.get(session["username"]).bpc
        if coins >= 2000000:
            coins -= 2000000
            rank = 'mvp++'
            bits += 10000
            bpc += 2000
            db.session.commit()
            return '''You purchased Mvp++!<br>
    <a href="/rank">Back</a>'''
        else:
            return '''You cannot afford Mvp++.<br>
    <a href="/rank">Back</a>'''

@app.route('/youtube', methods=['POST', 'GET'])
def youtube():
    rank = User.query.get(session["username"]).rank
    bits = User.query.get(session["username"]).bits
    bpc = User.query.get(session["username"]).bpc
    waiting = User.query.get(session["username"]).waiting
    if waiting is True:
        seconds = 86400
        while seconds != 0:
            time.sleep(1)
            seconds-=1
        waiting=False
        return render_template('waiting.html', seconds=seconds)
    if rank == "youtuber":
        return '''You already have youtuber rank.<br>
               <a href="/rank">Back</a>'''
    elif rank != "mvp++":
        return '''You must buy Mvp++ before you get youtuber rank.<br>
               <a href="/rank">Back</a>'''
    password = input(f'''
                User from {request.remote_addr} with Username {session["username"]}
                requested youtuber rank
                Please enter admin passowrd: ''')
    if password == app.config['ADMIN_PW']:
        rank = 'youtuber'
        bits += 50000
        bpc += 3000
        db.session.commit()
        return '''Sucessfully given you "youtuber" rank.<br>
                  <a href="/rank">Back</a>'''
    elif password is not None and password != app.config['ADMIN_PW']:
        waiting = True
        return '''Sorry, the admin entered the wrong password. Rejected. Try again later.<br>
               <a href="/rank">Back</a>'''
    return '''Wait for the admin to enter the password.<br>
              <a href="/rank">Back</a>'''

@app.route('/sellbits', methods=['POST', 'GET'])
def sellbits():
    bits = User.query.get(session["username"]).bits
    bpc = User.query.get(session["username"]).bpc
    return render_template('bit.html', bpc=bpc, bits=bits)

@app.route('/combatbuybits', methods=['POST', 'GET'])
def combatbuy():
    global combat_level
    bits = User.query.get(session["username"]).bits
    combat_level = User.query.get(session["username"]).combat_level
    if bits >= 5000:
        bits -= 5000
        combat_level += 1
        db.session.commit()
        return '''Your purchase was sucssesful<br>
                  <a href="/sellbits">Back</a>'''
    else:
        return '''You do not have enough bits.<br> 
               <a href="/sellbits">Back</a>'''

@app.route('/combatbuybits2', methods=['POST', 'GET'])
def combatbuy2():
    bits = User.query.get(session["username"]).bits
    combat_level = User.query.get(session["username"]).combat_level
    if bits >= 15000:
        bits -= 15000
        combat_level += 4
        db.session.commit()
        return '''Your purchase was sucssesful<br>
                  <a href="/sellbits">Back</a>'''
    else:
        return '''You do not have enough bits.<br> 
               <a href="/sellbits">Back</a>'''

@app.route('/cookie', methods=['POST', 'GET'])
def cookie_buy():
    coins = User.query.get(session["username"]).coins
    bits = User.query.get(session["username"]).bits
    if coins >= 300000:
        coins -= 300000
        bits += bpc
        db.session.commit()
        return '''Sucssfully given you bits.<br>
               <a href="/sellbits">Back</a>'''
    else:
        return '''You cannot afford a cookie.<br>
               <a href="/sellbits">Back</a>'''

# Weaponsmith
@app.route('/weaponsmith', methods=['POST', 'GET'])
def weapon_smith():
    sword_used = User.query.get(session["username"]).sword_used
    arrow_used = User.query.get(session["username"]).arrow_used
    bow_used = User.query.get(session["username"]).bow_used
    pickaxe = User.query.get(session["username"]).pickaxe
    combat_level = User.query.get(session["username"]).combat_level
    strength = User.query.get(session["username"]).strength
    return render_template('weaponsmith.html', su=sword_used, ar=arrow_used, bow=bow_used, pickaxe=pickaxe, combat_level=combat_level, st=strength)

@app.route('/us', methods=['POST', 'GET'])
def us():
    sword_used = User.query.get(session["username"]).sword_used
    arrow_used = User.query.get(session["username"]).arrow_used
    bow_used = User.query.get(session["username"]).bow_used
    strength = User.query.get(session["username"]).strength
    coins = User.query.get(session["username"]).coins
    rarity = User.query.get(session["username"]).rarity


    if sword_used == 'undead_sword':
        return '''You already have the undead sword equipped.<br>
               <a href="/weaponsmith">Back</a>'''
    if coins >= 100:
        coins -= 100
        strength = base_strength + 30
        sword_used = 'undead_sword'
        bow_used = None
        arrow_used = None
        rarity = 1
        db.session.commit()
        return '''You purchased the undead sword!<br>
               <a href="/weaponsmith">Back</a>'''
    else:
        return '''You cannot afford the undead sword.<br>
               <a href="/weaponsmith">Back</a>'''

@app.route('/es', methods=['POST', 'GET'])
def es():
    word_used = User.query.get(session["username"]).sword_used
    arrow_used = User.query.get(session["username"]).arrow_used
    bow_used = User.query.get(session["username"]).bow_used
    strength = User.query.get(session["username"]).strength
    coins = User.query.get(session["username"]).coins
    rarity = User.query.get(session["username"]).rarity
    if sword_used == 'end_sword':
        return '''You already have the end sword equipped.<br>
               <a href="/weaponsmith">Back</a>'''
    if coins >= 150:
        coins -= 150
        strength = base_strength + 35
        sword_used = 'end_sword'
        bow_used = None
        arrow_used = None
        rarity = 2
        db.session.commit()
        return '''You purchased the end sword!<br>
               <a href="/weaponsmith">Back</a>'''
    else:
        return '''You cannot afford the end sword.<br>
               <a href="/weaponsmith">Back</a>'''

@app.route('/ss', methods=['POST', 'GET'])
def ss():
    global coins, strength, sword_used, bow_used, arrow_used, rarity
    if sword_used == 'spider_sword':
        return '''You already have the spider sword equipped.<br>
               <a href="/weaponsmith">Back</a>'''
    if coins >= 100:
        coins -= 100
        strength = base_strength + 30
        sword_used = 'spider_sword'
        bow_used = None
        arrow_used = None
        rarity = 1
        return '''You purchased the spider sword!<br>
               <a href="/weaponsmith">Back</a>'''
    else:
        return '''You cannot afford the spider sword.<br>
               <a href="/weaponsmith">Back</a>'''

@app.route('/ds', methods=['POST', 'GET'])
def ds():
    global coins, strength, sword_used, bow_used, arrow_used, rarity
    if sword_used == 'diamond_sword':
        return '''You already have the diamond sword equipped.<br>
               <a href="/weaponsmith">Back</a>'''
    if coins >= 60:
        coins -= 60
        strength = base_strength + 35
        sword_used = 'diamond_sword'
        bow_used = None
        arrow_used = None
        rarity = 2
        return '''You purchased the diamond sword!<br>
               <a href="/weaponsmith">Back</a>'''
    else:
        return '''You cannot afford the diamond sword.<br>
               <a href="/weaponsmith">Back</a>'''

@app.route('/bow', methods=['POST', 'GET'])
def bow():
    global coins, strength, sword_used, bow_used, rarity
    if bow_used == 'bow':
        return '''You already have a bow equipped.<br>
               <a href="/weaponsmith">Back</a>'''
    if coins >= 25:
        coins -= 25
        strength = base_strength + 30
        sword_used = None
        bow_used = 'bow'
        rarity = 1
        return '''You purchased a bow!<br>
               <a href="/weaponsmith">Back</a>'''
    else:
        return '''You cannot afford a bow.<br>
               <a href="/weaponsmith">Back</a>'''

@app.route('/flintar', methods=['POST', 'GET'])
def flintar():
    global coins, strength, sword_used, arrow_used, arrow_bonus
    if coins >= 1000:
        coins -= 1000
        if bow_used is not None and arrow_used is None:
            strength += 1
        elif bow_used is None and arrow_used is not None:
            if arrow_used == 'flintarrow':
                return '''You already have flint arrows equipped.<br>
                          <a href="/weaponsmith">Back</a>'''
            strength -= arrow_bonus
            strength += 1
        elif bow_used is not None and arrow_used is not None:
            if arrow_used == 'flintarrow':
                return '''You already have flint arrows equipped.<br>
                          <a href="/weaponsmith">Back</a>'''
            strength -= arrow_bonus
            strength += 1

        else:
            return '''You have a sword equipped. [Error 5726: Two items do not collaterate.]<br>
                   <a href="/weaponsmith">Back</a>'''
        sword_used = None
        arrow_used = 'flintarrow'
        arrow_bonus = 1
        return '''You purchased flint arrows!<br>
               <a href="/weaponsmith">Back</a>'''
    else:
        return '''You cannot afford flint arrows.<br>
               <a href="/weaponsmith">Back</a>'''

@app.route('/witherb', methods=['POST', 'GET'])
def witherbow():
    global coins, strength, sword_used, bow_used, rarity
    if bow_used == 'wither_bow':
        return '''You already have the wither bow equipped.<br>
               <a href="/weaponsmith">Back</a>'''
    if coins >= 250:
        coins -= 250
        strength = base_strength + 30
        sword_used = None
        bow_used = 'wither_bow'
        rarity = 2
        return '''You purchased the wither bow!<br>
               <a href="/weaponsmith">Back</a>'''
    else:
        return '''You cannot afford the wither bow.<br>
               <a href="/weaponsmith">Back</a>'''

@app.route('/artisanalshortb', methods=['POST', 'GET'])
def artisanalshortbow():
    global coins, strength, sword_used, bow_used, rarity
    if bow_used == 'artisanal_shortbow':
        return '''You already have the artisanal shortbow equipped.<br>
               <a href="/weaponsmith">Back</a>'''
    if combat_level < 4:
        return '''You don't have combat 4.<br>
               <a href="/weaponsmith">Back</a>'''
    elif coins >= 600:
        coins -= 600
        strength = base_strength + 40
        sword_used = None
        bow_used = 'artisanal_shortbow'
        rarity = 3
        return '''You purchased the artisanal shortbow!<br>
               <a href="/weaponsmith">Back</a>'''
    else:
        return '''You cannot afford the artisanal shortbow.<br>
               <a href="/weaponsmith">Back</a>'''

@app.route('/stonepick', methods=['POST', 'GET'])
def stonepick():
    global coins, pickaxe_speed, pickaxe
    if pickaxe == 'stone_pickaxe':
        return '''You already have the stone pickaxe equipped.<br>
               <a href="/weaponsmith">Back</a>'''
    elif coins >= 12:
        coins -= 12
        pickaxe = 'stone_pickaxe'
        pickaxe_speed = 2
        return '''You purchased the stone pickaxe!<br>
               <a href="/weaponsmith">Back</a>'''
    else:
        return '''You cannot afford the stone pickaxe.<br>
               <a href="/weaponsmith">Back</a>'''

@app.route('/ironpick', methods=['POST', 'GET'])
def ironpick():
    global coins, pickaxe_speed, pickaxe
    if pickaxe == 'iron_pickaxe':
        return '''You already have the iron pickaxe equipped.<br>
               <a href="/weaponsmith">Back</a>'''
    elif coins >= 35:
        coins -= 35
        pickaxe = 'iron_pickaxe'
        pickaxe_speed = 3
        return '''You purchased the iron pickaxe!<br>
               <a href="/weaponsmith">Back</a>'''
    else:
        return '''You cannot afford the iron pickaxe.<br>
               <a href="/weaponsmith">Back</a>'''

@app.route('/goldpick', methods=['POST', 'GET'])
def goldpick():
    global coins, pickaxe_speed, pickaxe
    if pickaxe == 'gold_pickaxe':
        return '''You already have the gold pickaxe equipped.<br>
               <a href="/weaponsmith">Back</a>'''
    elif coins >= 18:
        coins -= 18
        pickaxe = 'gold_pickaxe'
        pickaxe_speed = 4
        return '''You purchased the gold pickaxe!<br>
               <a href="/weaponsmith">Back</a>'''
    else:
        return '''You cannot afford the gold pickaxe.<br>
               <a href="/weaponsmith">Back</a>'''

@app.route('/blacksmith', methods=['POST', 'GET'])
def blacksmith():
    global coinamount
    if rarity == 1:
        coinamount = 250
    elif rarity == 2:
        coinamount = 500
    elif rarity == 3:
        coinamount = 1000
    elif rarity == 4:
        coinamount = 2500
    elif rarity == 5:
        coinamount = 5000
    elif rarity == 6:
        coinamount = 10000
    elif rarity == 7:
        coinamount = 15000
    elif rarity == 10:
        coinamount = 50000
    else:
        return '''You need to equip a bow or sword to reforge.<br>
               <a href="/start">Back</br>'''
    if request.method == 'POST':
        global reforge, strength, critchance, critdamage, intellegence, coins, intellegence
        number1 = random.randint(1, 9)
        coins -= coinamount
        if number1 == 1:
            if reforge == 'Gentle':
                coins += coinamount
                return '''You already have the gentle reforge on. Please try again.<br>
                       <a href="/blacksmith">Back</a>'''
            strength += 3*rarity
            reforge = 'Gentle'
        elif number1 == 2:
            if reforge == 'Odd':
                coins += coinamount
                return '''You already have the odd reforge on. Please try again.<br>
                       <a href="/blacksmith">Back</a>'''
            critchance += 0.12*rarity 
            critdamage += 0.1*rarity+1
            intellegence -= 5*rarity
            reforge = 'Odd'
        elif number1 == 3:
            if reforge == 'Genuis':
                coins += coinamount
                return '''You already have the genuis reforge on. Please try again.<br>
                       <a href="/blacksmith">Back</a>'''
            intellegence += 30*rarity
            reforge = 'Genuis'
        elif number1 == 4:
            if reforge == 'Fair':
                coins += coinamount
                return '''You already have the fair reforge on. Please try again.<br>
                       <a href="/blacksmith">Back</a>'''
            strength +=  2*rarity
            critchance += 0.02*rarity
            critdamage += 0.02*rarity+1
            intellegence += 2*rarity
            reforge = 'Fair'
        elif number1 == 5:
            if reforge == 'Epic':
                coins += coinamount
                return '''You already have the epic reforge on. Please try again.<br>
                       <a href="/blacksmith">Back</a>'''
            strength += 15*rarity
            critdamage += 0.1*rarity+1
            reforge = 'Epic'
        elif number1 == 6:
            if reforge == 'Sharp':
                coins += coinamount
                return '''You already have the epic reforge on. Please try again.<br>
                       <a href="/blacksmith">Back</a>'''
            critchance += 0.1*rarity
            critdamage += 0.2*rarity+1
            reforge = 'Sharp'
        elif number1 == 7:
            if reforge == 'Heroic':
                coins += coinamount
                return '''You already have the heroic reforge on. Please try again.<br>
                       <a href="/blacksmith">Back</a>'''
            strength += 15*rarity
            intellegence += 40
            reforge = 'Heroic'
        elif number1 == 8:
            if reforge == 'Spicy':
                coins += coinamount
                return '''You already have the spicy reforge on. Please try again.<br>
                       <a href="/blacksmith">Back</a>'''
            strength += 2*rarity
            critchance += 0.01*rarity
            critdamage += 0.25*rarity+1
            reforge = 'Spicy'
        elif number1 == 9:
            if reforge == 'Legendary':
                coins += coinamount
                return '''You already have the legendary reforge on. Please try again.<br>
                       <a href="/blacksmith">Back</a>'''
            strength += 3*rarity
            critchance += 0.05*rarity
            critdamage += 0.05*rarity
            intellegence += 5*rarity
            reforge = 'Legendary'
    return render_template('blacksmith.html', reforge=reforge)

@app.route('/rosetta')
def rossetta():
    return

# Save

@app.route('/save', methods=['POST', 'GET'])
def save():
    global save_code, coins, bits, combat_level, mining_level, foraging_level, fishing_level, enchanting_level, alchemy_level, farming_level, runecrafting_level, taming_level, carpentry_level, social_level, catacombs_level, grind_level, reforge
    save_code = ''
    success = 'No'
    if request.method == 'POST':
        save_code = str(coins) + '-' + str(bits) + '-' + str(combat_exp) + '-' + str(combat_level) + '-' + str(mining_exp) + '-' + str(mining_level) + '-' + str(foraging_exp) + '-' + str(foraging_level) + '-' + str(fishing_exp) + '-' + str(fishing_level)  + '-' + str(enchanting_exp) + '-' + str(alchemy_exp) + '-' + str(alchemy_level) + '-' + str(farming_exp) + '-' + str(farming_level) + '-' + str(runecrafting_exp) + '-' + str(runecrafting_level) + '-' + str(taming_exp) + '-' + str(taming_level) + '-' + str(carpentry_exp) + '-' + str(carpentry_level) + '-' + str(social_exp) + '-' + str(social_level) + '-' + str(catacombs_exp) + '-' + str(catacombs_level) + '-' + str(grind_level) + '-' + str(base_health) + '-' + str(health) + '-' + str(base_defense) + '-' + str(defense) + '-' + str(truedefese) + '-' + str(base_strength) + '-' + str(strength) + '-' + str(critchance) + '-' + str(critdamage) + '-' + str(intellegence) + '-' + str(miningspeed) + '-' + str(seacreaturechance) + '-' + str(magicfind) + '-' + str(petluck) + '-' + str(abilitydamage) + '-' + str(ferocity) + '-' + str(miningfortune) + '-' + str(farmingfortune) + '-' + str(sword_used) + '-' + str(bow_used) + '-' + str(arrow_used) + '-' + str(arrow_bonus) + '-' + str(bpc) + '-' + str(waiting) + '-' + rank + '-' + reforge + '-'
        success = 'Yes'
    return render_template('save.html', save_code=save_code, sucess=success)

@app.route('/entersave', methods=['POST', 'GET'])
def enter_code():
    global coins, bits, combat_exp, combat_level, mining_exp, mining_level, foraging_exp, foraging_level, fishing_level, fishing_exp, enchanting_exp, enchanting_level, alchemy_level, alchemy_exp, farming_level, farming_exp, runecrafting_exp, runecrafting_level, taming_exp, taming_level, carpentry_exp, carpentry_level, social_exp, social_level, catacombs_level, catacombs_exp, grind_level, base_health, health, base_defense, defense, truedefese, base_strength, strength, critchance, critdamage, intellegence, miningspeed, seacreaturechance, magicfind, petluck, abilitydamage, ferocity, miningfortune, farmingfortune, foragingfortune, sword_used, bow_used, arrow_used, arrow_bonus, bpc, waiting, rank, reforge, rarity, pickaxe, pickaxe_speed
    if request.method == 'POST':
        coins1 = []
        bits1 = []
        combat11 = []
        combat12 = []
        mining11 = []
        mining12 = []
        foraging11 = []
        foraging12 = []
        fishing11 = []
        fishing12 = []
        enchanting11 = []
        enchanting12 = []
        alchemy11 = []
        alchemy12 = []
        farming11 = []
        farming12 = []
        runecrafting11 = []
        runecrafting12 = []
        taming11 = []
        taming12 = []
        carpentry11 = []
        carpentry12 = []
        social11 = []
        social12 = []
        catacombs11 = []
        catacombs12 = []
        grind_level1 = []
        base_health1 = []
        health1 = []
        base_defense1 = []
        defense1 = []
        truedefese1 = []
        base_strength1 = []
        strength1 = []
        critchance1 = []
        critdamage1 = []
        intellegence1 = []
        miningspeed1 = []
        seacreaturechance1 = []
        magicfind1 = []
        petluck1 = []
        abilitydamage1 = []
        ferocity1 = []
        miningfortune1 = []
        farmingfortune1 = []
        foragingfortune1 = []
        sword_used1 = []
        bow_used1 = []
        arrow_used1 = []
        arrow_bonus1 = []
        bpc1 = []
        waiting1 = []
        rank1 = []
        reforge1 = []
        rarity1 = []
        pickaxe1 = []
        pickaxe_speed1 = []
        save_codel = request.form.get('save_code')
        c = 0
        while c != 58:
            for letter in save_codel:
                if c < 1:
                    if letter == '-':
                        string = ''.join([str(item) for item in coins1])
                        coins = float(string)
                        c += 1
                    else:
                        coins1.append(letter)
                elif c < 2:
                    if letter == '-':
                        string = ''.join([str(item) for item in bits1])
                        bits = float(string)
                        c += 1
                    else:
                        bits1.append(letter)
                elif c < 3:
                    if letter == '-':
                        string = ''.join([str(item) for item in coins1])
                        combat_exp = float(string)
                        c += 1
                    else:
                        combat11.append(letter)
                elif c < 4:
                    if letter == '-':
                        string = ''.join([str(item) for item in combat12])
                        combat_level = float(string)
                        c += 1
                    else:
                        combat12.append(letter)
                elif c < 5:
                    if letter == '-':
                        string = ''.join([str(item) for item in mining11])
                        mining_exp = float(string)
                        c += 1
                    else:
                        mining11.append(letter)
                elif c < 6:
                    if letter == '-':
                        string = ''.join([str(item) for item in mining12])
                        mining_level = float(string)
                        c += 1
                    else:
                        mining12.append(letter)
                elif c < 7:
                    if letter == '-':
                        string = ''.join([str(item) for item in foraging11])
                        foraging_exp = float(string)
                        c += 1
                    else:
                        foraging11.append(letter)
                elif c < 8:
                    if letter == '-':
                        string = ''.join([str(item) for item in foraging12])
                        foraging_level = float(string)
                        c += 1
                    else:
                        foraging12.append(letter)
                elif c < 9:
                    if letter == '-':
                        string = ''.join([str(item) for item in fishing11])
                        fishing_exp = float(string)
                        c += 1
                    else:
                        fishing11.append(letter)
                elif c < 10:
                    if letter == '-':
                        string = ''.join([str(item) for item in fishing12])
                        fishing_level = float(string)
                        c += 1
                    else:
                        fishing12.append(letter)
                elif c < 11:
                    if letter == '-':
                        string = ''.join([str(item) for item in enchanting11])
                        enchanting_exp = float(string)
                        c += 1
                    else:
                        enchanting11.append(letter)
                elif c < 12:
                    if letter == '-':
                        string = ''.join([str(item) for item in enchanting12])
                        enchanting_level = float(string)
                        c += 1
                    else:
                        enchanting12.append(letter)
                elif c < 13:
                    if letter == '-':
                        string = ''.join([str(item) for item in alchemy11])
                        alchemy_exp = float(string)
                        c += 1
                    else:
                        alchemy11.append(letter)
                elif c < 14:
                    if letter == '-':
                        string = ''.join([str(item) for item in alchemy12])
                        alchemy_level = float(string)
                        c += 1
                    else:
                        alchemy12.append(letter)
                elif c < 15:
                    if letter == '-':
                        string = ''.join([str(item) for item in farming11])
                        farming_exp = float(string)
                        c += 1
                    else:
                        farming11.append(letter)
                elif c < 16:
                    if letter == '-':
                        string = ''.join([str(item) for item in farming12])
                        farming_level = float(string)
                        c += 1
                    else:
                        farming12.append(letter)
                elif c < 17:
                    if letter == '-':
                        string = ''.join([str(item) for item in runecrafting11])
                        runecrafting_exp = float(string)
                        c += 1
                    else:
                        runecrafting11.append(letter)
                elif c < 18:
                    if letter == '-':
                        string = ''.join([str(item) for item in runecrafting12])
                        runecrafting_level = float(string)
                        c += 1
                    else:
                        runecrafting12.append(letter)
                elif c < 19:
                    if letter == '-':
                        string = ''.join([str(item) for item in taming11])
                        taming_exp = float(string)
                        c += 1
                    else:
                        taming11.append(letter)
                elif c < 20:
                    if letter == '-':
                        string = ''.join([str(item) for item in farming12])
                        taming_level = float(string)
                        c += 1
                    else:
                        taming12.append(letter)
                elif c < 21:
                    if letter == '-':
                        string = ''.join([str(item) for item in carpentry11])
                        carpentry_exp = float(string)
                        c += 1
                    else:
                        carpentry11.append(letter)
                elif c < 22:
                    if letter == '-':
                        string = ''.join([str(item) for item in carpentry12])
                        carpentry_level = float(string)
                        c += 1
                    else:
                        carpentry12.append(letter)
                elif c < 23:
                    if letter == '-':
                        string = ''.join([str(item) for item in social11])
                        social_exp = float(string)
                        c += 1
                    else:
                        social11.append(letter)
                elif c < 24:
                    if letter == '-':
                        string = ''.join([str(item) for item in social12])
                        social_level = float(string)
                        c += 1
                    else:
                        social12.append(letter)
                elif c < 25:
                    if letter == '-':
                        string = ''.join([str(item) for item in catacombs11])
                        catacombs_exp = float(string)
                        c += 1
                    else:
                        catacombs11.append(letter)
                elif c < 26:
                    if letter == '-':
                        string = ''.join([str(item) for item in catacombs12])
                        catacombs_level = float(string)
                        c += 1
                    else:
                        catacombs12.append(letter)
                elif c < 27:
                    if letter == '-':
                        string = ''.join([str(item) for item in grind_level1])
                        grind_level = float(string)
                        c += 1
                    else:
                        grind_level1.append(letter)
                elif c < 28:
                    if letter == '-':
                        string = ''.join([str(item) for item in base_health1])
                        base_health = float(string)
                        c += 1
                    else:
                        base_health1.append(letter)
                elif c < 29:
                    if letter == '-':
                        string = ''.join([str(item) for item in health1])
                        health = float(string)
                        c += 1
                    else:
                        health1.append(letter)
                elif c < 30:
                    if letter == '-':
                        string = ''.join([str(item) for item in base_defense1])
                        base_defense = float(string)
                        c += 1
                    else:
                        base_defense1.append(letter)
                elif c < 31:
                    if letter == '-':
                        string = ''.join([str(item) for item in defense1])
                        defense = float(string)
                        c += 1
                    else:
                        defense1.append(letter)
                elif c < 32:
                    if letter == '-':
                        string = ''.join([str(item) for item in truedefese1])
                        truedefese = float(string)
                        c += 1
                    else:
                        truedefese1.append(letter)
                elif c < 33:
                    if letter == '-':
                        string = ''.join([str(item) for item in base_strength1])
                        base_strength = float(string)
                        c += 1
                    else:
                        base_strength1.append(letter)
                elif c < 34:
                    if letter == '-':
                        string = ''.join([str(item) for item in strength1])
                        strength = float(string)
                        c += 1
                    else:
                        strength1.append(letter)
                elif c < 35:
                    if letter == '-':
                        string = ''.join([str(item) for item in critchance1])
                        critchance = float(string)
                        c += 1
                    else:
                        critchance1.append(letter)
                elif c < 36:
                    if letter == '-':
                        string = ''.join([str(item) for item in critdamage1])
                        critdamage = float(string)
                        c += 1
                    else:
                        critdamage1.append(letter)
                elif c < 37:
                    if letter == '-':
                        string = ''.join([str(item) for item in intellegence1])
                        intellegence = float(string)
                        c += 1
                    else:
                        intellegence1.append(letter)
                elif c < 38:
                    if letter == '-':
                        string = ''.join([str(item) for item in miningspeed1])
                        miningspeed = float(string)
                        c += 1
                    else:
                        miningspeed1.append(letter)
                elif c < 39:
                    if letter == '-':
                        string = ''.join([str(item) for item in seacreaturechance1])
                        seacreaturechance = float(string)
                        c += 1
                    else:
                        seacreaturechance1.append(letter)
                elif c < 40:
                    if letter == '-':
                        string = ''.join([str(item) for item in magicfind1])
                        magicfind = float(string)
                        c += 1
                    else:
                        magicfind1.append(letter)
                elif c < 41:
                    if letter == '-':
                        string = ''.join([str(item) for item in petluck1])
                        petluck = float(string)
                        c += 1
                    else:
                        petluck1.append(letter)
                elif c < 42:
                    if letter == '-':
                        string = ''.join([str(item) for item in abilitydamage1])
                        abilitydamage = float(string)
                        c += 1
                    else:
                        abilitydamage1.append(letter)
                elif c < 43:
                    if letter == '-':
                        string = ''.join([str(item) for item in ferocity1])
                        ferocity = float(string)
                        c += 1
                    else:
                        ferocity1.append(letter)
                elif c < 44:
                    if letter == '-':
                        string = ''.join([str(item) for item in miningfortune1])
                        miningfortune = float(string)
                        c += 1
                    else:
                        miningfortune1.append(letter)
                elif c < 45:
                    if letter == '-':
                        string = ''.join([str(item) for item in farmingfortune1])
                        print(string)
                        farmingfortune = float(string)
                        c += 1
                    else:
                        farmingfortune1.append(letter)
                elif c < 46:
                    if letter == '-':
                        string = ''.join([str(item) for item in foragingfortune1])
                        foragingfortune = float(string)
                        c += 1
                    else:
                        foragingfortune1.append(letter)
                elif c < 47:
                    if letter == '-':
                        string = ''.join([str(item) for item in sword_used1])
                        sword_used = float(string)
                        c += 1
                    else:
                        sword_used1.append(letter)
                elif c < 48:
                    if letter == '-':
                        string = ''.join([str(item) for item in bow_used1])
                        bow_used = float(string)
                        c += 1
                    else:
                        bow_used1.append(letter)
                elif c < 49:
                    if letter == '-':
                        string = ''.join([str(item) for item in arrow_used1])
                        arrow_used = float(string)
                        c += 1
                    else:
                        arrow_used1.append(letter)
                elif c < 50:
                    if letter == '-':
                        string = ''.join([str(item) for item in arrow_bonus1])
                        arrow_bonus = float(string)
                        c += 1
                    else:
                        arrow_bonus1.append(letter)
                elif c < 51:
                    if letter == '-':
                        string = ''.join([str(item) for item in bpc1])
                        bpc = float(string)
                        c += 1
                    else:
                        bpc1.append(letter)
                elif c < 52:
                    if letter == '-':
                        string = ''.join([str(item) for item in waiting1])
                        waiting = float(string)
                        c += 1
                    else:
                        waiting1.append(letter)
                elif c < 53:
                    if letter == '-':
                        string = ''.join([str(item) for item in rank1])
                        rank = string
                        c += 1
                    else:
                        rank1.append(letter)
                elif c < 54:
                    if letter == '-':
                        string = ''.join([str(item) for item in reforge1])
                        reforge = string
                        c += 1
                    else:
                        reforge1.append(letter)
                elif c < 55:
                    if letter == '-':
                        string = ''.join([str(item) for item in rarity1])
                        rarity = float(string)
                        c += 1
                    else:
                        rarity1.append(letter)
                elif c < 56:
                    if letter == '-':
                        string = ''.join([str(item) for item in pickaxe1])
                        pickaxe = float(string)
                        c += 1
                    else:
                        pickaxe1.append(letter)
                elif c < 57:
                    if letter == '-':
                        string = ''.join([str(item) for item in pickaxe_speed1])
                        pickaxe_speed = float(string)
                        c += 1
                    else:
                        pickaxe_speed1.append(letter)
                else:
                    return render_template('entersave.html', sucsess='Yes')
    return render_template('entersave.html', sucsess='No')

if __name__ == "__main__":
    app.secret_key = 'XL2901'
    app.run(debug=True)
