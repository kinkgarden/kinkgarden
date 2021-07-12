import json

from django.conf import settings
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
from django.urls import reverse, resolve, Resolver404
from django.contrib.auth.hashers import check_password, make_password
import requests

from .models import (
    KinkList,
    KinkListColumn,
    StandardKinkListEntry,
    CustomKinkListEntry,
    CustomReject,
)
from editor.views import EditorView


class PasswordProtectedMixin:
    password_field = ""
    password_form_template = ""

    def bad_password(self, request):
        context = {}
        if len(self.submitted_password(request)) > 0:
            context["error_message"] = "Incorrect password."
        return render(request, self.password_form_template, context, status=403)

    def submitted_password(self, request):
        return request.POST.get(self.password_field, "")

    def check_password(self, request, encoded):
        return check_password(self.submitted_password(request), encoded)


@method_decorator(
    sensitive_post_parameters("view-password"), name="dispatch",
)
class KinkListView(PasswordProtectedMixin, generic.DetailView):
    model = KinkList
    template_name = "kinks/list.html"
    password_field = "view-password"
    password_form_template = "kinks/enter_view_password.html"
    slug_field = "short_link"
    slug_url_kwarg = "short_link"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return self.bad_password(request)
        if len(self.object.view_password) > 0:
            if not self.check_password(request, self.object.view_password):
                return self.bad_password(request)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    post = get


@method_decorator(
    [
        transaction.atomic,
        sensitive_post_parameters("view-password", "edit-password"),
        sensitive_variables("view_password", "edit_password"),
    ],
    name="dispatch",
)
class KinkListCreate(EditorView):
    def post(self, request, *args, **kwargs):
        for key in ("kink-list-data", "view-password", "edit-password"):
            if key not in request.POST:
                raise SuspiciousOperation()
        list_data = json.loads(request.POST["kink-list-data"])
        view_password = request.POST["view-password"]
        if len(view_password) > 0:
            view_password = make_password(view_password)
        else:
            view_password = ""
        edit_password = request.POST["edit-password"]
        if len(edit_password) > 0:
            edit_password = make_password(edit_password)
        else:
            edit_password = ""
        kink_list = KinkList(view_password=view_password, edit_password=edit_password)
        kink_list.save()
        for column in list_data:
            column_desc = KinkListColumn[column["name"].upper()]
            entry_metadata = {"list": kink_list, "column": column_desc.value}
            for kink in column["kinks"]:
                if kink["custom"]:
                    name = kink["name"]
                    if CustomReject.objects.filter(name__iexact=name).exists():
                        continue
                    description = kink["description"]
                    entry = CustomKinkListEntry(
                        custom_name=name,
                        custom_description=description,
                        **entry_metadata,
                    )
                    entry.save()
                else:
                    kink_id = kink["id"]
                    entry = StandardKinkListEntry(kink_id=kink_id, **entry_metadata)
                    entry.save()
        return HttpResponseRedirect(kink_list.get_absolute_url())


def push_edit_target(session, list_id):
    if "edit-target" not in session:
        session["edit-target"] = [str(list_id)]
    else:
        session["edit-target"] = [*session["edit-target"], str(list_id)]


def pop_edit_target(session, list_id):
    if "edit-target" not in session:
        raise PermissionDenied
    targets = session["edit-target"]
    if str(list_id) not in targets:
        raise PermissionDenied
    targets = list(x for x in targets if x != str(list_id))
    session["edit-target"] = targets


@method_decorator(sensitive_post_parameters("edit-password"), name="dispatch")
class KinkListEdit(PasswordProtectedMixin, EditorView):
    password_field = "edit-password"
    password_form_template = "kinks/enter_edit_password.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    def get(self, request, *args, **kwargs):
        return self.bad_password(request)

    def post(self, request, *args, **kwargs):
        try:
            self.object = KinkList.objects.get(id=kwargs["pk"])
        except KinkList.DoesNotExist:
            return self.bad_password(request)
        if not self.check_password(request, self.object.edit_password):
            return self.bad_password(request)
        push_edit_target(request.session, self.object.id)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        column_data = dict((x, []) for x in KinkListColumn)
        for entry in self.object.standardkinklistentry_set.all():
            column_data[KinkListColumn(entry.column)].append(
                {"custom": False, "id": entry.kink_id}
            )
        for entry in self.object.customkinklistentry_set.all():
            column_data[KinkListColumn(entry.column)].append(
                {
                    "custom": True,
                    "name": entry.custom_name,
                    "description": entry.custom_description,
                }
            )
        context["init_data"] = {
            "columns": [
                {"name": x.name.lower(), "kinks": k} for x, k in column_data.items()
            ],
            "action": reverse("kinks:kink_list_save", args=(self.object.id,)),
            "patreonClientId": settings.PATREON["client_id"],
            "listId": kwargs["pk"],
        }
        if self.request.session.get("patreon-ok", False):
            context["init_data"]["patreonOk"] = True
        if "patreon-error" in self.request.session:
            context["init_data"]["patreonError"] = self.request.session["patreon-error"]
        return context


@method_decorator(
    sensitive_variables("tokens_response", "tokens", "access_token"), name="dispatch",
)
class PatreonRedirect(generic.View):
    def get(self, request: HttpRequest, *args, **kwargs):
        code = request.GET["code"]
        list_id = request.GET["state"]

        client_id = settings.PATREON["client_id"]
        client_secret = settings.PATREON["client_secret"]

        tokens_response = requests.post(
            "https://www.patreon.com/api/oauth2/token",
            data={
                "code": code,
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": request.build_absolute_uri(request.path),
            },
            headers={"User-Agent": "kink.garden patreon integration"},
        )
        tokens = tokens_response.json()
        tokens_response.raise_for_status()
        access_token = tokens["access_token"]

        memberships_response = requests.get(
            "https://www.patreon.com/api/oauth2/v2/identity",
            params={
                "include": "memberships.currently_entitled_tiers,memberships.campaign"
            },
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": "kink.garden patreon integration",
            },
        )
        memberships = memberships_response.json()
        memberships_response.raise_for_status()
        target_campaign_id = settings.PATREON["campaign"]
        target_tier_id = settings.PATREON["short_link_tier"]
        found_campaign = False
        found_tier = False
        for membership in memberships["included"]:
            if membership["type"] == "member":
                if (
                    membership["relationships"]["campaign"]["data"]["id"]
                    == target_campaign_id
                ):
                    found_campaign = True
                    for tier in membership["relationships"]["currently_entitled_tiers"][
                        "data"
                    ]:
                        if tier["id"] == target_tier_id:
                            found_tier = True
                            break
                    break

        if found_campaign and found_tier:
            request.session["patreon-ok"] = True
        elif found_campaign:
            request.session["patreon-error"] = "wrong tier"
        else:
            request.session["patreon-error"] = "not pledged"

        if str(list_id) in request.session.get("edit-target", []):
            return HttpResponseRedirect(
                reverse("kinks:kink_list_edit", args=(list_id,))
            )
        else:
            return HttpResponseRedirect("/")


@method_decorator(
    [
        transaction.atomic,
        sensitive_post_parameters("view-password", "edit-password"),
        sensitive_variables("view_password", "edit_password"),
    ],
    name="dispatch",
)
class KinkListSave(generic.View):
    def post(self, request: HttpRequest, *args, **kwargs):
        for key in ("kink-list-data", "view-password", "edit-password"):
            if key not in request.POST:
                raise SuspiciousOperation()
        pop_edit_target(request.session, str(kwargs["pk"]))
        list_data = json.loads(request.POST["kink-list-data"])
        kink_list = KinkList.objects.get(id=kwargs["pk"])
        view_password = request.POST["view-password"]
        if len(view_password) > 0:
            kink_list.view_password = make_password(view_password)
        elif request.POST.get("clear-view-password", "") == "on":
            kink_list.view_password = ""
        edit_password = request.POST["edit-password"]
        if len(edit_password) > 0:
            kink_list.edit_password = make_password(edit_password)
        elif request.POST.get("clear-edit-password", "") == "on":
            kink_list.edit_password = ""
        short_link = request.POST.get("short-link", "")
        if short_link != "" and request.session.get("patreon-ok", False):
            # 1. make sure we aren't duplicating short links
            if not KinkList.objects.filter(short_link=short_link).exists():
                # 2. make sure we aren't overlapping with an internal URL
                match = resolve(
                    reverse("kinks:kink_list_by_short_link", args=(short_link,))
                )
                if match.url_name == "kink_list_by_short_link":
                    kink_list.short_link = short_link
        elif request.POST.get("clear-short-link", "") == "on":
            kink_list.short_link = ""
        kink_list.save()

        # this probably could be better.
        new_standard_ids = set(
            k["id"] for col in list_data for k in col["kinks"] if not k["custom"]
        )
        kink_list.standardkinklistentry_set.exclude(
            kink_id__in=new_standard_ids
        ).delete()

        new_custom_names = set(
            k["name"] for col in list_data for k in col["kinks"] if k["custom"]
        )
        kink_list.customkinklistentry_set.exclude(
            custom_name__in=new_custom_names
        ).delete()

        for column in list_data:
            column_desc = KinkListColumn[column["name"].upper()]
            for kink in column["kinks"]:
                if kink["custom"]:
                    name = kink["name"]
                    if CustomReject.objects.filter(name__iexact=name).exists():
                        continue
                    description = kink["description"]
                    entry, _ = kink_list.customkinklistentry_set.get_or_create(
                        custom_name=name,
                        defaults={
                            "custom_description": description,
                            "column": column_desc.value,
                        },
                    )
                    entry.custom_description = description
                    entry.column = column_desc.value
                    entry.save()
                else:
                    kink_id = kink["id"]
                    entry, _ = kink_list.standardkinklistentry_set.get_or_create(
                        kink_id=kink_id, defaults={"column": column_desc.value}
                    )
                    entry.column = column_desc.value
                    entry.save()
        return HttpResponseRedirect(kink_list.get_absolute_url())
