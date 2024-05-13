def ValidatePermission(permissions_required : str | tuple, request ):
    
    if isinstance(permissions_required, str):
        perms = (permissions_required, )
    else:
        perms = permissions_required

    if not request.user.has_perms(perms):
        raise Exception('No Tienes Permiso Para Esta Acción')