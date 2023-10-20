import os

from ckeditor_uploader import utils
from ckeditor_uploader.backends import get_backend
from ckeditor_uploader.utils import storage
from ckeditor_uploader.views import ImageUploadView, get_upload_filename
from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.response.renderer import CustomJSONResponseRenderer


class CustomCKEditorAPIView(ImageUploadView, APIView):
    http_method_names = ['get', 'options', 'head', 'post']
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomJSONResponseRenderer]

    def post(self, request, **kwargs):
        uploaded_file = request.FILES["upload"]

        backend = get_backend()

        ck_func_num = request.GET.get("CKEditorFuncNum")
        if ck_func_num:
            ck_func_num = escape(ck_func_num)

        file_wrapper = backend(storage, uploaded_file)
        allow_non_images = getattr(settings, "CKEDITOR_ALLOW_NONIMAGE_FILES", True)
        # Throws an error when an non-image file are uploaded.
        if not file_wrapper.is_image and not allow_non_images:
            return Response(content_type="""
                <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({}, '', 'Invalid file type.');
                </script>""".format(
                ck_func_num
            )
            )

        filepath = get_upload_filename(uploaded_file.name, request)

        saved_path = file_wrapper.save_as(filepath)

        url = utils.get_media_url(saved_path)

        if ck_func_num:
            # Respond with Javascript sending ckeditor upload url.
            return HttpResponse(
                """
            <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({}, '{}');
            </script>""".format(
                    ck_func_num, url
                )
            )
        else:
            _, filename = os.path.split(url)
            retdata = {"url": request.build_absolute_uri(url), "fileName": filename}
            return Response(retdata)
