from flaskr import create_app, db, create_first_user

app = create_app()

with app.app_context():
    db.create_all()
    create_first_user()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

