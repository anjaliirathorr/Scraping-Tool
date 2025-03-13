# Scrapping-Tool

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scraping Tool</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        h1, h2 { color: #333; }
        code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
        pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>Scraping Tool</h1>
    
    <h2>Overview</h2>
    <p>This Scraping Tool is designed to extract data from websites <strong>without relying on third-party APIs</strong>, reducing dependencies and providing greater flexibility. It allows users to scrape, process, and extract relevant data efficiently.</p>
    
    <h2>Features</h2>
    <ul>
        <li>Removes dependency on third-party APIs</li>
        <li>Automates data extraction from web pages</li>
        <li>Allows customization of scraping parameters</li>
        <li>Processes raw HTML to extract required data</li>
    </ul>
    
    <h2>Installation & Usage</h2>
    
    <h3>Prerequisites</h3>
    <p><strong>Python</strong> installed on your system (if not installed, download from <a href="https://www.python.org/downloads/">Python.org</a>)</p>
    
    <h3>Steps to Run the Tool</h3>
    <ol>
        <li><strong>Extract</strong> the files into an empty folder.</li>
        <li><strong>Install Python</strong> if not already installed.</li>
        <li><strong>Open Command Prompt.</strong></li>
        <li>Navigate to the extracted folder using:<br>
            <pre><code>cd path/to/extracted-folder</code></pre>
        </li>
        <li><strong>Create a folder named <code>data</code></strong> inside the extracted folder:<br>
            <pre><code>mkdir data</code></pre>
        </li>
        <li>If needed, update <strong>starting URL, start page, and end page</strong> in the <code>.env</code> file.</li>
        <li>Run the scraping script:<br>
            <pre><code>python getdata.py</code></pre>
        </li>
        <li>Once the above script finishes running, execute:<br>
            <pre><code>python gethtml.py</code></pre>
        </li>
        <li>After running the above command, process the extracted data with:<br>
            <pre><code>python process.py</code></pre>
        </li>
    </ol>
    
    <h2>Contribution & Support</h2>
    <p>Feel free to contribute or report any issues by raising a ticket in the repository.</p>
    
    <hr>
    <p><strong>Author:</strong> <a href="https://github.com/anjaliirathorr">Anjali Rathore</a></p>
    <p><strong>Repository:</strong> <a href="https://github.com/anjaliirathorr/Scrapping-Tool">Scraping Tool</a></p>
</body>
</html>

