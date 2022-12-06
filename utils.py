
from faker import Faker
from functools import wraps
from random import randint


faker = Faker()


def NotFoundResponse(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if (response := function(*args, **kwargs)):
            return response
        return {}, 404
    return wrapper


class User():
    def __init__(self) -> None:
        self.DB = [
            {
                "id": _ + 1,
                "fullname": faker.name(),
                "profile": f"https://avatars.dicebear.com/api/personas/{_}.svg"
            }
            for _ in range(5)
        ]

    def get_one(self, id):
        for user in self.DB:
            if user.get("id") == id:
                return user

    def get_all(self):
        return self.DB

    def insert(self, data):
        data.update({"id": randint(len(self.DB), len(self.DB) + 100) + 111})
        self.DB.append(data)
        return data

    def update(self, id, data):
        if (user := self.get_one(id)):
            user.update(data)
        return user

    def delete(self, id):
        DB_ = list(filter(lambda x: x["id"] != id,  self.DB))
        # Check if the object was there, by comparing then length of the list
        if (_ := (len(self.DB) != len(DB_))):
            self.DB = DB_
            return {"deleted": True}
        return _


UserTable = User()
