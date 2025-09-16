from .models import ActivityLogModel

class ActivityLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path == '/admin/logout/':
                ActivityLogModel.objects.create(
                    user=request.user,
                    action='logout',
                    model_name='User',
                    object_repr=request.user.username,
                    ip_address=self.get_client_ip(request)
                )
            elif request.path == '/admin/login/' and request.method == 'POST':
                ActivityLogModel.objects.create(
                    user=request.user,
                    action='login',
                    model_name='User',
                    object_repr=request.user.username,
                    ip_address=self.get_client_ip(request)
                )

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):  # no `self` needed now
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
