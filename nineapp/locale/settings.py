
#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'nineapp/static'),]
"""
DATABASES = {
	"default": {
	"ENGINE": "django.db.backends.postgresql",
	"NAME": "nine",
	"USER": "postgres",
	"PASSWORD": "power123",
	"HOST": "localhost"	
	}
}
"""

CATEGORY_CHOICES = (
	('lf','LifeStyle'),
	('ed', 'Education'),
	('fh', 'Fashion & Arts'),
	('hl', 'Health'),
	('po', 'Politics'),
	('bs', 'Business'),
	('tc', 'Technology'),
)


ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
}