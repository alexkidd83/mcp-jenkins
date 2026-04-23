from fastmcp import Context

from mcp_jenkins.core.lifespan import jenkins
from mcp_jenkins.server import mcp


@mcp.tool(tags=['read'])
async def get_running_builds(ctx: Context) -> list[dict]:
    """Get all running builds from Jenkins

    Returns:
        A list of all running builds
    """
    return [
        item.model_dump(include={'number', 'url', 'building', 'timestamp'})
        for item in jenkins(ctx).get_running_builds()
    ]


@mcp.tool(tags=['read'])
async def get_build(ctx: Context, fullname: str, number: int | None = None, tree: str | None = None) -> dict:
    """Get specific build info from Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build, if None, get the last build
        tree: Optional Jenkins tree parameter to select specific fields (e.g. "number,result,duration")

    Returns:
        The build info
    """
    if number is None:
        number = jenkins(ctx).get_item(fullname=fullname, depth=1).lastBuild.number

    return jenkins(ctx).get_build(fullname=fullname, number=number, tree=tree).model_dump(exclude_none=True)


@mcp.tool(tags=['read'])
async def get_build_scripts(ctx: Context, fullname: str, number: int | None = None) -> list[str]:
    """Get the scripts used in a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build, if None, get the last build

    Returns:
        A list of scripts used in the build
    """
    if number is None:
        number = jenkins(ctx).get_item(fullname=fullname, depth=1).lastBuild.number

    return jenkins(ctx).get_build_replay(fullname=fullname, number=number).scripts


@mcp.tool(tags=['read'])
async def get_build_console_output(
    ctx: Context,
    fullname: str,
    number: int | None = None,
    pattern: str | None = None,
    offset: int = 0,
    limit: int | None = None,
) -> str:
    """Get the console output of a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build, if None, get the last build
        pattern: Optional regex pattern to filter lines (only matching lines are returned)
        offset: Number of lines to skip from the beginning after filtering, default 0
        limit: Maximum number of lines to return after filtering and offset

    Returns:
        The console output of the build
    """
    if number is None:
        number = jenkins(ctx).get_item(fullname=fullname, depth=1).lastBuild.number
    if number is None:
        raise ValueError(f'No build found for job: {fullname}')

    return jenkins(ctx).get_build_console_output(
        fullname=fullname, number=number, pattern=pattern, offset=offset, limit=limit
    )


@mcp.tool(tags=['read'])
async def get_build_test_report(
    ctx: Context,
    fullname: str,
    number: int | None = None,
    tree: str | None = None,
) -> dict:
    """Get the test report of a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build, if None, get the last build
        tree: Optional Jenkins tree parameter to select specific fields.
              Use "suites[cases[name,status,errorDetails]]" to fetch only test case names and failures.

    Returns:
        The test report of the build
    """
    if number is None:
        number = jenkins(ctx).get_item(fullname=fullname, depth=1).lastBuild.number

    return jenkins(ctx).get_build_test_report(fullname=fullname, number=number, tree=tree)


@mcp.tool(tags=['read'])
async def get_build_parameters(ctx: Context, fullname: str, number: int | None = None) -> dict:
    """Get the parameters of a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build, if None, get the last build

    Returns:
        A dictionary of build parameter names and their values
    """
    if number is None:
        number = jenkins(ctx).get_item(fullname=fullname, depth=1).lastBuild.number

    return jenkins(ctx).get_build_parameters(fullname=fullname, number=number)


@mcp.tool(tags=['write'])
async def stop_build(ctx: Context, fullname: str, number: int) -> None:
    """Stop a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build to stop
    """
    return jenkins(ctx).stop_build(fullname=fullname, number=number)
