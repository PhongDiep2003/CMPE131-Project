from app import myapp_obj, models
import secrets
from datetime import date

myapp_obj.debug=True
myapp_obj.config['SECRET_KEY'] = secrets.token_hex(16)


# dbSession = models.Session()
# usercontact = models.userContact(id=0, userId=1, contactId=2, nickName='Phong')
# dbSession.add(usercontact)
# dbSession.commit()
# dbSession.close()

# u = models.user(email="nobito@gmailclone.com", passwordHash="nobito")
# todoList = models.todoList(id=0, userId=0, name="Test")
# todoItem = models.todoItem(id=0, todoListId=0, name="Test", priority=1, startDate=date.today(), dueDate=date.today(), status=False)
# u1 = models.user(email="khate22@gmailclone.com", passwordHash="khate22")
# u2 = models.user(email="lenat44@gmailclone.com", passwordHash="lenat44")
# u3 = models.user(email="coreyboy1820@gmailclone.com", passwordHash="hs")
# dbSession = models.Session()
# current_date = date.today()
# dbSession.begin()
# message = models.message(id=0, senderId= dbSession.query(models.user).filter_by(email="coreyboy1820@gmailclone.com").first().id ,message= "hs", sentDate= current_date, recievedDate = current_date, subject= "hs" )
# dbSession.add(todoList)
# dbSession.add(todoItem)
# dbSession.commit()
# print(dbSession.query(models.message).first().message)
# dbSession.close()
# session.begin()
# session.add(u)
# session.add(u1)
# session.add(u2)
# session.commit()


if __name__ == "__main__":
    myapp_obj.run(port=5000)
