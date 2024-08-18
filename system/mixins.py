from django.shortcuts import redirect


class LegalRequirementMixin:
    def dispatch(self, request, *args, **kwargs):

        if not request.user.legaluser.privacy:
            return redirect("privacy")

        if not request.user.legaluser.disclaimer:
            return redirect("disclaimer")

        if not request.user.legaluser.terms:
            return redirect("terms")

        return super().dispatch(request, *args, **kwargs)
