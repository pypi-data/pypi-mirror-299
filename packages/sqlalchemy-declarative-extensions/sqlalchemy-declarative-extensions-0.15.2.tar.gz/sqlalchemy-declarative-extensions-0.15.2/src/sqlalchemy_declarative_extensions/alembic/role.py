from __future__ import annotations

from alembic.autogenerate.api import AutogenContext
from alembic.autogenerate.compare import comparators
from alembic.autogenerate.render import renderers
from alembic.operations import Operations

from sqlalchemy_declarative_extensions.role.compare import (
    CreateRoleOp,
    DropRoleOp,
    Roles,
    UpdateRoleOp,
    compare_roles,
)

Operations.register_operation("create_role")(CreateRoleOp)
Operations.register_operation("update_role")(UpdateRoleOp)
Operations.register_operation("drop_role")(DropRoleOp)


@comparators.dispatch_for("schema")
def _compare_roles(autogen_context: AutogenContext, upgrade_ops, _):
    roles: Roles | None = Roles.extract(autogen_context.metadata)
    if not roles:
        return

    assert autogen_context.connection
    result = compare_roles(autogen_context.connection, roles)
    upgrade_ops.ops[0:0] = result


@renderers.dispatch_for(CreateRoleOp)
@renderers.dispatch_for(DropRoleOp)
@renderers.dispatch_for(UpdateRoleOp)
def render_role(autogen_context: AutogenContext, op: CreateRoleOp):
    is_dynamic = op.role.is_dynamic
    if is_dynamic:
        autogen_context.imports.add("import os")

    return [
        f'op.execute({"f" if is_dynamic else ""}"""{command}""")'
        for command in op.to_sql(raw=False)
    ]


@Operations.implementation_for(CreateRoleOp)
@Operations.implementation_for(UpdateRoleOp)
@Operations.implementation_for(DropRoleOp)
def create_role(operations, op):
    commands = op.to_sql()
    for command in commands:
        operations.execute(command)
