

def get_github_tools(all_tools):
    # If all_tools is None, it defaults to [] and safely skips the loop
    #print(f"in get_jira_tools jira_tools {all_tools}")
    return [
        tool for tool in (all_tools or [])
        if not tool.name.startswith("jira")
    ]


