from mako.template import Template

def render(reportType, storedMessages):
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
<!DOCTYPE html>
<html lang="en">
    <head>        
        <meta charset="UTF-8">
        <title>${reportType.capitalize()} Report</title>
        <style>
            body {
                font-family: baskerville, serif;
            }
            p {
                font-size: 14px;
            }
            h1 {
                font-size: 50px;
            }
            h2 {
                font-size: 30px;
            }
            .header {
                height: 10vh;
            }
            .content {
                height: 80vh;
            }
            .footer {
                height: 10vh;
            }
            .content, .header {
                display: flex;
                flex-flow: column;
                align-items: center;
            }
            .content > div, .header > div {
                width: 1920px;
                display: flex;
                justify-content: center;
            }
            a, a:visited {
                color: darkgray;
            }
            .content .description {
                max-height: 40vh;
                overflow-y: auto;
            }
            
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
            }
            .footer > .wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-flow: column;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
            .download_url {
                color: lightgray;
            }
            .download_url p {
                font-size: 10px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">
                <h1>${title}</h1>
            </div>
        </div>
        <div class="content">
            <div class="cve">
                <h2>
                    <a href="${download_url}">${cve}</a>
                <h2>
            </div>
            <div class="description">
                <p>
                    ${description}
                </p>
            </div>
        </div>
        <div class="footer">
            <div class="wrapper">
                <div class="date">Report creation date: ${report_date}</div>
                <div class="download_url">
                    <p>Download url is can be found here ${download_url}</p>
                </div>
            </div>
        </div>
    </body>
</html>
"""

userListTemplate = """
<!DOCTYPE html>
<html lang="en">
    <head>        
        <meta charset="UTF-8">
        <title>${reportType.capitalize()} Report</title>
        <style>
            body {
                font-family: baskerville, serif;
            }
            p {
                font-size: 14px;
            }
            h1 {
                font-size: 50px;
            }
            .header {
                height: 10vh;
            }
            .content {
                height: 80vh;
            }
            .footer {
                height: 10vh;
            }
            .content, .header {
                display: flex;
                flex-flow: column;
                align-items: center;
            }
            .content > div, .header > div {
                width: 1920px;
                display: flex;
                justify-content: center;
            }
            .content .users {
                max-height: 40vh;
                overflow-y: auto;
            }
            
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
            }
            .footer > .wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-flow: column;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">
                <h1>${title}</h1>
            </div>
        </div>
        <div class="content">
            <div class="users">
                <ul>
                % for user in users:
                    % if user:
                        <li>
                            <p>${user}</p>
                        </li>
                    % endif
                % endfor
                </ul>
            </div>
        </div>
        <div class="footer">
            <div class="wrapper">
                <div class="date">Report creation date: ${report_date}</div>
            </div>
        </div>
    </body>
</html>
"""

runningProcessesTemplate = """
<!DOCTYPE html>
<html lang="en">
    <head>        
        <meta charset="UTF-8">
        <title>${reportType.capitalize()} Report</title>
        <style>
            body {
                font-family: baskerville, serif;
            }
            p {
                font-size: 14px;
            }
            h1 {
                font-size: 50px;
            }
            .header {
                height: 10vh;
            }
            .content {
                height: 80vh;
            }
            .footer {
                height: 10vh;
            }
            .content, .header {
                display: flex;
                flex-flow: column;
                align-items: center;
            }
            .content > div, .header > div {
                width: 1920px;
                display: flex;
                justify-content: center;
            }
            .content .processes {
                max-height: 40vh;
                overflow-y: auto;
            }
            
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
            }
            .footer > .wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-flow: column;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">
                <h1>${title}</h1>
            </div>
        </div>
        <div class="content">
            <div class="processes">
                <ul>
                % for process in processes:
                    % if process:
                        <li>
                            <p>${process}</p>
                        </li>
                    % endif
                % endfor
                </ul>
            </div>
        </div>
        <div class="footer">
            <div class="wrapper">
                <div class="date">Report creation date: ${report_date}</div>
            </div>
        </div>
    </body>
</html>
"""

suidBinariesTemplate = """
<!DOCTYPE html>
<html lang="en">
    <head>        
        <meta charset="UTF-8">
        <title>${reportType.capitalize()} Report</title>
        <style>
            body {
                font-family: baskerville, serif;
            }
            p {
                font-size: 14px;
            }
            h1 {
                font-size: 50px;
            }
            .header {
                height: 10vh;
            }
            .content {
                height: 80vh;
            }
            .footer {
                height: 10vh;
            }
            .content, .header {
                display: flex;
                flex-flow: column;
                align-items: center;
            }
            .content > div, .header > div {
                width: 1920px;
                display: flex;
                justify-content: center;
            }
            .content .suid {
                max-height: 40vh;
                overflow-y: auto;
            }
            
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
            }
            .footer > .wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-flow: column;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">
                <h1>${title}</h1>
            </div>
        </div>
        <div class="content">
            <div class="suid">
                <ul>
                % for binary in binaries:
                    % if binary:
                        <li>
                            <p>${binary}</p>
                        </li>
                    % endif
                % endfor
                </ul>
            </div>
        </div>
        <div class="footer">
            <div class="wrapper">
                <div class="date">Report creation date: ${report_date}</div>
            </div>
        </div>
    </body>
</html>
"""

moundtedDevicesTemplate = """
<!DOCTYPE html>
<html lang="en">
    <head>        
        <meta charset="UTF-8">
        <title>${reportType.capitalize()} Report</title>
        <style>
            body {
                font-family: baskerville, serif;
            }
            p {
                font-size: 14px;
            }
            h1 {
                font-size: 50px;
            }
            .header {
                height: 10vh;
            }
            .content {
                height: 80vh;
            }
            .footer {
                height: 10vh;
            }
            .content, .header {
                display: flex;
                flex-flow: column;
                align-items: center;
            }
            .content > div, .header > div {
                width: 1920px;
                display: flex;
                justify-content: center;
            }
            .content .mounted-devices {
                max-height: 40vh;
                overflow-y: auto;
            }
            
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
            }
            .footer > .wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-flow: column;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">
                <h1>${title}</h1>
            </div>
        </div>
        <div class="content">
            <div class="mounted-devices">
                <ul>
                % for d in mounted_devices:
                    % if d:
                        <li>
                            <p>${d}</p>
                        </li>
                    % endif
                % endfor
                </ul>
            </div>
        </div>
        <div class="footer">
            <div class="wrapper">
                <div class="date">Report creation date: ${report_date}</div>
            </div>
        </div>
    </body>
</html>
"""

usefulBinariesTemplate = """
<!DOCTYPE html>
<html lang="en">
    <head>        
        <meta charset="UTF-8">
        <title>${reportType.capitalize()} Report</title>
        <style>
            body {
                font-family: baskerville, serif;
            }
            p {
                font-size: 14px;
            }
            h1 {
                font-size: 50px;
            }
            .header {
                height: 10vh;
            }
            .content {
                height: 80vh;
            }
            .footer {
                height: 10vh;
            }
            .content, .header {
                display: flex;
                flex-flow: column;
                align-items: center;
            }
            .content > div, .header > div {
                width: 1920px;
                display: flex;
                justify-content: center;
            }
            .content .useful-binaries {
                max-height: 40vh;
                overflow-y: auto;
            }
            
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
            }
            .footer > .wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-flow: column;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">
                <h1>${title}</h1>
            </div>
        </div>
        <div class="content">
            <div class="useful-binaries">
                <ul>
                % for b in useful_binaries:
                    % if b:
                        <li>
                            <p>${b}</p>
                        </li>
                    % endif
                % endfor
                </ul>
            </div>
        </div>
        <div class="footer">
            <div class="wrapper">
                <div class="date">Report creation date: ${report_date}</div>
            </div>
        </div>
    </body>
</html>
"""

availableCompilersTemplate = """
<!DOCTYPE html>
<html lang="en">
    <head>        
        <meta charset="UTF-8">
        <title>${reportType.capitalize()} Report</title>
        <style>
            body {
                font-family: baskerville, serif;
            }
            p {
                font-size: 14px;
            }
            h1 {
                font-size: 50px;
            }
            .header {
                height: 10vh;
            }
            .content {
                height: 80vh;
            }
            .footer {
                height: 10vh;
            }
            .content, .header {
                display: flex;
                flex-flow: column;
                align-items: center;
            }
            .content > div, .header > div {
                width: 1920px;
                display: flex;
                justify-content: center;
            }
            .content .available-compilers {
                max-height: 40vh;
                overflow-y: auto;
            }
            
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
            }
            .footer > .wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-flow: column;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">
                <h1>${title}</h1>
            </div>
        </div>
        <div class="content">
            <div class="available-compilers">
                <ul>
                % for c in available_compilers:
                    % if c:
                        <li>
                            <p>${c}</p>
                        </li>
                    % endif
                % endfor
                </ul>
            </div>
        </div>
        <div class="footer">
            <div class="wrapper">
                <div class="date">Report creation date: ${report_date}</div>
            </div>
        </div>
    </body>
</html>
"""

cveSearchResultTemplate = """
<!DOCTYPE html>
<html lang="en">
    <head>        
        <meta charset="UTF-8">
        <title>${reportType.capitalize()} Report</title>
        <style>
            body {
                font-family: baskerville, serif;
            }
            p {
                font-size: 14px;
            }
            h1 {
                font-size: 50px;
            }
            h2 {
                font-size: 30px;
            }
            .header {
                height: 10vh;
            }
            .content {
                height: 80vh;
            }
            .footer {
                height: 10vh;
            }
            .content, .header {
                display: flex;
                flex-flow: column;
                align-items: center;
            }
            .content > div, .header > div {
                width: 1920px;
                display: flex;
                justify-content: center;
            }
            .content .search-parameters {
                display: flex;
                justify-content: space-evenly;
            }
            .content .search-url {
                color: lightslategray;
            }
            .content .results {
                max-height: 40vh;
                overflow-y: auto;
            }

            .content .results table {
                width: 100%;
            }

            .content .results table tr td{
                text-align: center;
            }
            
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
            }
            .footer > .wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-flow: column;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
            .download_url, .search-url p, .search-url p a {
                color: lightgray;
            }
            .search-url p a:visited {
                color: lightgray;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">
                <h1>${title}</h1>
            </div>
        </div>
        <div class="content">
            <div class="search-parameters">
                <div class="keyword">
                    <lable>Keyword</lable>
                    <p>${keyword}</p>
                </div>
                <div class="platform">
                    <lable>Platform</lable>
                    <p>${platform}</p>
                </div>
                <div class="ports">
                    <lable>Ports</lable>
                    <p>${','.join([str(p) for p in ports])}</p>
                </div>
            </div>
            <div class="search-url">
                <p>Search url was: <a href="${search_url}">${search_url}</a></p>
            </div>
            <div class="results">
                <table>
                    <thead>
                        <th>ID</th>
                        <th>CVE</th>
                        <th>Title</th>
                    </thead>
                    <tbody>
                    % for r in results:
                        <tr>
                            <td>${r.id}</td>
                            <td>${r.cve}</td>
                            <td>${r.title}</td>
                        </tr>
                    % endfor
                    </tbody>
                </table>
            </div>
        </div>
        <div class="footer">
            <div class="wrapper">
                <div class="date">Report date: ${report_date}</div>
            </div>
        </div>
    </body>
</html>
"""

codeanAlysisTemplate = """
<!DOCTYPE html>
<html lang="en">
    <head>        
        <meta charset="UTF-8">
        <title>${reportType.capitalize()} Report</title>
        <style>
            body {
                font-family: baskerville, serif;
            }
            p {
                font-size: 14px;
            }
            h1 {
                font-size: 50px;
            }
            h2 {
                font-size: 30px;
            }
            .header {
                height: 10vh;
            }
            .content {
                height: 80vh;
            }
            .footer {
                height: 10vh;
            }
            .content, .header {
                display: flex;
                flex-flow: column;
                align-items: center;
            }
            .content > div, .header > div {
                width: 1920px;
                display: flex;
                justify-content: center;
            }
            .content .analysis-parameters {
                display: flex;
                justify-content: space-evenly;
            }
            .level-INFO {
                color: green;
            }
            .level-WARNING {
                color: orange;
            }
            .level-ERROR {
                color: red;
            }
            .content .results {
                max-height: 40vh;
                overflow-y: auto;
            }

            .content .results table {
                width: 100%;
            }

            .content .results table tr td{
                text-align: center;
            }
            
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
            }
            .footer > .wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-flow: column;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
            .download_url, .search-url p, .search-url p a {
                color: lightgray;
            }
            .search-url p a:visited {
                color: lightgray;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">
                <h1>${title}</h1>
            </div>
        </div>
        <div class="content">
            <div class="analysis-parameters">
                <div class="repo">
                    <lable>Repository</lable>
                    <p>${repo}</p>
                </div>
                <div class="version">
                    <lable>Version</lable>
                    <p>${version}</p>
                </div>
                <div class="level">
                    <lable>Level</lable>
                    <p class="level-${level}">${level}</p>
                </div>
            </div>
            <div class="results">
                <table>
                    <thead>
                        <th>Severity</th>
                        <th>Message</th>
                    </thead>
                    <tbody>
                    % for r in results:
                        <tr>
                            <td class="level-${r["level"]}">${r["level"]}</td>
                            <td>${r["msg"]}</td>
                        </tr>
                    % endfor
                    </tbody>
                </table>
            </div>
        </div>
        <div class="footer">
            <div class="wrapper">
                <div class="date">Report date: ${report_date}</div>
            </div>
        </div>
    </body>
</html>
"""
