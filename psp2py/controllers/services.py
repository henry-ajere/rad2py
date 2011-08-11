# coding: utf8
# try something like

from gluon.tools import Service
service = Service(globals())

def call():
    session.forget()
    return service()
    
response.generic_patterns = ['*.json', '*.html']

@service.jsonrpc
def get_projects(): 
    projects = db(db.psp_project.project_id>0).select()
    return [project.name for project in projects]

@service.jsonrpc
def save_project(project_name, defects, time_summaries, comments): 
    project = db(db.psp_project.name==project_name).select()[0]

    # clean and store defects:
    db(db.psp_defect.project_id==project.project_id).delete()
    for defect in defects:
        defect['project_id'] = project.project_id
        defect.pop("id", None)
        defect.pop("defect_id", None)
        db.psp_defect.insert(**defect)

    # clean and store time summaries:
    db(db.psp_time_summary.project_id==project.project_id).delete()
    for time_summary in time_summaries:
        time_summary['project_id'] = project.project_id
        if 'id' in time_summary:
             del time_summary['id']
        db.psp_time_summary.insert(**time_summary)

    # clean and store comments:
    db(db.psp_comment.project_id==project.project_id).delete()
    for comment in comments:
        comment['project_id'] = project.project_id
        if 'id' in comment:
             del comment['id']
        db.psp_comment.insert(**comment)

    return True

@service.jsonrpc
def load_project(project_name): 
    project = db(db.psp_project.name==project_name).select()[0]
    defects = db(db.psp_defect.project_id==project.project_id).select()
    time_summaries = db(db.psp_time_summary.project_id==project.project_id).select()
    comments = db(db.psp_comment.project_id==project.project_id).select()
    return defects, time_summaries, comments


@service.jsonrpc
def add(a,b):
    return a+b

def test():
    from gluon.contrib.simplejsonrpc import JSONRPCClient
    client = JSONRPCClient(
                location="http://localhost:8000/psp2py/services/call/jsonrpc",
                exceptions=True, trace=True,
                )
    return {'result': client.add(1, 2)}