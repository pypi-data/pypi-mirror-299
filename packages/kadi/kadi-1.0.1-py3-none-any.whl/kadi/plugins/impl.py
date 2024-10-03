# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# pylint: disable=missing-function-docstring


from flask import current_app
from flask import render_template

from kadi.lib.api.blueprint import bp as api_bp
from kadi.lib.storage.local import LocalStorage
from kadi.modules.accounts.blueprint import bp as accounts_bp
from kadi.modules.collections.blueprint import bp as collections_bp
from kadi.modules.groups.blueprint import bp as groups_bp
from kadi.modules.main.blueprint import bp as main_bp
from kadi.modules.records.blueprint import bp as records_bp
from kadi.modules.records.dashboards import (
    get_custom_mimetype as get_dashboard_mimetype,
)
from kadi.modules.records.previews import get_builtin_preview_data
from kadi.modules.settings.blueprint import bp as settings_bp
from kadi.modules.sysadmin.blueprint import bp as sysadmin_bp
from kadi.modules.templates.blueprint import bp as templates_bp
from kadi.modules.workflows.blueprint import bp as workflows_bp
from kadi.modules.workflows.core import get_custom_mimetype as get_workflow_mimetype

from . import hookimpl


@hookimpl(tryfirst=True)
def kadi_get_blueprints():
    blueprints = [
        api_bp,
        accounts_bp,
        collections_bp,
        groups_bp,
        main_bp,
        records_bp,
        settings_bp,
        sysadmin_bp,
        templates_bp,
    ]

    if current_app.config["WORKFLOW_FEATURES"]:
        import kadi.modules.workflows.api  # pylint: disable=unused-import

        blueprints.append(workflows_bp)

    return blueprints


@hookimpl(tryfirst=True)
def kadi_get_content_security_policies():
    return {
        "default-src": "'self'",
        "base-uri": "'none'",
        "frame-ancestors": "'self'",
        "frame-src": "'self'",
        "img-src": ["'self'", "blob:", "data:"],
        "object-src": "'none'",
        "script-src": ["'self'", "'unsafe-eval'"],
        "style-src": ["'self'", "'unsafe-inline'", "data:"],
    }


@hookimpl(tryfirst=True)
def kadi_get_custom_mimetype(file, base_mimetype):
    for get_custom_mimetype in [get_workflow_mimetype, get_dashboard_mimetype]:
        custom_mimetype = get_custom_mimetype(file, base_mimetype)

        if custom_mimetype:
            return custom_mimetype

    return None


@hookimpl(tryfirst=True)
def kadi_get_preview_data(file):
    return get_builtin_preview_data(file)


@hookimpl(tryfirst=True)
def kadi_get_preview_templates(file):
    return render_template("records/snippets/preview_file.html", file=file)


@hookimpl(tryfirst=True)
def kadi_get_storage_providers():
    storage_path = current_app.config["STORAGE_PATH"]

    if storage_path is None:
        return None

    return LocalStorage(storage_path)
