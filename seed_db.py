from run import seed_data, app

if __name__ == '__main__':
    with app.app_context():
        # this will invoke the seed_data logic that populates Categories and Interests
        seed_data()
        print("Seed complete.")
