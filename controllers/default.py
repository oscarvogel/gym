# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello, have a great day")
    return dict(message=T('Welcome to gym system!'))


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

@auth.requires_login()
def clientes():
    db.pagos.cliente.writable = False
    db.pagos.cliente.readable = False
    db.pagos.id.readable = False

    grid = SQLFORM.smartgrid(db.clientes,
        showbuttontext = False,
        linked_tables = ['pagos', 'clasesxcli'],
        upload = URL('download'),
        orderby = dict(parent = db.clientes.nombre, child=db.pagos.fecha_pago)
        )
    return locals()

@auth.requires_login()
def clases():
    grid = SQLFORM.grid(db.clases,
        showbuttontext = False
        )
    return locals()

@auth.requires_login()
def clasesxcli():
    grid = SQLFORM.grid(db.clasesxcli,
        showbuttontext = False
        )
    return locals()


@auth.requires_login()
def horarios():
    grid = SQLFORM.grid(db.horarios,
        showbuttontext = False
        )
    return locals()