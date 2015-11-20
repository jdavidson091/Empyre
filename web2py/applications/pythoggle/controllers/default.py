# -*- coding: utf-8 -*-


"""
This is the default view, which users are redirected to if not logged in.
TODO:
    present a quick introduction about the site. Scroll down?
    Link to sign in.
    EXTRA: facebook/twitter sign-in link.
"""
def index():
    return dict(message=T('This is the default index page.'))



@auth.requires_login()
def home():
    """
    return user info so wins/losses/picture can be displayed

    also, if auth user is logged in, retrieve their player info.
    If there is no player info for this user, redirect to new player screen
    """
    logged_in_profile = db(db.user_profile.auth_user_id == auth.user_id).select().first()
    if logged_in_profile is None:
        session.flash = 'Since this is your first time, create a new user profile'
        redirect(URL(request.application, request.controller, 'create_new_profile'))

    return dict(logged_in_profile)


@auth.requires_login()
def create_new_profile():
    """
    have a form for the user profile to be filled out
    """
    current_user_id = auth.user_id
    form = SQLFORM(db.user_profile,
                   fields=['username', 'user_image'])

    form.vars.auth_user_id = current_user_id

    if form.process().accepted:

        session.flash = 'New profile created'
        redirect(URL('home'))
    return dict(form=form)


def find_new_opponents():
    """
    Display list of players (all for now), maybe filter by wins/losses later
    List with:
        Username    wins/losses     [start new game]

    [start new game] will redirect you to the game screen

    return: a list of players to face
    """

    players = db(db.user_profile).select()

    if not players:
        players = []

    return dict(players=players)


def match():
    """
    the screen for an ongoing match
    :return:
    """
    # retrieve the current match info from passed id (add authentication checking later)
    game_board_id = request.args(0)
    current_game_board = db.game_board(game_board_id)

    #display the current game board...
    

    return dict()


def current_games():
    """
    Display 2 sets of games:
    Games where it is your turn
    Games where you are waiting to take your turn
        *have a flag on the right showing if a game is a new game or not
    """
    matches_your_turn = []
    matches_their_turn = []


    return dict(matches_your_turn=matches_your_turn,
                matches_their_turn=matches_their_turn,
                )


def past_games():
    response.flash = T("past games")
    return dict()


# TODO: have 'game' screen be in a different controller/view?

def high_scores():
    response.flash = "high score screen"
    return dict()


def rules():
    response.flash = "rules screen, have pictures as well"
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


