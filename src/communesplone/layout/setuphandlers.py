def simplify(setup_tool):
    """Post handler of the simplify profile: full-layout group, permissions for administrators only."""
    site = setup_tool.portal_url.getPortalObject()
    # Add a full-layout group
    groups_tool = site.portal_groups
    group_id = "full-layout"
    if group_id not in groups_tool.getGroupIds():
        groups_tool.addGroup(group_id, title="Full edition layout")
        groups_tool.addPrincipalToGroup("Administrators", "full-layout")
        groups_tool.addPrincipalToGroup("Site Administrators", "full-layout")

    # Clean user interface
    site.manage_permission(
        "Sharing page: Delegate roles",
        (
            "Manager",
            "Site Administrator",
        ),
        acquire=0,
    )
    site.manage_permission(
        "Modify view template",
        (
            "Manager",
            "Site Administrator",
        ),
        acquire=0,
    )
    site.manage_permission(
        "Review portal content",
        ("Manager", "Site Administrator", "Reviewer"),
        acquire=0,
    )
    site.manage_permission(
        "Modify constrain types",
        (
            "Manager",
            "Site Administrator",
        ),
        acquire=0,
    )
    site.manage_permission(
        "CMFPlacefulWorkflow: Manage workflow policies",
        (
            "Manager",
            "Site Administrator",
        ),
        acquire=0,
    )
