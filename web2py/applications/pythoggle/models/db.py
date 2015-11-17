# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
db.define_table('user_profile',
    Field('username', 'string'),
    Field('auth_user_id', 'integer', default=0),
    Field('current_matches', 'list:reference pythoggle_match', default=[]),
    Field('old_matches', 'list:reference pythoggle_match', default=[]),
    Field('user_image', 'upload', default=None),
    Field('high_score', 'integer', default=0),
    )


db.define_table('game_board',
    Field('board_values', 'string'),
    Field('user1', 'reference user_profile'),
    Field('user2', 'reference user_profile'),
    Field('user1_words', 'list:string'),
    Field('user2_words', 'list:string'),
    Field('user1_score', 'integer'),
    Field('user2_score', 'integer'),

    )

#don't implement time left to play initially
db.define_table('pythoggle_match',
    Field('created_on', 'datetime', default=request.now),
    Field('current_game_board', 'reference game_board'),
    Field('players_played_this_round', 'list:reference user_profile'),
    Field('current_round', 'integer', default=1),
    Field('finished', 'boolean', default=False),
    )




# db.define_table('recipe',
#    Field('name'),
#    Field('ingredients', 'text'),
#    Field('instructions', 'text'),
#    Field('image', 'upload'),
#    Field('rating','double',writable=False,readable=False),
#    Field('created_on', 'datetime', default=request.now),
#    Field('created_by', 'reference auth_user', default=auth.user_id), format = '%(name)s')
#
# db.define_table('comment',
#    Field('recipe_id'),
#    Field('comment', 'text'),
#    Field('created_on', 'datetime', default=request.now),
#    Field('author', 'reference auth_user', default=auth.user_id), format = '%(name)s')
#
# db.define_table('vote',
#     Field('recipe','reference recipe'),
#     Field('rating','double'))
#
# db.recipe.name.requires = IS_NOT_IN_DB(db, db.recipe.name)
# db.recipe.ingredients.requires = IS_NOT_EMPTY()
# db.recipe.instructions.requires = IS_NOT_EMPTY()
#
# db.comment.recipe_id.requires = IS_IN_DB(db, db.recipe.id, '%(name)s')
# db.comment.author.requires = IS_IN_DB(db, db.auth_user.id, '%(name)s')
# db.comment.author.requires = IS_NOT_EMPTY()
# db.comment.comment.requires = IS_NOT_EMPTY()
#
# db.comment.recipe_id.writable = db.comment.recipe_id.readable = False