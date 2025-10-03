from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View

class GroupPermissionPerMethod(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        
         # ใช้ method lowercase เช่น 'get', 'post'
        method = request.method.lower()
        action = getattr(view, 'action', None)

        permission_map = getattr(view, 'permission_required_by_method', {})
        required_perm = permission_map.get(method) or permission_map.get(action)

        if not required_perm:
            return True  # ถ้า method นี้ไม่ได้กำหนด permission ถือว่า allow

        if isinstance(required_perm, str):
            return request.user.has_perm(required_perm)
        elif isinstance(required_perm, list): # รองรับ list permission Ex."save_exam_rooms": ["exam.change_examroom", "exam.add_examroom"],
            return all(request.user.has_perm(perm) for perm in required_perm)
        return False

    def has_object_permission(self, request: Request, view: View, obj: object) -> bool:
        return self.has_permission(request, view)