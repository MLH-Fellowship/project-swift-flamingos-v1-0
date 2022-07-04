from email.policy import default
import os
import datetime
from flask import Flask, redirect, render_template, request
from playhouse.shortcuts import model_to_dict
from dotenv import load_dotenv
from peewee import *
import re


if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSOL DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )

load_dotenv()

db = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


db.connect()
db.create_tables([TimelinePost])
app = Flask(__name__)


indexData = {
    "img": "img/mateo.jpeg",
    "name": "Mateo Marinez",
    "intro": "Computer Science Student @ The University of Texas Rio Grande Valley",
}

aboutData = [
    """I'm a Computer Science Student @ University of Texas Rio Grande
              Valley. I was born and raised in the Rio Grande Valley aka 956 -
              Magic Valley. I live in the coutry side of a town called
              Harlingen. The valley is on the border between Tamaulipas, Mexico
              and the US. We are known for our amazing hispanic food culture and
              diabates which is not a good combo. We are also known for our
              amazing beach on South Padre Island and Boca Chica Beach which is
              divided by the Jetties. Boca Chica Beach has become more popular
              due to our new honary RGV resident Elon Musk that lives out
              somewhere on his launch pad near Boca Chica. We also hold the
              national title of poorest areas to live in the US and Texas, once
              again not the greatest thing to brag about.""",
    """We also have many visitors from northern states and even Canada.
              The older population that come to stay during our winter times are
              called Winter Texans or Snow Birds. They move down during winter
              time mainly because their states and or cities are frozen while we
              are warm and toasty during this time. You see many of them going
              into Mexico to buy things they need and to have a Mexican Beer or Margerita!""",
    """Anyways back to the food! We have a growing local restaurant chain
              that only has one major item on the menu, Tamales! Delia's Tamales
              has literaly blown up in our area and is still growing. If your
              into cajun seafood the Dirty Al's chain of restaurants has also
              blown up. They started out in Port Isabel and South Padre Island.
              Now they have spread to bigger cities through out the RGV. They serve
              some of my most favorite food! Sea Food!""",
    """Many people in our area poor to be honest but have worked
              extremely hard to provide for their families and are happy. This
              is true of my family and others that live in the RGV. My
              grandparents and great grandparents were migrant farm workers who
              hardly knew English. The majority of my great grand parents either
              never went to school or dropped out at a super young age. My
              grandparents saw how my great grandparents struggled and worked
              just as hard to provide for my parents. Now my parents have done the
              same for me and my brother. I am who I am because of my friends and family 
              that have instilled a sense of morality and love for god in me. This is who I am.""",
]

hobbiesData = [
    {
        "img": "img/spi.jpeg",
        "title": "🌊 South Padre Island 🌊",
        "content": "On days that I'm off me and my family like to go eat cajun seafood. We also like to fish off a part of the island called the Jetties. And of course, we go swim in the water!",
    },
    {
        "img": "img/mnt.jpeg",
        "title": "🥾 Hiking 🥾",
        "content": "I recently found a love for hiking. This is a trail that was off the road as I was heading towards Mnt. Rainier. This pond called Jacob's Pond was so clear you coud see the bottom about 30ft out!",
    },
    {
        "img": "img/pi.jpeg",
        "title": "💾 Raspberry Pi's 💾",
        "content": "These computers have changed the way we see computing. Thay have been used in many real world pojects. Because of their open source nature it has given life to ideas without breaking the bank!",
    },
]

placesData = {
    "map": "https://www.google.com/maps/d/embed?mid=1TpVtIh2KYkDkKg-R2-0ZEr8ml0NC8jk&ehbc=2E312F",
}

experienceData = {
    "swe": [
        "Software Engineering",
        [
            "Web Development",
            "Network Programming",
            "System Programming",
            "Cryptography",
            "CTF's",
            "Hackathons",
        ],
    ],
    "linux": ["Linux", ["Shell Scripting", "System Managment", "KDE", "Kali Linux"]],
    "networking": [
        "Networking",
        ["Network Hacking", "Ethernet & Coaxial Cable Running", "Phone Lines", "WISP"],
    ],
    "hardware": [
        "Hardware",
        ["Raspberry Pi's", "PC Builds", "Server Builds", "Pfsense Router Builds"],
    ],
}

contactData = {}


@app.route("/")
def index():
    return render_template("index.html", indexData=indexData)


@app.route("/about")
def about():
    return render_template("about.html", aboutData=aboutData)


@app.route("/hobbies")
def hobbies():
    return render_template("hobbies.html", hobbiesData=hobbiesData)


@app.route("/places")
def places():
    return render_template("places.html", placesData=placesData)


@app.route("/experience")
def experience():
    return render_template("experience.html", experienceData=experienceData)


@app.route("/contact")
def contact():
    return render_template("contact.html", contactData=contactData)


@app.route("/timeline")
def timeline():
    data = get_time_line_post()
    return render_template("timeline.html", data=data)


@app.route("/api/timeline_post", methods=["DELETE"])
def delete_time_line_post():
    id = request.form["id"]
    TimelinePost.delete_by_id(id)
    return render_template("timeline.html")


@app.route("/api/timeline_post", methods=["POST"])
def post_time_linepost():

    name = request.form.get("name")
    email = request.form.get("email")
    content = request.form.get("content")

    if not name or name == "" or name is None:
        return "Invalid name", 400

    elif (
        not email
        or email == ""
        or email is None
        or re.match(
            r"([A-Za-z0-9]+[.-])*[A-Za-z0-9]+@[A-Za-z0-9-]+(.[A-Z|a-z]{2,})+", email
        )
        == None
    ):
        return "Invalid email", 400

    elif not content or content == "" or content is None:
        return "Invalid content", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():

    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
