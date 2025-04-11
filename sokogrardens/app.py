from flask import *
import sms
import pymysql


# initialize the app 
app = Flask(__name__)
app.secret_key="123456780"
connection = pymysql.connect(host='localhost', user = 'root', password='', database='funosokogardens')

@app.route('/vendor', methods=['POST', 'GET'])
def vendor():
      if request.method == 'GET':
            return render_template('vendor.html')
      else:
         firstname=request.form['firstname']
         lastname=request.form['lastname']
         county=request.form['county']
         password1=request.form['password1']
         password2=request.form['password2']
         email=request.form['email']

         # verify password 
         if len(password1) < 8:
            return render_template("vendor.html", error = "password must be at least 8 characters")
         elif password1!= password2:
            return render_template("vendor.html", error="password do not match")
         else:
            sql = "insert into vendors (firstname,lastname,county,password,email) values (%s,%s,%s,%s,%s)"
            cursor = connection.cursor()
            cursor.execute (sql,(firstname,lastname,county,password1,email))
            connection.commit()
            cursor.close()
            return render_template('vendor.html',success = "vendor added  successfully")
               
         
       
    





@app.route('/home')
def Home():
    cursor1 = connection.cursor()
    cursor2=connection.cursor()
    cursor3=connection.cursor()
    # print("Connection Successful")
    sql1 ="select* FROM products where product_category='electronic'"
    sql2 ="select* FROM products where product_category='furniture'"
    sql3 ="select* FROM products where product_category='phones'"

    cursor1.execute(sql1)
    cursor2.execute(sql2)
    cursor3.execute(sql3)
    # fetch rows
    electronic=cursor1.fetchall()
    furniture=cursor2.fetchall()
    phones=cursor3.fetchall()





























    return render_template('home.html' ,electronic=electronic,furniture=furniture, phones=phones)
@app.route('/singleitem/<product_id>')   
def single(product_id):
    connection = pymysql.connect(host='localhost', user = 'root', password='', database='funosokogardens')
    sql="SELECT* FROM products where product_id=%s"
    cursor1= connection.cursor()
    cursor1.execute(sql,(product_id))
    # get single product 
    product=cursor1.fetchone()
    return render_template('single.html',product=product)

@app.route('/upload',methods = ['POST', 'GET'] )
def upload():
    if request.method == 'POST':
        # upload here 
        product_name = request.form['product_name']
        product_desc = request.form['product_desc']
        product_cost = request.form['product_cost']
        product_category = request.form['product_category']
        product_image_name = request.files['product_image_name']
        product_image_name.save('static/images/' + product_image_name.filename)
        connection = pymysql.connect(host='localhost', user = 'root', password='', database='funosokogardens')
        cursor = connection.cursor()

        # prepare your data 
        data = (product_name, product_desc, product_cost, product_category, product_image_name.filename)
        sql = "insert into products (product_name, product_desc, product_cost, product_category, product_image_name) values (%s, %s, %s, %s, %s)"
        
        cursor.execute(sql , data )
        connection.commit()
        return render_template('upload.html', message="products added successful")
    

























    else:
        return render_template('upload.html')












@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        username=request.form['username']
        email=request.form['email']
        phone=request.form['phone']
        password1=request.form['password1']
        password2=request.form['password2']

        # verify password
        if len(password1)<8:
            return render_template("register.html",error="password must be 8 chars")
        elif password1 != password2:
             return render_template("register.html",error="password does not much")
        else:
            sql="insert into users(username,email,phone,password)values(%s,%s,%s,%s)"
            cursor= connection.cursor()
            cursor.execute(sql,(username,email,phone,password1))
            connection.commit()
            sms.send_sms(phone,'Registration successful')

            return render_template('register.html',success='Registration succesful')
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='GET':
     return render_template('login.html')
    else:
        username=request.form['username']
        password=request.form['password']
        sql="SELECT* FROM users where username=%s and password=%s"
        cursor=connection.cursor()
        cursor.execute(sql,(username,password))
        if cursor.rowcount ==0:
            return render_template('login.html',error='invalid username or password')
        else:
            session['key']=username
            return redirect('/home')
        

@app.route('/logout')    
def logout():
    session.clear()
    return redirect('/login')



        


        

            


    
    
    
    
    
if __name__ == '__main__':
# run app 
    app.run(debug=True, port=4001)