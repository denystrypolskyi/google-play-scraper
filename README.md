<h1>Description</h1>
<p>The script is used to retrieve detailed information and comments about an app from Google Play using Selenium.</p>
<h2>Features</h2>
<ul>
  <li><strong>Retrieve app details:</strong>
    <ul>
      <li>Title</li>
      <li>Description</li>
      <li>Image</li>
      <li>Rating</li>
      <li>Age category</li>
      <li>Number of downloads</li>
      <li>Last update date</li>
      <li>Contains ads</li>
      <li>In-app purchases</li>
      <li>Release date</li>
      <li>Developer name</li>
    </ul>
  </li>
  <li><strong>Retrieve comments:</strong>
    <ul>
      <li>Ability to specify the number of comments to retrieve</li>
    </ul>
  </li>
</ul>
<h2>Requirements</h2>
<ul>
  <li>Python 3.x</li>
  <li>Selenium library (<code>pip install selenium</code>)</li>
  <li>WebDriver (ChromeDriver)</li>
  <li>Chrome browser</li>
</ul>
<h2>How to Run</h2>
<ol>
  <li>Install the required libraries:
    <pre><code>pip install selenium</code></pre>
  </li>
  <li>Download the appropriate WebDriver for Chrome (ChromeDriver) and place it in the path <code>./chromedriver.exe</code>.</li>
  <li>Run the script:
    <pre><code>python google_play_scraper.py</code></pre>
  </li>
  <li>Follow the instructions in the console to provide the app ID and the desired number of comments.</li>
</ol>