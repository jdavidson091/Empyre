# -*- coding: utf-8 -*-


def index():
    response.flash = T("Hello World")
    return dict(message=T(''))



def find_new_opponents():
    response.flash = T("find new opponents screen")
    return dict()


def current_games():
    response.flash = T("current games")
    return dict()


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


