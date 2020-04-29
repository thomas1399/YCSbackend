from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# all primary keys are autoincremented on creation, there is no integrity check yet except for the Foreign keys


class User(db.Model): #the User table
    idU = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lastName = db.Column(db.String, nullable=False)
    firstName = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    right = db.Column(db.Integer, nullable=False)
    surveys = db.relationship("Survey", cascade="all, delete-orphan") # foreign key to child survey
    votes = db.relationship("Vote", cascade="all, delete-orphan") #foreign key to child vote

    @property
    def serialize(self): # property that transforms the user object into a json string
        return{
            'idU'    : self.idU,
            'lastName': self.lastName,
            'firstName': self.firstName,
            'birthdate': self.birthdate.strftime('%d-%m-%Y'),
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'password': self.password,
            'right': self.right,
            'surveys': self.serialize_one2many_surveys,
            'votes': self.serialize_one2many_votes
        }

    @property
    def serialize_one2many_surveys(self): # property to create an array of json elements, basically the foreign keys of the main on
        return [item.serialize for item in self.surveys]

    @property
    def serialize_one2many_votes(self):
        return [item.serialize for item in self.votes]

    def __repr__(self):
        return  '<User %r %r>' % self.lastName % self.firstName


class Survey(db.Model):
    idS = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    nbOfQuestions = db.Column(db.Integer, nullable=False)
    idU = db.Column(db.Integer, db.ForeignKey('user.idU'), nullable=False) # foreign key to parent user
    questions = db.relationship("Question", cascade="all, delete-orphan") # foreign key to child question

    @property
    def serialize(self):
        return {
            'idS': self.idS,
            'title': self.title,
            'category': self.category,
            'nbOfQuestions': self.nbOfQuestions,
            'questions': self.serialize_one2many_questions
        }

    @property
    def serialize_one2many_questions(self): # same as for User
        return [item.serialize for item in self.questions]

    def __repr__(self):
        return '<Survey %r %r>' % self.idS % self.title


class Question(db.Model):
    idQ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statement = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    answer1 = db.Column(db.String, nullable=True)
    answer2 = db.Column(db.String, nullable=True)
    answer3 = db.Column(db.String, nullable=True)
    answer4 = db.Column(db.String, nullable=True)
    answer5 = db.Column(db.String, nullable=True)
    idS = db.Column(db.Integer, db.ForeignKey('survey.idS'), nullable=False) # foreign key to parent survey
    votes = db.relationship("Vote", cascade="all, delete-orphan") # foreign key to child vote

    @property
    def serialize(self):
        return{
            'idQ': self.idQ,
            'statement': self.statement,
            'number': self.number,
            'answer1': self.answer1,
            'answer2': self.answer2,
            'answer3': self.answer3,
            'answer4': self.answer4,
            'answer5': self.answer5,
            'votes': self.serialize_one2many_votes
        }

    @property
    def serialize_one2many_votes(self): #same as User
        return [item.serialize for item in self.votes]

    def __repr__(self):
        return '<Question %r %r>' % self.statement  % self.number


class Vote(db.Model):
    idV = db.Column(db.Integer, primary_key=True, autoincrement=True)
    answer = db.Column(db.String, nullable=False)
    idU = db.Column(db.Integer, db.ForeignKey('user.idU'), nullable=False)
    idQ = db.Column(db.Integer, db.ForeignKey('question.idQ'), nullable=False)

    @property
    def serialize(self):
        return{
            'idV': self.idV,
            'answer': self.answer
        }