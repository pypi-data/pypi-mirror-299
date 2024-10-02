from raft.tasks import task
from .base import AzureTask
from ..base.utils import get_context_value
from ..base.utils import notice, notice_end


@task(help=dict(perms='read, write, or manage'), iterable=['perms'], klass=AzureTask)
def grant_access_to_site(ctx, site_name, app_name, perms=None, **kwargs):
    """
    grants the app with name app_name read and write permissions to the site_name sharepoint site

    this convocation is useful when you have created an azure application
    registration with api permission Sites.Selected and need to authorize
    the application to connect to a particular sharepoint site.
    """
    from requests.sessions import Session
    notice('tenant_name')
    perms = perms or [ 'read', 'write' ]
    creds = kwargs['creds']
    scopes = [
        'https://graph.microsoft.com/.default',
    ]
    token = creds.get_token(*scopes)
    tenant_id = get_context_value(ctx, 'azure.tenant_id')
    session = Session()
    base_url = 'https://graph.microsoft.com/v1.0/'
    session.headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {token.token}',
        'consistencylevel': 'eventual',
    }
    response = session.get(
        f'{base_url}/tenantRelationships/'
        f"findTenantInformationByTenantId(tenantId='{tenant_id}')",
    )
    data = response.json()
    tenant_name = data['displayName'].lower()
    notice_end(tenant_name)
    notice('looking up application')
    hostname = f'{tenant_name}.sharepoint.com'
    list_apps_url = f'{base_url}/applications'
    params = {
        '$search': f'"displayName:{app_name}"',
    }
    response = session.get(list_apps_url, params=params)
    result = response.json()['value']
    app_id = None
    for x in result:
        if x['displayName'].lower() == app_name.lower():
            app_id = x['id']
            break
    if not app_id:
        notice_end(False)
        return
    notice_end(f'{app_id}')
    notice('site id')
    site_url = f'{base_url}/sites/{hostname}:/sites/{site_name}'
    response = session.get(site_url)
    data = response.json()
    site_id = data['id']
    notice_end(site_id)
    notice('checking existing permissions')
    perms_url = f'{base_url}/sites/{site_id}/permissions'
    params = {
        '$select': 'id,roles,grantedToIdentities'
    }
    response = session.get(perms_url, params=params)
    data = response.json()
    app_id_exists = False
    existing_permission_id = None
    existing_perms = []
    for x in data['value']:
        permission_id = x['id']
        perm_url = f'{perms_url}/{permission_id}'
        response = session.get(perm_url)
        data = response.json()
        roles = data['roles']
        identities = data['grantedToIdentitiesV2']
        for i in identities:
            app = i.get('application')
            if app and app['id'] == app_id:
                app_id_exists = True
                existing_permission_id = permission_id
                existing_perms = roles
                break
        if roles == perms and app_id_exists:
            notice_end('permission already granted')
            return
    notice_end(existing_permission_id is not None)
    if existing_permission_id:
        notice('updating existing permission')
        perm_url = f'{perms_url}/{existing_permission_id}'
        updated_perms = set(existing_perms)
        for perm in perms:
            updated_perms.add(perm)
        response = session.patch(perm_url, json={
            'roles': updated_perms,
        })
        notice_end(response.ok)
    else:
        notice('creating new permission')
        perm_url = f'{perms_url}'
        response = session.post(perm_url, json={
            'roles': perms,
            'grantedToIdentities': {
                'application': {
                    'id': app_id,
                },
            },
        })
        notice_end(response.ok)
