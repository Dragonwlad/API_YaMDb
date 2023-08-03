from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Доступ разрешен только для аутентифицированных суперпользователей или пользователей с правами администратора.
    Пользователи с остальными ролями могут только просматривать объекты, но не редактировать или удалять их.

    """
    message = "Редактирование или удаление этого элемента недопустимо."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser)
            )
        )


class IsAdminOnly(BasePermission):
    """
    Доступ разрешен только для аутентифицированных суперпользователей или пользователей с правами администратора.

    """
    message = "Это действие не разрешено."

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsOwnerAdminModeratorOrReadOnly(BasePermission):
    """
    Доступ разрешен только для суперпользователей, администраторов, авторов объектов или пользователей с ролью модератора.
    Остальные пользователи могут только просматривать объекты, но не редактировать или удалять их.

    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.is_admin
            or request.user.is_superuser
            or request.user.is_moderator
        )
