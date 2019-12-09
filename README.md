# embedded-portal-setup
Repository to set up a sample embedded portal to replicate Embedded Analytics with Tableau. This portal setup allows you to test out the vital functionalities that most users are exploring when determining if Tableau is a good embedded analytics solution for them.

---Pre-requisites---
1. Clean  Windows instance
2. Minimum tech specs mentioned to be adhered to - https://www.tableau.com/en-sg/products/techspecs#server
<br/>

---Tableau Server setup---
1. Install Tableau Server (https://www.tableau.com/products/server). During the installation, change the Run As User account to a Windows administrator, who would have access to CSV files - https://help.tableau.com/current/server/en-us/config_general.htm
2. Create an initial server admin user with the credentials admin/Tableau123
3. Add the IP address of the web application server as a trusted IP address (no need to restart just yet) through the TSM Web UI - https://help.tableau.com/current/server/en-us/trusted_auth_trustIP.htm
4. Make certain changes via the TSM Command Line -
    - Set the trusted tickets to unrestricted by entering the following command - tsm configuration set -k wgserver.unrestricted_ticket -v true
    - Apply all changes and restart the Tableau Server - tsm pending-changes apply
5. On the Tableau Server, create a new site called 'Template'
6. Add 2 users in the new site (any password is fine but the role must be 'Explorer (can Publish)') -
    - adrian
    - jamie
7. Create a new project titled 'Sandbox'.
8. Apply permissions on the project as per below -
    - Default project - <br/>
        - Project - Viewer <br/>
        - Workbooks - Interactor + Save/ Save As
    - Sandbox project -<br/>
        - Project - Publisher <br/>
        - Workbooks/ Data-sources - None
9. In both cases, ensure that ther project permissions are locked to the project.
10. Install Tableau Desktop (https://www.tableau.com/products/desktop) and open the workbook in the viz folder. Ensure that the data-source titled 'Sample - Superstore with Data Source Filter' is pointing at the folder titled 'data' within the source files, and not to a temporary folder.
11. Publish the workbook to Tableau Server on the 'Default' project on the 'Template' site, and ensure that you keep 'Include External Assets' unticked.
<br/>

---Web application server setup---
1. Install Python (https://www.python.org/downloads/release/python-374/). Remember to add Python to PATH during installation.
2. Use the command line to install packages using pip install (https://packaging.python.org/tutorials/installing-packages/#use-pip-for-installing) -
    - tableauserverclient
    - flask
    - cryptography
3. Navigate to the script titled 'RestCalls.py' script and modify the environment variables at the top (if all other steps have been followed exactly until now, then only the IP address of the instance needs to be modified).
4. Open a terminal window, and navigate to the FlaskApp folder. Run 'python FlaskApp.py'.
<br/>

On any machine that has access, access http://webapp-server:5000/ on a web browser and proceed to Login
