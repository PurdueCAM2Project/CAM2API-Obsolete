from django.contirb.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied

class CAM2APIPermissionRequiredMixin(AccessMixin):
	permission_required = None
	def get_permission_required(self):
		if self.permission_required is None:
			raise ImproperlyConfigured("SMD")
		
		if isinstance(self.permission_required, str):
			return (self.permission_required, )
		return self.permission_required 

	def has_permission(self):
		perm = self.get_permission_required()
		return self.request.user.has_perm(perm)

	def dispatch(self, request, *args, **kwargs):
		if not has_permission():
			return self.handle_no_permission()
		super().dispatch(request, *args, **kwargs)

