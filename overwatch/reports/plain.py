from mako.template import Template
import pyfiglet

def render(reportType, storedMessages):
    storedMessages["banner"] = pyfiglet.figlet_format("overwatch")
    tmpl = ""
    if reportType == "lookup":
        tmpl = lookupTemplate
    elif reportType == "user_list":
        tmpl = userListTemplate
    elif reportType == "running_processes":
        tmpl = runningProcessesTemplate
    elif reportType == "suid_binaries":
        tmpl = suidBinariesTemplate
    elif reportType == "mounted_devices":
        tmpl = moundtedDevicesTemplate
    elif reportType == "useful_binaries":
        tmpl = usefulBinariesTemplate
    elif reportType == "available_compilers":
        tmpl = availableCompilersTemplate
    elif reportType == "cve_search":
        tmpl = cveSearchResultTemplate
    elif reportType == "codeanalysis":
        tmpl = codeanAlysisTemplate
    if tmpl == "":
        return ""
    return Template(tmpl).render(**storedMessages)

lookupTemplate = """
${banner}
${"-"*50}
${reportType.capitalize()} Report
Title: ${title}
CVE Code: ${cve}
Download URL: ${download_url}
${"-"*50}
Description: ${description}
${"-"*50}
Report creation date: ${report_date}
"""

userListTemplate = """
${banner}
${"-"*50}
${reportType.replace("_", " ").capitalize()} Report
Title: ${title}
${"-"*50}
% for user in users:
    % if user:
- ${user}
    % endif
% endfor
${"-"*50}
Report creation date: ${report_date}
"""

runningProcessesTemplate = """
${banner}
${"-"*50}
${reportType.replace("_", " ").capitalize()} Report
Title: ${title}
${"-"*50}
% for process in processes:
    % if process:
- ${process}
    % endif
% endfor
${"-"*50}
Report creation date: ${report_date}
"""

suidBinariesTemplate = """
${banner}
${"-"*50}
${reportType.replace("_", " ").capitalize()} Report
Title: ${title}
${"-"*50}
% for binary in binaries:
    % if binary:
- ${binary}
    % endif
% endfor
${"-"*50}
Report creation date: ${report_date}
"""

moundtedDevicesTemplate = """
${banner}
${"-"*50}
${reportType.replace("_", " ").capitalize()} Report
Title: ${title}
${"-"*50}
% for d in mounted_devices:
    % if d:
- ${d}
    % endif
% endfor
${"-"*50}
Report creation date: ${report_date}
"""

usefulBinariesTemplate = """
${banner}
${"-"*50}
${reportType.replace("_", " ").capitalize()} Report
Title: ${title}
${"-"*50}
% for b in useful_binaries:
    % if b:
- ${b}
    % endif
% endfor
${"-"*50}
Report creation date: ${report_date}
"""

availableCompilersTemplate = """
${banner}
${"-"*50}
${reportType.replace("_", " ").capitalize()} Report
Title: ${title}
${"-"*50}
% for c in available_compilers:
    % if c:
- ${c}
    % endif
% endfor
${"-"*50}
Report creation date: ${report_date}
"""

cveSearchResultTemplate = """
${banner}
${"-"*50}
${reportType.replace("_", " ").capitalize()} Report
Title: ${title}
${"-"*50}
Search parameters:
Keyword: ${keyword}
Platform: ${platform}
Ports: ${','.join([str(p) for p in ports])}
URL: ${search_url}
${"-"*50}
Results:
% for r in results:
${r.title}
${r.id} :::: ${r.cve}
${"/"*20}
% endfor
Report creation date: ${report_date}
"""

codeanAlysisTemplate = """
${banner}
${"-"*50}
${reportType.replace("_", " ").capitalize()} Report
Title: ${title}
${"-"*50}
Analysis parameters:
Repository: ${repo}
Version: ${version}
Level: ${level}
${"-"*50}
Results:
% for r in results:
${r["level"]} :::: ${r["msg"]}
${"/"*20}
% endfor
Report creation date: ${report_date}
"""
